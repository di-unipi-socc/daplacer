APP_FILE = "code/app.pl"

SERVICE = "service({}, [{}], ({}, {}, {}), [{}], {}).\n"
DATA_TYPE = "dataType({}, {}, [{}]).\n"
E2E = "e2e({}, {}, {}, [{}]).\n"


def commit_1():
	f = open(APP_FILE, "a")
	new_dt = DATA_TYPE.format("location", 0.3, "encryption, auth")
	new_s1 = SERVICE.format("localisator", "ubuntu", 3, 2, 32, "location", 20)
	new_s2 = SERVICE.format("locStorage", "mySQL, ubuntu", 3, 3, 64, "location", 80)
	int1 = E2E.format("rLoc", "locStorage", 30, "(location,40)")
	int2 = E2E.format("locStorage", "localisator", 30, "(location,40)")
	f.write("\n")
	f.write(new_dt)
	f.write(new_s1)
	f.write(new_s2)
	f.write(int1)
	f.write(int2)
	f.close()

	print("Adding localisator and locStorage")


def commit_2():
	f_r = open(APP_FILE, "r")
	lines = f_r.readlines()
	ps = [l for l in lines if l.startswith("service(localisator") or l.startswith("e2e(locStorage, localisator")]
	f_r.close()

	for p in ps:
		lines.remove(p)
	f_w = open(APP_FILE, "w")
	f_w.writelines(lines)
	f_w.close()

	print("Removing localisator")


def commit_3():
	f_r = open(APP_FILE, "r")
	lines = f_r.readlines()
	ps = [l for l in lines if l.startswith("service(locStorage")]
	f_r.close()

	lines.remove(ps[0])
	new_ds = SERVICE.format("locStorage", "mySQL, ubuntu", 3, 4, 128, "location", 120)
	lines.append(new_ds)
	f_w = open(APP_FILE, "w")
	f_w.writelines(lines)
	f_w.close()

	print("Change locStorage requirements")


def commit_4():
	f_r = open(APP_FILE, "r")
	lines = f_r.readlines()
	ps = [l for l in lines if l.startswith("e2e(rLoc, locStorage")]
	f_r.close()

	lines.remove(ps[0])

	int1 = E2E.format("locStorage", "interface", 50, "(location,40)")
	int2 = E2E.format("locStorage", "controllerController", 40, "(location,40)")
	lines.append(int1)
	lines.append(int2)
	f_w = open(APP_FILE, "w")
	f_w.writelines(lines)
	f_w.close()

	print("Add/remove e2e interactions")


def commit_5():
	f_r = open(APP_FILE, "r")
	lines = f_r.readlines()
	ps = [l for l in lines if l.startswith("e2e(locStorage, interface") or
	      l.startswith("e2e(locStorage, controller")]
	f_r.close()

	for p in ps:
		lines.remove(p)

	int1 = E2E.format("locStorage", "interface", 30, "(location,50)")
	int2 = E2E.format("locStorage", "controller", 40, "(location,60)")
	lines.append(int1)
	lines.append(int2)
	f_w = open(APP_FILE, "w")
	f_w.writelines(lines)
	f_w.close()

	print("Change e2e interaction parameters")


def commit_6():
	pass


if __name__ == '__main__':
	commit_6()
