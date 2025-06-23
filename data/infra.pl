bwTh(20).

dataBinding(interface, rCam, cam20).
dataBinding(interface, rVid, video3).
dataBinding(dataStorage, rVst, vst38).
dataBinding(dataStorage, rArt, art42).
dataBinding(controller, rGls, glass4).
dataBinding(controller, rDor, door27).

sensor(art42, heat, [artStats]).
sensor(vst38, smartphone, [visitorStats, videoStream]).
sensor(cam20, camera, [videoStream]).
actuator(video3, display).
actuator(door27, smartdoor).
actuator(glass4, smartphone).

node(parkingServices, [python, mySQL], (2.4, 2, 16), [encryption, auth], [door27]).
node(westEntry, [ubuntu], (2.4, 2, 32), [encryption], [video3]).
node(kleiberHall, [ubuntu, mySQL], (2.4, 3, 50), [], [art42]).
node(hoaglandAnnex, [ubuntu], (2.4, 6, 128), [auth], [cam20]).
node(briggsHall, [ubuntu, mySQL], (3, 6, 128), [auth], []).
node(mannLab, [ubuntu, python], (3, 6, 256), [encryption, auth], []).
node(lifeSciences, [python, mySQL], (3, 6, 256), [encryption, auth], []).
node(sciencesLectureHall, [ubuntu, mySQL], (3, 6, 256), [encryption, auth], [vst38]).
node(firePolice, [ubuntu, mySQL, python], (4, 8, 512), [encryption, auth], []).
node(studentCenter, [ubuntu, mySQL, python], (4, 8, 512), [encryption, auth], [glass4]).
node(isp, [ubuntu, mySQL], (5, 16, 600), [encryption, auth], []).
node(cloud, [ubuntu, mySQL, python], (6, 32, 10000), [encryption, auth], []).

nodeCost(parkingServices, 2.0).
nodeCost(westEntry, 1.5).
nodeCost(kleiberHall, 1.8).
nodeCost(hoaglandAnnex, 2.2).
nodeCost(briggsHall, 2.5).
nodeCost(mannLab, 2.8).
nodeCost(lifeSciences, 3.0).
nodeCost(sciencesLectureHall, 3.2).
nodeCost(firePolice, 3.5).
nodeCost(studentCenter, 3.8).
nodeCost(isp, 5.0).
nodeCost(cloud, 8.0).

nodeCI(parkingServices, 0.10).
nodeCI(westEntry, 0.08).
nodeCI(kleiberHall, 0.09).
nodeCI(hoaglandAnnex, 0.12).
nodeCI(briggsHall, 0.13).
nodeCI(mannLab, 0.15).
nodeCI(lifeSciences, 0.17).
nodeCI(sciencesLectureHall, 0.18).
nodeCI(firePolice, 0.20).
nodeCI(studentCenter, 0.22).
nodeCI(isp, 0.30).
nodeCI(cloud, 0.50).

link(isp, firePolice, 10, 80).
link(firePolice, isp, 10, 80).
link(isp, studentCenter, 10, 1000).
link(studentCenter, isp, 10, 1000).


link(isp, cloud, 50, 10000).
link(cloud, isp, 50, 10000).

link(parkingServices, westEntry, 15, 70).
link(parkingServices, lifeSciences, 15, 70).
link(parkingServices, mannLab, 15, 70).

link(westEntry, parkingServices, 15, 70).
link(westEntry, mannLab, 15, 70).
link(westEntry, firePolice, 15, 70).

link(firePolice, westEntry, 15, 70).
link(firePolice, mannLab, 15, 70).
link(firePolice, kleiberHall, 15, 70).
link(firePolice, hoaglandAnnex, 15, 70).

link(mannLab, parkingServices, 15, 70).
link(mannLab, westEntry, 15, 70).
link(mannLab, firePolice, 15, 70).
link(mannLab, lifeSciences, 15, 70).
link(mannLab, briggsHall, 15, 70).
link(mannLab, sciencesLectureHall, 15, 70).
link(mannLab, kleiberHall, 15, 70).
link(mannLab, hoaglandAnnex, 15, 70).

link(hoaglandAnnex, mannLab, 15, 70).
link(hoaglandAnnex, firePolice, 15, 70).
link(hoaglandAnnex, kleiberHall, 15, 70).

link(kleiberHall, hoaglandAnnex, 15, 70).
link(kleiberHall, mannLab, 15, 70).
link(kleiberHall, briggsHall, 15, 70).
link(kleiberHall, firePolice, 15, 70).
link(kleiberHall, sciencesLectureHall, 15, 70).

link(briggsHall, mannLab, 15, 70).
link(briggsHall, lifeSciences, 15, 70).
link(briggsHall, kleiberHall, 15, 70).
link(briggsHall, sciencesLectureHall, 15, 70).


link(lifeSciences, parkingServices, 15, 70).
link(lifeSciences, mannLab, 15, 70).
link(lifeSciences, briggsHall, 15, 70).


link(sciencesLectureHall, briggsHall, 15, 70).
link(sciencesLectureHall, mannLab, 15, 70).
link(sciencesLectureHall, kleiberHall, 15, 70).

% wired edge-edge

link(sciencesLectureHall, studentCenter, 5, 250).
link(studentCenter, sciencesLectureHall, 5, 250).

link(lifeSciences, studentCenter, 5, 250).
link(studentCenter, lifeSciences, 5, 250).
link(briggsHall, studentCenter, 5, 250).
link(studentCenter, briggsHall, 5, 250).