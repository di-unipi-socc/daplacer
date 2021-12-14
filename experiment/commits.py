APP_FILE = "code/app.pl"

SERVICE = "service({}, [{}], ({}, {}, {}), [{}], [{}], [{}]).\n"
DATA_SERVICE = "data({}, [{}], [{}], ({}, {}, {}), [{}]).\n"
E2E = "e2e({}, {}, {}, [{}]).\n"


def commit_1():
	print("Adding localisator and locStorage")
	f = open(APP_FILE, "a")
	new_ps = SERVICE.format("localisator", "ubuntu", 3, 2, 32, "encryption, auth", "smartphone", "")
	new_ds = DATA_SERVICE.format("locStorage", "location", "mySQL, ubuntu", 3, 3, 64, "encryption, auth", "smartphone")
	int1 = E2E.format("rLoc", "locStorage", 30, "(location,40)")
	int2 = E2E.format("locStorage", "localisator", 30, "(location,40)")

	f.write(new_ds)
	f.write(new_ps)
	f.write(int1)
	f.write(int2)
	f.close()


def commit_2():
	print("Removing localisator")
	f_r = open(APP_FILE, "r")
	lines = f_r.readlines()
	ps = [l for l in lines if l.startswith("service(localisator") or l.startswith("e2e(locStorage, localisator")]
	f_r.close()

	for p in ps:
		lines.remove(p)
	f_w = open(APP_FILE, "w")
	f_w.writelines(lines)
	f_w.close()


def commit_3():
	print("Change locStorage requirements")
	f_r = open(APP_FILE, "r")
	lines = f_r.readlines()
	ps = [l for l in lines if l.startswith("data(locStorage")]
	f_r.close()

	lines.remove(ps[0])
	new_ds = DATA_SERVICE.format("locStorage", "location", "mySQL, ubuntu", 3, 4, 128, "encryption, auth", "smartphone")
	lines.append(new_ds)
	f_w = open(APP_FILE, "w")
	f_w.writelines(lines)
	f_w.close()


def commit_4():
	print("add/remove e2e interactions")
	f_r = open(APP_FILE, "r")
	lines = f_r.readlines()
	ps = [l for l in lines if l.startswith("e2e(rLoc, dataStorage")]
	f_r.close()

	lines.remove(ps[0])

	int1 = E2E.format("locStorage", "interface", 50, "(location,40)")
	int2 = E2E.format("locStorage", "shadersController", 40, "(location,40)")
	lines.append(int1)
	lines.append(int2)
	f_w = open(APP_FILE, "w")
	f_w.writelines(lines)
	f_w.close()


def commit_5():
	print("change e2e interaction parameters")
	f_r = open(APP_FILE, "r")
	lines = f_r.readlines()
	ps = [l for l in lines if l.startswith("e2e(locStorage, interface") or
	      l.startswith("e2e(locStorage, shadersController")]
	f_r.close()

	for p in ps:
		lines.remove(p)

	int1 = E2E.format("locStorage", "interface", 30, "(location,50)")
	int2 = E2E.format("locStorage", "shadersController", 40, "(location,60)")
	lines.append(int1)
	lines.append(int2)
	f_w = open(APP_FILE, "w")
	f_w.writelines(lines)
	f_w.close()


def commit_6():
	pass


if __name__ == '__main__':
	commit_5()
