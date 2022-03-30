bwTh(0.1).

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
node(cloud, [ubuntu, mySQL, python], (8, 16, 600), [encryption, auth], []).
node(ap1, [python, mySQL], (3, 6, 512), [encryption, auth], []).
node(ap2, [ubuntu], (3, 8, 256), [encryption, auth], [accell20]).
node(edge1, [python, ubuntu], (2.4, 4, 128), [encryption], [video3, relay4]).
node(edge2, [python, mySQL], (3, 6, 128), [encryption, auth], [wht42, loc38]).
link(cloud, ap1, 20, 1000).
link(ap1, cloud, 20, 1000).
link(ap1, ap2, 10, 500).
link(ap2, ap1, 10, 500).
link(ap1, edge1, 15, 800).
link(edge1, ap1, 15, 800).
link(ap2, edge1, 20, 1000).
link(edge1, ap2, 20, 1000).
link(ap1, edge2, 10, 700).
link(edge2, ap1, 10, 700).
