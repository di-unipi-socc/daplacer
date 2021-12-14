import random
from multiprocessing import Process, Manager

import pandas as pd
from parse import *
from pyswip import Prolog

APP_NAME = "museuMonitor"
DAP = "dap(A,P,R,Infs,Time).".format(APP_NAME)
DAP_CR = "dapCR(A,NP,NR,Infs,Time).".format(APP_NAME)

INFR_FILE = "code/infra.pl"
NODE = "node({}, {}, ({}, {}, {}), {}, {}).\n"
LINK = "link({}, {}, {}, {}).\n"


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
		print("fault")
		res.append({})


def change_nodes(nodes, prob):
	res = []
	for n in nodes:
		if random.random() < prob:
			name, sw, cpu, ram, hdd, sec, iot = parse(NODE, n)
			ram = float(ram)
			hdd = float(hdd)
			new_ram = round(random.uniform(ram // 2, ram * 1.2), 2)
			new_hdd = round(random.uniform(hdd // 2, hdd * 1.2), 2)
			n = NODE.format(name, sw, cpu, new_ram, new_hdd, sec, iot)
		# print("{} changed".format(name))
		res.append(n)
	return res


def change_links(links, prob):
	res = []
	for l in links:
		if random.random() < prob:
			n1, n2, lat, bw = parse(LINK, l)
			lat = float(lat)
			bw = float(bw)
			new_lat = round(random.uniform(5, lat * 1.5), 2)
			new_bw = round(random.uniform(bw // 1.2, bw * 1.2), 2)
			l = LINK.format(n1, n2, new_lat, new_bw)
		res.append(l)
	return res


def change_infr(prob):
	f_r = open(INFR_FILE, "r")
	infr = f_r.readlines()
	nodes = [i for i in infr if i.startswith("node(")]
	links = [i for i in infr if i.startswith("link(")]
	for n in nodes:
		infr.remove(n)
	for l in links:
		infr.remove(l)
	f_r.close()

	new_nodes = change_nodes(nodes, prob)
	new_links = change_links(links, prob)
	infr.extend(new_nodes)
	infr.extend(new_links)

	f_w = open(INFR_FILE, "w")
	f_w.writelines(infr)
	f_w.close()


def change_app(epoch):
	if epoch % 60 == 0:
		commit_no = epoch // 60
		eval("commit_{}()".format(commit_no))


def main(epochs=10, prob=0.1):
	mgr = Manager()
	res_no_cr = mgr.list()
	res_cr = []

	p_cr = Prolog()
	p_cr.consult("code/dap2.pl")
	i = 1

	while i <= epochs:
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
		sys.stdout.write("Done {}/{}".format(i + 1, epochs))
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

	print("TIME: {:.6f} \t TIME_CR: {:.6f}".format(avg_time, avg_time_cr))
	print("INFS: {} \t INFS_CR: {}".format(avg_infs, avg_infs_cr))

	filename = "results_{}.csv".format(prob)
	df.index.name = "Epoch"
	df.to_csv("csv/{}".format(filename))


if __name__ == '__main__':
	main(epochs=10, prob=0.5)
