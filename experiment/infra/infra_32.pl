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
node(smartphone5, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone6, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone7, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone8, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone9, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone10, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone11, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone12, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone13, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone14, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone15, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone16, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone17, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(accesspoint0, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], [video3, relay4]).
node(accesspoint1, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(accesspoint2, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(accesspoint3, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(accesspoint4, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(accesspoint5, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(accesspoint6, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(cabinet0, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet1, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(isp0, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp1, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp2, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp3, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp4, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(cloud0, [ubuntu, mySQL, python], (100, 64, 10000), [encryption, auth], []).
node(cloud1, [ubuntu, mySQL, python], (100, 64, 10000), [encryption, auth], []).

link(smartphone0, smartphone1, 5, 1000).
link(smartphone1, smartphone0, 5, 1000).
link(smartphone0, smartphone2, 5, 1000).
link(smartphone2, smartphone0, 5, 1000).
link(smartphone0, smartphone3, 5, 1000).
link(smartphone3, smartphone0, 5, 1000).
link(smartphone0, smartphone4, 5, 1000).
link(smartphone4, smartphone0, 5, 1000).
link(smartphone0, isp0, 5, 1000).
link(isp0, smartphone0, 5, 1000).
link(smartphone0, accesspoint0, 5, 1000).
link(accesspoint0, smartphone0, 5, 1000).
link(smartphone0, isp1, 5, 1000).
link(isp1, smartphone0, 5, 1000).
link(smartphone0, smartphone5, 5, 1000).
link(smartphone5, smartphone0, 5, 1000).
link(smartphone0, smartphone6, 5, 1000).
link(smartphone6, smartphone0, 5, 1000).
link(smartphone0, smartphone7, 5, 1000).
link(smartphone7, smartphone0, 5, 1000).
link(smartphone0, cabinet0, 5, 1000).
link(cabinet0, smartphone0, 5, 1000).
link(smartphone0, accesspoint2, 5, 1000).
link(accesspoint2, smartphone0, 5, 1000).
link(smartphone0, smartphone9, 5, 1000).
link(smartphone9, smartphone0, 5, 1000).
link(smartphone0, smartphone11, 5, 1000).
link(smartphone11, smartphone0, 5, 1000).
link(smartphone0, cabinet1, 5, 1000).
link(cabinet1, smartphone0, 5, 1000).
link(smartphone0, accesspoint3, 5, 1000).
link(accesspoint3, smartphone0, 5, 1000).
link(smartphone0, smartphone12, 5, 1000).
link(smartphone12, smartphone0, 5, 1000).
link(smartphone0, smartphone14, 5, 1000).
link(smartphone14, smartphone0, 5, 1000).
link(smartphone0, smartphone15, 5, 1000).
link(smartphone15, smartphone0, 5, 1000).
link(smartphone0, accesspoint6, 5, 1000).
link(accesspoint6, smartphone0, 5, 1000).
link(smartphone1, accesspoint0, 5, 1000).
link(accesspoint0, smartphone1, 5, 1000).
link(smartphone1, isp1, 5, 1000).
link(isp1, smartphone1, 5, 1000).
link(smartphone1, smartphone5, 5, 1000).
link(smartphone5, smartphone1, 5, 1000).
link(smartphone1, smartphone6, 5, 1000).
link(smartphone6, smartphone1, 5, 1000).
link(smartphone1, smartphone7, 5, 1000).
link(smartphone7, smartphone1, 5, 1000).
link(smartphone1, smartphone8, 5, 1000).
link(smartphone8, smartphone1, 5, 1000).
link(smartphone1, accesspoint1, 5, 1000).
link(accesspoint1, smartphone1, 5, 1000).
link(smartphone1, cabinet0, 5, 1000).
link(cabinet0, smartphone1, 5, 1000).
link(smartphone1, smartphone9, 5, 1000).
link(smartphone9, smartphone1, 5, 1000).
link(smartphone1, smartphone10, 5, 1000).
link(smartphone10, smartphone1, 5, 1000).
link(smartphone1, smartphone11, 5, 1000).
link(smartphone11, smartphone1, 5, 1000).
link(smartphone1, cabinet1, 5, 1000).
link(cabinet1, smartphone1, 5, 1000).
link(smartphone1, accesspoint3, 5, 1000).
link(accesspoint3, smartphone1, 5, 1000).
link(smartphone1, smartphone12, 5, 1000).
link(smartphone12, smartphone1, 5, 1000).
link(smartphone1, isp4, 5, 1000).
link(isp4, smartphone1, 5, 1000).
link(smartphone1, smartphone13, 5, 1000).
link(smartphone13, smartphone1, 5, 1000).
link(smartphone1, accesspoint5, 5, 1000).
link(accesspoint5, smartphone1, 5, 1000).
link(smartphone1, accesspoint6, 5, 1000).
link(accesspoint6, smartphone1, 5, 1000).
link(smartphone2, isp1, 5, 1000).
link(isp1, smartphone2, 5, 1000).
link(smartphone2, smartphone5, 5, 1000).
link(smartphone5, smartphone2, 5, 1000).
link(smartphone2, smartphone7, 5, 1000).
link(smartphone7, smartphone2, 5, 1000).
link(smartphone2, accesspoint1, 5, 1000).
link(accesspoint1, smartphone2, 5, 1000).
link(smartphone2, accesspoint2, 5, 1000).
link(accesspoint2, smartphone2, 5, 1000).
link(smartphone2, isp3, 5, 1000).
link(isp3, smartphone2, 5, 1000).
link(smartphone2, smartphone10, 5, 1000).
link(smartphone10, smartphone2, 5, 1000).
link(smartphone2, isp4, 5, 1000).
link(isp4, smartphone2, 5, 1000).
link(smartphone3, accesspoint0, 5, 1000).
link(accesspoint0, smartphone3, 5, 1000).
link(smartphone4, accesspoint0, 5, 1000).
link(accesspoint0, smartphone4, 5, 1000).
link(smartphone4, isp1, 5, 1000).
link(isp1, smartphone4, 5, 1000).
link(smartphone4, isp2, 5, 1000).
link(isp2, smartphone4, 5, 1000).
link(smartphone4, isp3, 5, 1000).
link(isp3, smartphone4, 5, 1000).
link(smartphone4, smartphone12, 5, 1000).
link(smartphone12, smartphone4, 5, 1000).
link(smartphone4, accesspoint4, 5, 1000).
link(accesspoint4, smartphone4, 5, 1000).
link(isp0, accesspoint0, 5, 1000).
link(accesspoint0, isp0, 5, 1000).
link(isp0, smartphone8, 5, 1000).
link(smartphone8, isp0, 5, 1000).
link(isp0, accesspoint2, 5, 1000).
link(accesspoint2, isp0, 5, 1000).
link(isp0, smartphone9, 5, 1000).
link(smartphone9, isp0, 5, 1000).
link(isp0, accesspoint3, 5, 1000).
link(accesspoint3, isp0, 5, 1000).
link(isp0, isp4, 5, 1000).
link(isp4, isp0, 5, 1000).
link(isp0, accesspoint5, 5, 1000).
link(accesspoint5, isp0, 5, 1000).
link(isp0, smartphone16, 5, 1000).
link(smartphone16, isp0, 5, 1000).
link(accesspoint0, isp1, 5, 1000).
link(isp1, accesspoint0, 5, 1000).
link(accesspoint0, smartphone5, 5, 1000).
link(smartphone5, accesspoint0, 5, 1000).
link(accesspoint0, smartphone6, 5, 1000).
link(smartphone6, accesspoint0, 5, 1000).
link(accesspoint0, smartphone7, 5, 1000).
link(smartphone7, accesspoint0, 5, 1000).
link(accesspoint0, isp2, 5, 1000).
link(isp2, accesspoint0, 5, 1000).
link(accesspoint0, isp3, 5, 1000).
link(isp3, accesspoint0, 5, 1000).
link(accesspoint0, smartphone11, 5, 1000).
link(smartphone11, accesspoint0, 5, 1000).
link(accesspoint0, smartphone12, 5, 1000).
link(smartphone12, accesspoint0, 5, 1000).
link(accesspoint0, isp4, 5, 1000).
link(isp4, accesspoint0, 5, 1000).
link(accesspoint0, accesspoint4, 5, 1000).
link(accesspoint4, accesspoint0, 5, 1000).
link(accesspoint0, smartphone15, 5, 1000).
link(smartphone15, accesspoint0, 5, 1000).
link(isp1, smartphone5, 5, 1000).
link(smartphone5, isp1, 5, 1000).
link(isp1, smartphone6, 5, 1000).
link(smartphone6, isp1, 5, 1000).
link(isp1, accesspoint1, 5, 1000).
link(accesspoint1, isp1, 5, 1000).
link(isp1, accesspoint2, 5, 1000).
link(accesspoint2, isp1, 5, 1000).
link(isp1, smartphone9, 5, 1000).
link(smartphone9, isp1, 5, 1000).
link(isp1, accesspoint4, 5, 1000).
link(accesspoint4, isp1, 5, 1000).
link(isp1, smartphone15, 5, 1000).
link(smartphone15, isp1, 5, 1000).
link(smartphone5, smartphone6, 5, 1000).
link(smartphone6, smartphone5, 5, 1000).
link(smartphone5, isp2, 5, 1000).
link(isp2, smartphone5, 5, 1000).
link(smartphone5, smartphone8, 5, 1000).
link(smartphone8, smartphone5, 5, 1000).
link(smartphone5, accesspoint1, 5, 1000).
link(accesspoint1, smartphone5, 5, 1000).
link(smartphone5, cabinet0, 5, 1000).
link(cabinet0, smartphone5, 5, 1000).
link(smartphone5, smartphone17, 5, 1000).
link(smartphone17, smartphone5, 5, 1000).
link(smartphone6, smartphone7, 5, 1000).
link(smartphone7, smartphone6, 5, 1000).
link(smartphone6, isp2, 5, 1000).
link(isp2, smartphone6, 5, 1000).
link(smartphone6, smartphone8, 5, 1000).
link(smartphone8, smartphone6, 5, 1000).
link(smartphone6, accesspoint1, 5, 1000).
link(accesspoint1, smartphone6, 5, 1000).
link(smartphone6, cabinet0, 5, 1000).
link(cabinet0, smartphone6, 5, 1000).
link(smartphone6, smartphone9, 5, 1000).
link(smartphone9, smartphone6, 5, 1000).
link(smartphone6, isp3, 5, 1000).
link(isp3, smartphone6, 5, 1000).
link(smartphone6, smartphone10, 5, 1000).
link(smartphone10, smartphone6, 5, 1000).
link(smartphone6, smartphone11, 5, 1000).
link(smartphone11, smartphone6, 5, 1000).
link(smartphone6, cabinet1, 5, 1000).
link(cabinet1, smartphone6, 5, 1000).
link(smartphone6, accesspoint4, 5, 1000).
link(accesspoint4, smartphone6, 5, 1000).
link(smartphone6, accesspoint5, 5, 1000).
link(accesspoint5, smartphone6, 5, 1000).
link(smartphone7, isp2, 5, 1000).
link(isp2, smartphone7, 5, 1000).
link(smartphone7, accesspoint2, 5, 1000).
link(accesspoint2, smartphone7, 5, 1000).
link(smartphone7, smartphone10, 5, 1000).
link(smartphone10, smartphone7, 5, 1000).
link(smartphone7, smartphone11, 5, 1000).
link(smartphone11, smartphone7, 5, 1000).
link(smartphone7, isp4, 5, 1000).
link(isp4, smartphone7, 5, 1000).
link(smartphone7, smartphone13, 5, 1000).
link(smartphone13, smartphone7, 5, 1000).
link(isp2, smartphone8, 5, 1000).
link(smartphone8, isp2, 5, 1000).
link(isp2, cabinet0, 5, 1000).
link(cabinet0, isp2, 5, 1000).
link(isp2, accesspoint4, 5, 1000).
link(accesspoint4, isp2, 5, 1000).
link(isp2, smartphone14, 5, 1000).
link(smartphone14, isp2, 5, 1000).
link(isp2, accesspoint5, 5, 1000).
link(accesspoint5, isp2, 5, 1000).
link(smartphone8, accesspoint3, 5, 1000).
link(accesspoint3, smartphone8, 5, 1000).
link(smartphone8, smartphone13, 5, 1000).
link(smartphone13, smartphone8, 5, 1000).
link(accesspoint1, cabinet1, 5, 1000).
link(cabinet1, accesspoint1, 5, 1000).
link(accesspoint1, accesspoint3, 5, 1000).
link(accesspoint3, accesspoint1, 5, 1000).
link(accesspoint1, smartphone17, 5, 1000).
link(smartphone17, accesspoint1, 5, 1000).
link(cabinet0, isp3, 5, 1000).
link(isp3, cabinet0, 5, 1000).
link(cabinet0, smartphone10, 5, 1000).
link(smartphone10, cabinet0, 5, 1000).
link(cabinet0, cabinet1, 5, 1000).
link(cabinet1, cabinet0, 5, 1000).
link(cabinet0, smartphone14, 5, 1000).
link(smartphone14, cabinet0, 5, 1000).
link(cabinet0, smartphone17, 5, 1000).
link(smartphone17, cabinet0, 5, 1000).
link(accesspoint2, smartphone12, 5, 1000).
link(smartphone12, accesspoint2, 5, 1000).
link(accesspoint2, smartphone17, 5, 1000).
link(smartphone17, accesspoint2, 5, 1000).
link(smartphone9, smartphone14, 5, 1000).
link(smartphone14, smartphone9, 5, 1000).
link(smartphone9, accesspoint5, 5, 1000).
link(accesspoint5, smartphone9, 5, 1000).
link(isp3, smartphone13, 5, 1000).
link(smartphone13, isp3, 5, 1000).
link(isp3, smartphone15, 5, 1000).
link(smartphone15, isp3, 5, 1000).
link(smartphone11, accesspoint6, 5, 1000).
link(accesspoint6, smartphone11, 5, 1000).
link(cabinet1, smartphone14, 5, 1000).
link(smartphone14, cabinet1, 5, 1000).
link(cabinet1, smartphone15, 5, 1000).
link(smartphone15, cabinet1, 5, 1000).
link(cabinet1, smartphone16, 5, 1000).
link(smartphone16, cabinet1, 5, 1000).
link(isp4, smartphone13, 5, 1000).
link(smartphone13, isp4, 5, 1000).
link(isp4, smartphone16, 5, 1000).
link(smartphone16, isp4, 5, 1000).
link(isp4, accesspoint6, 5, 1000).
link(accesspoint6, isp4, 5, 1000).
link(smartphone13, smartphone16, 5, 1000).
link(smartphone16, smartphone13, 5, 1000).
link(smartphone14, smartphone17, 5, 1000).
link(smartphone17, smartphone14, 5, 1000).
link(smartphone14, accesspoint6, 5, 1000).
link(accesspoint6, smartphone14, 5, 1000).
link(accesspoint5, smartphone16, 5, 1000).
link(smartphone16, accesspoint5, 5, 1000).

