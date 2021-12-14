bwTh(100).

dataBinding(interface, rAcc, accell20).
dataBinding(interface, rVid, video3).
dataBinding(dataStorage, rLoc, loc38).
dataBinding(dataStorage, rWht, wht42).
dataBinding(shadersController, rRly, relay4).

sensor(wht42, temperature, [weather]).
sensor(loc38, smartphone, [location, accelerometer]).
sensor(accell20, smartphone, [accelerometer]).
actuator(video3, display).
actuator(relay4, relay).

node(parkingServices, [python, mySQL], (2.4, 2, 16), [encryption, auth], [wht42, loc38]).
node(westEntry, [ubuntu], (2.4, 2, 32), [encryption], [video3, relay4]).
node(kleiberHall, [ubuntu, mySQL], (2.4, 3, 50), [], []).
node(hoaglandAnnex, [ubuntu], (2.4, 6, 128), [auth], [accell20]).
node(briggsHall, [ubuntu, mySQL], (3, 6, 128), [auth], []).
node(mannLab, [ubuntu, python], (3, 6, 256), [encryption, auth], []).
node(lifeSciences, [python, mySQL], (3, 6, 256), [encryption, auth], []).
node(sciencesLectureHall, [ubuntu, mySQL], (3, 6, 256), [encryption, auth], []).
node(firePolice, [ubuntu, mySQL, python], (4, 8, 512), [encryption, auth], []).
node(studentCenter, [ubuntu, mySQL, python], (4, 8, 512), [encryption, auth], []).
node(isp, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(cloud, [ubuntu, mySQL, python], (6, 32, 10000), [encryption, auth], []).

link(isp, firePolice, 10, 10000).
link(firePolice, isp, 10, 10000).
link(isp, studentCenter, 10, 10000).
link(studentCenter, isp, 10, 10000).
link(isp, cloud, 50, 100000).
link(cloud, isp, 50, 100000).
link(parkingServices, westEntry, 15, 700).
link(parkingServices, lifeSciences, 15, 700).
link(parkingServices, mannLab, 15, 700).
link(westEntry, parkingServices, 15, 700).
link(westEntry, mannLab, 15, 700).
link(westEntry, firePolice, 15, 700).
link(firePolice, westEntry, 15, 700).
link(firePolice, mannLab, 15, 700).
link(firePolice, kleiberHall, 15, 700).
link(firePolice, hoaglandAnnex, 15, 700).
link(mannLab, parkingServices, 15, 700).
link(mannLab, westEntry, 15, 700).
link(mannLab, firePolice, 15, 700).
link(mannLab, lifeSciences, 15, 700).
link(mannLab, briggsHall, 15, 700).
link(mannLab, sciencesLectureHall, 15, 700).
link(mannLab, kleiberHall, 15, 700).
link(mannLab, hoaglandAnnex, 15, 700).
link(hoaglandAnnex, mannLab, 15, 700).
link(hoaglandAnnex, firePolice, 15, 700).
link(hoaglandAnnex, kleiberHall, 15, 700).
link(kleiberHall, hoaglandAnnex, 15, 700).
link(kleiberHall, mannLab, 15, 70).
link(kleiberHall, briggsHall, 15, 700).
link(kleiberHall, firePolice, 15, 700).
link(kleiberHall, sciencesLectureHall, 15, 700).
link(briggsHall, mannLab, 15, 700).
link(briggsHall, lifeSciences, 15, 700).
link(briggsHall, kleiberHall, 15, 700).
link(briggsHall, sciencesLectureHall, 15, 700).
link(lifeSciences, parkingServices, 15, 700).
link(lifeSciences, mannLab, 15, 700).
link(lifeSciences, briggsHall, 15, 700).
link(sciencesLectureHall, briggsHall, 15, 700).
link(sciencesLectureHall, mannLab, 15, 700).
link(sciencesLectureHall, kleiberHall, 15, 700).
link(sciencesLectureHall, studentCenter, 5, 2500).
link(studentCenter, sciencesLectureHall, 5, 2500).
link(lifeSciences, studentCenter, 5, 2500).
link(studentCenter, lifeSciences, 5, 2500).
link(briggsHall, studentCenter, 5, 2500).
link(studentCenter, briggsHall, 5, 2500).
