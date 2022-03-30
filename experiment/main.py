import sys
import os
import shutil
import random
from multiprocessing import Process, Manager

import pandas as pd
from parse import *
from pyswip import Prolog
from commits import *

APP_NAME = "museuMonitor"
DAP = "dap(A,P,R,Infs,Time).".format(APP_NAME)
DAP_CR = "dapCR(A,NP,NR,Infs,Time).".format(APP_NAME)

INFR_FILE = "code/infra.pl"
APP_FILE = "code/app.pl"
NODE = "node({}, {}, ({}, {}, {}), {}, {}).\n"
LINK = "link({}, {}, {}, {}).\n"

HW_CAPS = {}
QOS_CAPS = {}

FAIL_PROB = 0.02
SEED = 33


def my_query(s, p):
	q = p.query(s)
	result = next(q)
	return result


def no_cr_process(res):
	p = Prolog()
	p.consult("code/dap.pl")

	try:
		no_cr = my_query(DAP, p)
		res.append({"Infs": no_cr["Infs"], "Time": no_cr["Time"]})

	except StopIteration:
		print(" - fault")
		res.append({})


def fail():
	return random.random() < FAIL_PROB


def save_caps():
	global HW_CAPS, QOS_CAPS
	f_r = open(INFR_FILE, "r")
	infr = f_r.readlines()
	nodes = [i for i in infr if i.startswith("node(")]
	links = [i for i in infr if i.startswith("link(")]

	for n in nodes:
		name, _, _, ram, hdd, _, _ = parse(NODE, n)
		HW_CAPS[name] = {'ram': float(ram), 'hdd': float(hdd)}

	for ln in links:
		n1, n2, lat, bw = parse(LINK, ln)
		QOS_CAPS[(n1, n2)] = {'lat': float(lat), 'bw': float(bw)}


def change_nodes(nodes, prob):
	res = []
	for n in nodes:
		if random.random() < prob:
			name, sw, cpu, _, _, sec, iot = parse(NODE, n)
			ram = HW_CAPS[name]['ram']
			hdd = HW_CAPS[name]['hdd']
			new_ram = round(random.uniform(ram//10, ram * 1.1), 2) if not fail() else 0
			new_hdd = round(random.uniform(hdd//10, hdd * 1.2), 2) if not fail() else 0
			n = NODE.format(name, sw, cpu, new_ram, new_hdd, sec, iot)
		res.append(n)
	return res


def change_links(links, prob):
	res = []
	for ln in links:
		if random.random() < prob:
			n1, n2, _, _ = parse(LINK, ln)
			lat = QOS_CAPS[(n1, n2)]['lat']
			bw = QOS_CAPS[(n1, n2)]['bw']
			new_lat = round(random.uniform(lat // 2, lat * 1.5), 2) if not fail() else 1000
			new_bw = round(random.uniform(bw // 2, bw * 1.1), 2) if not fail() else 0
			ln = LINK.format(n1, n2, new_lat, new_bw)
		res.append(ln)
	return res


def change_infr(prob):
	f_r = open(INFR_FILE, "r")
	infr = f_r.readlines()
	nodes = [i for i in infr if i.startswith("node(")]
	links = [i for i in infr if i.startswith("link(")]
	for n in nodes:
		infr.remove(n)
	for ln in links:
		infr.remove(ln)
	f_r.close()

	new_nodes = change_nodes(nodes, prob)
	new_links = change_links(links, prob)
	infr.extend(new_nodes)
	infr.extend(new_links)

	f_w = open(INFR_FILE, "w")
	f_w.writelines(infr)
	f_w.close()


def change_app(epoch):
	if epoch % 100 == 0:
		commit_no = epoch // 100
		eval("commit_{}()".format(commit_no))


def get_data(n):
	if os.path.exists(APP_FILE):
		os.remove(APP_FILE)
	if os.path.exists(INFR_FILE):
		os.remove(INFR_FILE)

	shutil.copy("infra/app.pl", APP_FILE)
	shutil.copy(f"infra/infra_{n}.pl", INFR_FILE)


def main(n=16, prob=0.1, epochs=600):
	mgr = Manager()
	res_no_cr = mgr.list()
	res_cr = []

	# preliminary operation
	random.seed(SEED)
	get_data(n)

	p_cr = Prolog()
	p_cr.consult("code/dap2.pl")
	i = 1

	while i <= epochs:

		if i == 1:
			save_caps()
		# NO CR PROCESS
		process = Process(target=no_cr_process, args=(res_no_cr,))
		process.start()
		process.join()

		# CR PROCESS
		try:
			my_query("make", p_cr)
			cr = my_query(DAP_CR, p_cr)
			res_cr.append({"InfsCR": cr["Infs"], "TimeCR": cr["Time"]})
		except StopIteration:
			print("CR fault")
			res_cr.append({})

		sys.stdout.write("\r")
		sys.stdout.flush()
		sys.stdout.write("Done {}/{}".format(i, epochs))
		i += 1

		change_app(i)
		change_infr(prob)

	print("\n")
	res_no_cr = list(res_no_cr)
	df_no_cr = pd.DataFrame.from_records(res_no_cr, columns=["Infs", "Time"])
	df_cr = pd.DataFrame.from_records(res_cr, columns=["InfsCR", "TimeCR"])
	df = pd.concat([df_no_cr, df_cr], axis=1, ignore_index=True)
	df.columns = ["Infs", "Time", "InfsCR", "TimeCR"]

	avg_time = df['Time'].mean()
	avg_time_cr = df['TimeCR'].mean()

	avg_infs = df['Infs'].mean()
	avg_infs_cr = df['InfsCR'].mean()

	print("Done for {} prob\n".format(prob))
	print("TIME: {:.6f} \t TIME_CR: {:.6f}".format(avg_time, avg_time_cr))
	print("INFS: {} \t INFS_CR: {}".format(avg_infs, avg_infs_cr))

	filename = "results_{}_{}.csv".format(n, prob)
	df.index.name = "Epoch"
	df.to_csv("csv/{}".format(filename))


if __name__ == '__main__':
	PROBS = [0.1, 0.2, 0.4, 0.5]
	NODES = [16, 32, 64, 128, 256, 512]
	for n in NODES:
		for p in PROBS:	
			main(n=n, prob=p, epochs=600)
