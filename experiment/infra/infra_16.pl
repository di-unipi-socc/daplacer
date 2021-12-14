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

node(smartphone0, [ubuntu, python], (2.4, 4, 32), [encryption, auth], [wht42, loc38]).
node(smartphone1, [ubuntu, python], (2.4, 4, 32), [encryption, auth], [accell20]).
node(smartphone2, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone3, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone4, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(accesspoint0, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], [video3, relay4]).
node(accesspoint1, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(accesspoint2, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(accesspoint3, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(accesspoint4, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(cabinet0, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet1, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet2, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(isp0, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp1, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp2, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(cloud0, [ubuntu, mySQL, python], (100, 64, 10000), [encryption, auth], []).

link(cabinet0, isp0, 5, 1000).
link(isp0, cabinet0, 5, 1000).
link(cabinet0, smartphone0, 5, 1000).
link(smartphone0, cabinet0, 5, 1000).
link(cabinet0, accesspoint0, 5, 1000).
link(accesspoint0, cabinet0, 5, 1000).
link(cabinet0, cabinet1, 5, 1000).
link(cabinet1, cabinet0, 5, 1000).
link(cabinet0, accesspoint1, 5, 1000).
link(accesspoint1, cabinet0, 5, 1000).
link(cabinet0, smartphone1, 5, 1000).
link(smartphone1, cabinet0, 5, 1000).
link(cabinet0, smartphone2, 5, 1000).
link(smartphone2, cabinet0, 5, 1000).
link(cabinet0, isp1, 5, 1000).
link(isp1, cabinet0, 5, 1000).
link(cabinet0, isp2, 5, 1000).
link(isp2, cabinet0, 5, 1000).
link(cabinet0, smartphone4, 5, 1000).
link(smartphone4, cabinet0, 5, 1000).
link(isp0, accesspoint1, 5, 1000).
link(accesspoint1, isp0, 5, 1000).
link(isp0, smartphone1, 5, 1000).
link(smartphone1, isp0, 5, 1000).
link(isp0, smartphone2, 5, 1000).
link(smartphone2, isp0, 5, 1000).
link(isp0, accesspoint4, 5, 1000).
link(accesspoint4, isp0, 5, 1000).
link(smartphone0, accesspoint1, 5, 1000).
link(accesspoint1, smartphone0, 5, 1000).
link(smartphone0, smartphone2, 5, 1000).
link(smartphone2, smartphone0, 5, 1000).
link(smartphone0, isp1, 5, 1000).
link(isp1, smartphone0, 5, 1000).
link(smartphone0, cabinet2, 5, 1000).
link(cabinet2, smartphone0, 5, 1000).
link(smartphone0, accesspoint2, 5, 1000).
link(accesspoint2, smartphone0, 5, 1000).
link(accesspoint0, isp1, 5, 1000).
link(isp1, accesspoint0, 5, 1000).
link(accesspoint0, isp2, 5, 1000).
link(isp2, accesspoint0, 5, 1000).
link(accesspoint0, cabinet2, 5, 1000).
link(cabinet2, accesspoint0, 5, 1000).
link(accesspoint0, accesspoint2, 5, 1000).
link(accesspoint2, accesspoint0, 5, 1000).
link(accesspoint0, smartphone3, 5, 1000).
link(smartphone3, accesspoint0, 5, 1000).
link(cabinet1, accesspoint1, 5, 1000).
link(accesspoint1, cabinet1, 5, 1000).
link(cabinet1, smartphone1, 5, 1000).
link(smartphone1, cabinet1, 5, 1000).
link(cabinet1, accesspoint3, 5, 1000).
link(accesspoint3, cabinet1, 5, 1000).
link(accesspoint1, smartphone1, 5, 1000).
link(smartphone1, accesspoint1, 5, 1000).
link(accesspoint1, isp1, 5, 1000).
link(isp1, accesspoint1, 5, 1000).
link(accesspoint1, cabinet2, 5, 1000).
link(cabinet2, accesspoint1, 5, 1000).
link(accesspoint1, accesspoint3, 5, 1000).
link(accesspoint3, accesspoint1, 5, 1000).
link(accesspoint1, smartphone3, 5, 1000).
link(smartphone3, accesspoint1, 5, 1000).
link(accesspoint1, accesspoint4, 5, 1000).
link(accesspoint4, accesspoint1, 5, 1000).
link(smartphone1, smartphone2, 5, 1000).
link(smartphone2, smartphone1, 5, 1000).
link(smartphone1, cabinet2, 5, 1000).
link(cabinet2, smartphone1, 5, 1000).
link(smartphone1, accesspoint2, 5, 1000).
link(accesspoint2, smartphone1, 5, 1000).
link(smartphone1, smartphone4, 5, 1000).
link(smartphone4, smartphone1, 5, 1000).
link(smartphone2, isp2, 5, 1000).
link(isp2, smartphone2, 5, 1000).
link(smartphone2, smartphone3, 5, 1000).
link(smartphone3, smartphone2, 5, 1000).
link(isp1, isp2, 5, 1000).
link(isp2, isp1, 5, 1000).
link(isp1, accesspoint2, 5, 1000).
link(accesspoint2, isp1, 5, 1000).
link(isp1, accesspoint3, 5, 1000).
link(accesspoint3, isp1, 5, 1000).
link(isp1, accesspoint4, 5, 1000).
link(accesspoint4, isp1, 5, 1000).
link(isp2, accesspoint4, 5, 1000).
link(accesspoint4, isp2, 5, 1000).
link(cabinet2, accesspoint3, 5, 1000).
link(accesspoint3, cabinet2, 5, 1000).
link(accesspoint3, smartphone3, 5, 1000).
link(smartphone3, accesspoint3, 5, 1000).
link(accesspoint3, smartphone4, 5, 1000).
link(smartphone4, accesspoint3, 5, 1000).
link(smartphone3, smartphone4, 5, 1000).
link(smartphone4, smartphone3, 5, 1000).

