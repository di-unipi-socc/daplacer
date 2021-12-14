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
node(smartphone18, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone19, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone20, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone21, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone22, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone23, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone24, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone25, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone26, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone27, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone28, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(smartphone29, [ubuntu, python], (2.4, 4, 32), [encryption, auth], []).
node(accesspoint0, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], [video3, relay4]).
node(accesspoint1, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(accesspoint2, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(accesspoint3, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(accesspoint4, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(accesspoint5, [ubuntu, mySQL], (3, 6, 128), [encryption, auth], []).
node(cabinet0, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet1, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet2, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet3, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet4, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet5, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet6, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet7, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet8, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet9, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet10, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet11, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet12, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet13, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet14, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet15, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(cabinet16, [python, mySQL], (4, 8, 512), [encryption, auth], []).
node(isp0, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp1, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp2, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp3, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp4, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp5, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp6, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp7, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp8, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp9, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(isp10, [ubuntu, mySQL, python], (5, 16, 600), [encryption, auth], []).
node(cloud0, [ubuntu, mySQL, python], (100, 64, 10000), [encryption, auth], []).
node(cloud1, [ubuntu, mySQL, python], (100, 64, 10000), [encryption, auth], []).
node(cloud2, [ubuntu, mySQL, python], (100, 64, 10000), [encryption, auth], []).

link(smartphone0, cabinet0, 5, 1000).
link(cabinet0, smartphone0, 5, 1000).
link(smartphone0, isp0, 5, 1000).
link(isp0, smartphone0, 5, 1000).
link(smartphone0, cabinet1, 5, 1000).
link(cabinet1, smartphone0, 5, 1000).
link(smartphone0, cabinet2, 5, 1000).
link(cabinet2, smartphone0, 5, 1000).
link(smartphone0, smartphone1, 5, 1000).
link(smartphone1, smartphone0, 5, 1000).
link(smartphone0, cabinet3, 5, 1000).
link(cabinet3, smartphone0, 5, 1000).
link(smartphone0, smartphone2, 5, 1000).
link(smartphone2, smartphone0, 5, 1000).
link(smartphone0, smartphone3, 5, 1000).
link(smartphone3, smartphone0, 5, 1000).
link(smartphone0, smartphone4, 5, 1000).
link(smartphone4, smartphone0, 5, 1000).
link(smartphone0, smartphone5, 5, 1000).
link(smartphone5, smartphone0, 5, 1000).
link(smartphone0, smartphone6, 5, 1000).
link(smartphone6, smartphone0, 5, 1000).
link(smartphone0, cabinet4, 5, 1000).
link(cabinet4, smartphone0, 5, 1000).
link(smartphone0, smartphone8, 5, 1000).
link(smartphone8, smartphone0, 5, 1000).
link(smartphone0, smartphone10, 5, 1000).
link(smartphone10, smartphone0, 5, 1000).
link(smartphone0, accesspoint1, 5, 1000).
link(accesspoint1, smartphone0, 5, 1000).
link(smartphone0, smartphone14, 5, 1000).
link(smartphone14, smartphone0, 5, 1000).
link(smartphone0, isp1, 5, 1000).
link(isp1, smartphone0, 5, 1000).
link(smartphone0, isp3, 5, 1000).
link(isp3, smartphone0, 5, 1000).
link(smartphone0, isp4, 5, 1000).
link(isp4, smartphone0, 5, 1000).
link(smartphone0, accesspoint3, 5, 1000).
link(accesspoint3, smartphone0, 5, 1000).
link(smartphone0, cabinet6, 5, 1000).
link(cabinet6, smartphone0, 5, 1000).
link(smartphone0, isp5, 5, 1000).
link(isp5, smartphone0, 5, 1000).
link(smartphone0, isp6, 5, 1000).
link(isp6, smartphone0, 5, 1000).
link(smartphone0, smartphone18, 5, 1000).
link(smartphone18, smartphone0, 5, 1000).
link(smartphone0, cabinet7, 5, 1000).
link(cabinet7, smartphone0, 5, 1000).
link(smartphone0, smartphone19, 5, 1000).
link(smartphone19, smartphone0, 5, 1000).
link(smartphone0, smartphone21, 5, 1000).
link(smartphone21, smartphone0, 5, 1000).
link(smartphone0, smartphone22, 5, 1000).
link(smartphone22, smartphone0, 5, 1000).
link(smartphone0, smartphone23, 5, 1000).
link(smartphone23, smartphone0, 5, 1000).
link(smartphone0, cabinet15, 5, 1000).
link(cabinet15, smartphone0, 5, 1000).
link(smartphone0, cabinet16, 5, 1000).
link(cabinet16, smartphone0, 5, 1000).
link(cabinet0, smartphone2, 5, 1000).
link(smartphone2, cabinet0, 5, 1000).
link(cabinet0, smartphone4, 5, 1000).
link(smartphone4, cabinet0, 5, 1000).
link(cabinet0, smartphone7, 5, 1000).
link(smartphone7, cabinet0, 5, 1000).
link(cabinet0, accesspoint0, 5, 1000).
link(accesspoint0, cabinet0, 5, 1000).
link(cabinet0, smartphone13, 5, 1000).
link(smartphone13, cabinet0, 5, 1000).
link(cabinet0, smartphone16, 5, 1000).
link(smartphone16, cabinet0, 5, 1000).
link(cabinet0, accesspoint3, 5, 1000).
link(accesspoint3, cabinet0, 5, 1000).
link(cabinet0, cabinet9, 5, 1000).
link(cabinet9, cabinet0, 5, 1000).
link(cabinet0, smartphone20, 5, 1000).
link(smartphone20, cabinet0, 5, 1000).
link(cabinet0, smartphone21, 5, 1000).
link(smartphone21, cabinet0, 5, 1000).
link(cabinet0, accesspoint5, 5, 1000).
link(accesspoint5, cabinet0, 5, 1000).
link(cabinet0, cabinet16, 5, 1000).
link(cabinet16, cabinet0, 5, 1000).
link(isp0, smartphone3, 5, 1000).
link(smartphone3, isp0, 5, 1000).
link(isp0, smartphone5, 5, 1000).
link(smartphone5, isp0, 5, 1000).
link(isp0, cabinet4, 5, 1000).
link(cabinet4, isp0, 5, 1000).
link(isp0, smartphone7, 5, 1000).
link(smartphone7, isp0, 5, 1000).
link(isp0, accesspoint1, 5, 1000).
link(accesspoint1, isp0, 5, 1000).
link(isp0, isp1, 5, 1000).
link(isp1, isp0, 5, 1000).
link(isp0, isp5, 5, 1000).
link(isp5, isp0, 5, 1000).
link(isp0, cabinet7, 5, 1000).
link(cabinet7, isp0, 5, 1000).
link(isp0, cabinet8, 5, 1000).
link(cabinet8, isp0, 5, 1000).
link(isp0, cabinet12, 5, 1000).
link(cabinet12, isp0, 5, 1000).
link(isp0, isp10, 5, 1000).
link(isp10, isp0, 5, 1000).
link(cabinet1, smartphone2, 5, 1000).
link(smartphone2, cabinet1, 5, 1000).
link(cabinet1, smartphone4, 5, 1000).
link(smartphone4, cabinet1, 5, 1000).
link(cabinet1, smartphone5, 5, 1000).
link(smartphone5, cabinet1, 5, 1000).
link(cabinet1, accesspoint1, 5, 1000).
link(accesspoint1, cabinet1, 5, 1000).
link(cabinet1, isp9, 5, 1000).
link(isp9, cabinet1, 5, 1000).
link(cabinet1, smartphone23, 5, 1000).
link(smartphone23, cabinet1, 5, 1000).
link(cabinet1, smartphone27, 5, 1000).
link(smartphone27, cabinet1, 5, 1000).
link(cabinet2, smartphone2, 5, 1000).
link(smartphone2, cabinet2, 5, 1000).
link(cabinet2, smartphone3, 5, 1000).
link(smartphone3, cabinet2, 5, 1000).
link(cabinet2, smartphone4, 5, 1000).
link(smartphone4, cabinet2, 5, 1000).
link(cabinet2, smartphone7, 5, 1000).
link(smartphone7, cabinet2, 5, 1000).
link(cabinet2, smartphone12, 5, 1000).
link(smartphone12, cabinet2, 5, 1000).
link(cabinet2, smartphone14, 5, 1000).
link(smartphone14, cabinet2, 5, 1000).
link(cabinet2, accesspoint2, 5, 1000).
link(accesspoint2, cabinet2, 5, 1000).
link(cabinet2, isp1, 5, 1000).
link(isp1, cabinet2, 5, 1000).
link(cabinet2, cabinet5, 5, 1000).
link(cabinet5, cabinet2, 5, 1000).
link(cabinet2, cabinet10, 5, 1000).
link(cabinet10, cabinet2, 5, 1000).
link(cabinet2, smartphone23, 5, 1000).
link(smartphone23, cabinet2, 5, 1000).
link(cabinet2, cabinet13, 5, 1000).
link(cabinet13, cabinet2, 5, 1000).
link(cabinet2, smartphone25, 5, 1000).
link(smartphone25, cabinet2, 5, 1000).
link(cabinet2, accesspoint4, 5, 1000).
link(accesspoint4, cabinet2, 5, 1000).
link(cabinet2, smartphone27, 5, 1000).
link(smartphone27, cabinet2, 5, 1000).
link(cabinet2, isp10, 5, 1000).
link(isp10, cabinet2, 5, 1000).
link(smartphone1, smartphone2, 5, 1000).
link(smartphone2, smartphone1, 5, 1000).
link(smartphone1, smartphone3, 5, 1000).
link(smartphone3, smartphone1, 5, 1000).
link(smartphone1, smartphone4, 5, 1000).
link(smartphone4, smartphone1, 5, 1000).
link(smartphone1, smartphone5, 5, 1000).
link(smartphone5, smartphone1, 5, 1000).
link(smartphone1, smartphone6, 5, 1000).
link(smartphone6, smartphone1, 5, 1000).
link(smartphone1, cabinet4, 5, 1000).
link(cabinet4, smartphone1, 5, 1000).
link(smartphone1, smartphone10, 5, 1000).
link(smartphone10, smartphone1, 5, 1000).
link(smartphone1, smartphone11, 5, 1000).
link(smartphone11, smartphone1, 5, 1000).
link(smartphone1, smartphone12, 5, 1000).
link(smartphone12, smartphone1, 5, 1000).
link(smartphone1, smartphone15, 5, 1000).
link(smartphone15, smartphone1, 5, 1000).
link(smartphone1, smartphone17, 5, 1000).
link(smartphone17, smartphone1, 5, 1000).
link(smartphone1, cabinet9, 5, 1000).
link(cabinet9, smartphone1, 5, 1000).
link(smartphone1, smartphone20, 5, 1000).
link(smartphone20, smartphone1, 5, 1000).
link(smartphone1, cabinet10, 5, 1000).
link(cabinet10, smartphone1, 5, 1000).
link(smartphone1, smartphone26, 5, 1000).
link(smartphone26, smartphone1, 5, 1000).
link(smartphone1, smartphone28, 5, 1000).
link(smartphone28, smartphone1, 5, 1000).
link(cabinet3, smartphone2, 5, 1000).
link(smartphone2, cabinet3, 5, 1000).
link(cabinet3, smartphone3, 5, 1000).
link(smartphone3, cabinet3, 5, 1000).
link(cabinet3, cabinet4, 5, 1000).
link(cabinet4, cabinet3, 5, 1000).
link(cabinet3, smartphone15, 5, 1000).
link(smartphone15, cabinet3, 5, 1000).
link(cabinet3, smartphone23, 5, 1000).
link(smartphone23, cabinet3, 5, 1000).
link(cabinet3, cabinet14, 5, 1000).
link(cabinet14, cabinet3, 5, 1000).
link(smartphone2, smartphone3, 5, 1000).
link(smartphone3, smartphone2, 5, 1000).
link(smartphone2, smartphone5, 5, 1000).
link(smartphone5, smartphone2, 5, 1000).
link(smartphone2, smartphone6, 5, 1000).
link(smartphone6, smartphone2, 5, 1000).
link(smartphone2, smartphone7, 5, 1000).
link(smartphone7, smartphone2, 5, 1000).
link(smartphone2, smartphone8, 5, 1000).
link(smartphone8, smartphone2, 5, 1000).
link(smartphone2, smartphone9, 5, 1000).
link(smartphone9, smartphone2, 5, 1000).
link(smartphone2, accesspoint2, 5, 1000).
link(accesspoint2, smartphone2, 5, 1000).
link(smartphone2, isp1, 5, 1000).
link(isp1, smartphone2, 5, 1000).
link(smartphone2, smartphone17, 5, 1000).
link(smartphone17, smartphone2, 5, 1000).
link(smartphone2, cabinet5, 5, 1000).
link(cabinet5, smartphone2, 5, 1000).
link(smartphone2, smartphone22, 5, 1000).
link(smartphone22, smartphone2, 5, 1000).
link(smartphone2, smartphone25, 5, 1000).
link(smartphone25, smartphone2, 5, 1000).
link(smartphone2, cabinet14, 5, 1000).
link(cabinet14, smartphone2, 5, 1000).
link(smartphone2, smartphone28, 5, 1000).
link(smartphone28, smartphone2, 5, 1000).
link(smartphone2, cabinet16, 5, 1000).
link(cabinet16, smartphone2, 5, 1000).
link(smartphone3, smartphone4, 5, 1000).
link(smartphone4, smartphone3, 5, 1000).
link(smartphone3, smartphone5, 5, 1000).
link(smartphone5, smartphone3, 5, 1000).
link(smartphone3, smartphone6, 5, 1000).
link(smartphone6, smartphone3, 5, 1000).
link(smartphone3, cabinet4, 5, 1000).
link(cabinet4, smartphone3, 5, 1000).
link(smartphone3, smartphone8, 5, 1000).
link(smartphone8, smartphone3, 5, 1000).
link(smartphone3, smartphone9, 5, 1000).
link(smartphone9, smartphone3, 5, 1000).
link(smartphone3, accesspoint0, 5, 1000).
link(accesspoint0, smartphone3, 5, 1000).
link(smartphone3, smartphone10, 5, 1000).
link(smartphone10, smartphone3, 5, 1000).
link(smartphone3, smartphone11, 5, 1000).
link(smartphone11, smartphone3, 5, 1000).
link(smartphone3, accesspoint1, 5, 1000).
link(accesspoint1, smartphone3, 5, 1000).
link(smartphone3, smartphone12, 5, 1000).
link(smartphone12, smartphone3, 5, 1000).
link(smartphone3, smartphone13, 5, 1000).
link(smartphone13, smartphone3, 5, 1000).
link(smartphone3, smartphone14, 5, 1000).
link(smartphone14, smartphone3, 5, 1000).
link(smartphone3, isp2, 5, 1000).
link(isp2, smartphone3, 5, 1000).
link(smartphone3, isp3, 5, 1000).
link(isp3, smartphone3, 5, 1000).
link(smartphone3, cabinet5, 5, 1000).
link(cabinet5, smartphone3, 5, 1000).
link(smartphone3, cabinet6, 5, 1000).
link(cabinet6, smartphone3, 5, 1000).
link(smartphone3, smartphone18, 5, 1000).
link(smartphone18, smartphone3, 5, 1000).
link(smartphone3, isp7, 5, 1000).
link(isp7, smartphone3, 5, 1000).
link(smartphone3, cabinet8, 5, 1000).
link(cabinet8, smartphone3, 5, 1000).
link(smartphone3, cabinet9, 5, 1000).
link(cabinet9, smartphone3, 5, 1000).
link(smartphone3, smartphone22, 5, 1000).
link(smartphone22, smartphone3, 5, 1000).
link(smartphone3, isp8, 5, 1000).
link(isp8, smartphone3, 5, 1000).
link(smartphone3, smartphone24, 5, 1000).
link(smartphone24, smartphone3, 5, 1000).
link(smartphone3, smartphone27, 5, 1000).
link(smartphone27, smartphone3, 5, 1000).
link(smartphone3, accesspoint5, 5, 1000).
link(accesspoint5, smartphone3, 5, 1000).
link(smartphone4, smartphone6, 5, 1000).
link(smartphone6, smartphone4, 5, 1000).
link(smartphone4, smartphone9, 5, 1000).
link(smartphone9, smartphone4, 5, 1000).
link(smartphone4, smartphone14, 5, 1000).
link(smartphone14, smartphone4, 5, 1000).
link(smartphone4, accesspoint2, 5, 1000).
link(accesspoint2, smartphone4, 5, 1000).
link(smartphone4, isp3, 5, 1000).
link(isp3, smartphone4, 5, 1000).
link(smartphone4, isp4, 5, 1000).
link(isp4, smartphone4, 5, 1000).
link(smartphone4, accesspoint3, 5, 1000).
link(accesspoint3, smartphone4, 5, 1000).
link(smartphone4, smartphone17, 5, 1000).
link(smartphone17, smartphone4, 5, 1000).
link(smartphone4, isp7, 5, 1000).
link(isp7, smartphone4, 5, 1000).
link(smartphone4, cabinet8, 5, 1000).
link(cabinet8, smartphone4, 5, 1000).
link(smartphone4, smartphone22, 5, 1000).
link(smartphone22, smartphone4, 5, 1000).
link(smartphone4, isp8, 5, 1000).
link(isp8, smartphone4, 5, 1000).
link(smartphone4, accesspoint4, 5, 1000).
link(accesspoint4, smartphone4, 5, 1000).
link(smartphone4, accesspoint5, 5, 1000).
link(accesspoint5, smartphone4, 5, 1000).
link(smartphone4, cabinet15, 5, 1000).
link(cabinet15, smartphone4, 5, 1000).
link(smartphone5, smartphone6, 5, 1000).
link(smartphone6, smartphone5, 5, 1000).
link(smartphone5, smartphone8, 5, 1000).
link(smartphone8, smartphone5, 5, 1000).
link(smartphone5, smartphone9, 5, 1000).
link(smartphone9, smartphone5, 5, 1000).
link(smartphone5, smartphone11, 5, 1000).
link(smartphone11, smartphone5, 5, 1000).
link(smartphone5, isp2, 5, 1000).
link(isp2, smartphone5, 5, 1000).
link(smartphone5, smartphone16, 5, 1000).
link(smartphone16, smartphone5, 5, 1000).
link(smartphone5, isp3, 5, 1000).
link(isp3, smartphone5, 5, 1000).
link(smartphone5, accesspoint3, 5, 1000).
link(accesspoint3, smartphone5, 5, 1000).
link(smartphone5, smartphone18, 5, 1000).
link(smartphone18, smartphone5, 5, 1000).
link(smartphone5, isp7, 5, 1000).
link(isp7, smartphone5, 5, 1000).
link(smartphone5, cabinet7, 5, 1000).
link(cabinet7, smartphone5, 5, 1000).
link(smartphone5, smartphone19, 5, 1000).
link(smartphone19, smartphone5, 5, 1000).
link(smartphone5, cabinet9, 5, 1000).
link(cabinet9, smartphone5, 5, 1000).
link(smartphone5, smartphone20, 5, 1000).
link(smartphone20, smartphone5, 5, 1000).
link(smartphone5, cabinet10, 5, 1000).
link(cabinet10, smartphone5, 5, 1000).
link(smartphone5, isp8, 5, 1000).
link(isp8, smartphone5, 5, 1000).
link(smartphone5, smartphone24, 5, 1000).
link(smartphone24, smartphone5, 5, 1000).
link(smartphone5, accesspoint4, 5, 1000).
link(accesspoint4, smartphone5, 5, 1000).
link(smartphone5, accesspoint5, 5, 1000).
link(accesspoint5, smartphone5, 5, 1000).
link(smartphone6, cabinet4, 5, 1000).
link(cabinet4, smartphone6, 5, 1000).
link(smartphone6, smartphone7, 5, 1000).
link(smartphone7, smartphone6, 5, 1000).
link(smartphone6, smartphone9, 5, 1000).
link(smartphone9, smartphone6, 5, 1000).
link(smartphone6, accesspoint0, 5, 1000).
link(accesspoint0, smartphone6, 5, 1000).
link(smartphone6, smartphone11, 5, 1000).
link(smartphone11, smartphone6, 5, 1000).
link(smartphone6, smartphone14, 5, 1000).
link(smartphone14, smartphone6, 5, 1000).
link(smartphone6, isp2, 5, 1000).
link(isp2, smartphone6, 5, 1000).
link(smartphone6, smartphone16, 5, 1000).
link(smartphone16, smartphone6, 5, 1000).
link(smartphone6, accesspoint3, 5, 1000).
link(accesspoint3, smartphone6, 5, 1000).
link(smartphone6, cabinet5, 5, 1000).
link(cabinet5, smartphone6, 5, 1000).
link(smartphone6, isp5, 5, 1000).
link(isp5, smartphone6, 5, 1000).
link(smartphone6, smartphone20, 5, 1000).
link(smartphone20, smartphone6, 5, 1000).
link(smartphone6, isp9, 5, 1000).
link(isp9, smartphone6, 5, 1000).
link(smartphone6, cabinet12, 5, 1000).
link(cabinet12, smartphone6, 5, 1000).
link(smartphone6, smartphone29, 5, 1000).
link(smartphone29, smartphone6, 5, 1000).
link(cabinet4, smartphone7, 5, 1000).
link(smartphone7, cabinet4, 5, 1000).
link(cabinet4, smartphone8, 5, 1000).
link(smartphone8, cabinet4, 5, 1000).
link(cabinet4, accesspoint0, 5, 1000).
link(accesspoint0, cabinet4, 5, 1000).
link(cabinet4, smartphone10, 5, 1000).
link(smartphone10, cabinet4, 5, 1000).
link(cabinet4, accesspoint1, 5, 1000).
link(accesspoint1, cabinet4, 5, 1000).
link(cabinet4, isp1, 5, 1000).
link(isp1, cabinet4, 5, 1000).
link(cabinet4, isp2, 5, 1000).
link(isp2, cabinet4, 5, 1000).
link(cabinet4, accesspoint3, 5, 1000).
link(accesspoint3, cabinet4, 5, 1000).
link(cabinet4, isp6, 5, 1000).
link(isp6, cabinet4, 5, 1000).
link(cabinet4, cabinet13, 5, 1000).
link(cabinet13, cabinet4, 5, 1000).
link(smartphone7, smartphone8, 5, 1000).
link(smartphone8, smartphone7, 5, 1000).
link(smartphone7, accesspoint0, 5, 1000).
link(accesspoint0, smartphone7, 5, 1000).
link(smartphone7, smartphone11, 5, 1000).
link(smartphone11, smartphone7, 5, 1000).
link(smartphone7, smartphone12, 5, 1000).
link(smartphone12, smartphone7, 5, 1000).
link(smartphone7, accesspoint2, 5, 1000).
link(accesspoint2, smartphone7, 5, 1000).
link(smartphone7, smartphone15, 5, 1000).
link(smartphone15, smartphone7, 5, 1000).
link(smartphone7, smartphone17, 5, 1000).
link(smartphone17, smartphone7, 5, 1000).
link(smartphone7, isp6, 5, 1000).
link(isp6, smartphone7, 5, 1000).
link(smartphone7, smartphone18, 5, 1000).
link(smartphone18, smartphone7, 5, 1000).
link(smartphone7, smartphone23, 5, 1000).
link(smartphone23, smartphone7, 5, 1000).
link(smartphone7, cabinet13, 5, 1000).
link(cabinet13, smartphone7, 5, 1000).
link(smartphone7, smartphone26, 5, 1000).
link(smartphone26, smartphone7, 5, 1000).
link(smartphone8, smartphone9, 5, 1000).
link(smartphone9, smartphone8, 5, 1000).
link(smartphone8, accesspoint0, 5, 1000).
link(accesspoint0, smartphone8, 5, 1000).
link(smartphone8, isp1, 5, 1000).
link(isp1, smartphone8, 5, 1000).
link(smartphone8, isp3, 5, 1000).
link(isp3, smartphone8, 5, 1000).
link(smartphone8, smartphone18, 5, 1000).
link(smartphone18, smartphone8, 5, 1000).
link(smartphone8, isp9, 5, 1000).
link(isp9, smartphone8, 5, 1000).
link(smartphone8, smartphone28, 5, 1000).
link(smartphone28, smartphone8, 5, 1000).
link(smartphone8, cabinet15, 5, 1000).
link(cabinet15, smartphone8, 5, 1000).
link(smartphone9, smartphone10, 5, 1000).
link(smartphone10, smartphone9, 5, 1000).
link(smartphone9, smartphone11, 5, 1000).
link(smartphone11, smartphone9, 5, 1000).
link(smartphone9, accesspoint1, 5, 1000).
link(accesspoint1, smartphone9, 5, 1000).
link(smartphone9, smartphone13, 5, 1000).
link(smartphone13, smartphone9, 5, 1000).
link(smartphone9, smartphone14, 5, 1000).
link(smartphone14, smartphone9, 5, 1000).
link(smartphone9, smartphone15, 5, 1000).
link(smartphone15, smartphone9, 5, 1000).
link(smartphone9, smartphone16, 5, 1000).
link(smartphone16, smartphone9, 5, 1000).
link(smartphone9, smartphone17, 5, 1000).
link(smartphone17, smartphone9, 5, 1000).
link(smartphone9, isp5, 5, 1000).
link(isp5, smartphone9, 5, 1000).
link(smartphone9, isp6, 5, 1000).
link(isp6, smartphone9, 5, 1000).
link(smartphone9, smartphone19, 5, 1000).
link(smartphone19, smartphone9, 5, 1000).
link(smartphone9, isp9, 5, 1000).
link(isp9, smartphone9, 5, 1000).
link(smartphone9, cabinet13, 5, 1000).
link(cabinet13, smartphone9, 5, 1000).
link(smartphone9, smartphone24, 5, 1000).
link(smartphone24, smartphone9, 5, 1000).
link(smartphone9, smartphone26, 5, 1000).
link(smartphone26, smartphone9, 5, 1000).
link(smartphone9, isp10, 5, 1000).
link(isp10, smartphone9, 5, 1000).
link(smartphone9, cabinet16, 5, 1000).
link(cabinet16, smartphone9, 5, 1000).
link(accesspoint0, smartphone10, 5, 1000).
link(smartphone10, accesspoint0, 5, 1000).
link(accesspoint0, smartphone13, 5, 1000).
link(smartphone13, accesspoint0, 5, 1000).
link(accesspoint0, smartphone16, 5, 1000).
link(smartphone16, accesspoint0, 5, 1000).
link(accesspoint0, cabinet6, 5, 1000).
link(cabinet6, accesspoint0, 5, 1000).
link(accesspoint0, isp5, 5, 1000).
link(isp5, accesspoint0, 5, 1000).
link(accesspoint0, smartphone19, 5, 1000).
link(smartphone19, accesspoint0, 5, 1000).
link(accesspoint0, smartphone24, 5, 1000).
link(smartphone24, accesspoint0, 5, 1000).
link(smartphone10, smartphone12, 5, 1000).
link(smartphone12, smartphone10, 5, 1000).
link(smartphone10, isp2, 5, 1000).
link(isp2, smartphone10, 5, 1000).
link(smartphone10, isp4, 5, 1000).
link(isp4, smartphone10, 5, 1000).
link(smartphone10, smartphone22, 5, 1000).
link(smartphone22, smartphone10, 5, 1000).
link(smartphone10, smartphone26, 5, 1000).
link(smartphone26, smartphone10, 5, 1000).
link(smartphone10, smartphone29, 5, 1000).
link(smartphone29, smartphone10, 5, 1000).
link(smartphone11, smartphone13, 5, 1000).
link(smartphone13, smartphone11, 5, 1000).
link(smartphone11, isp2, 5, 1000).
link(isp2, smartphone11, 5, 1000).
link(smartphone11, isp4, 5, 1000).
link(isp4, smartphone11, 5, 1000).
link(smartphone11, cabinet6, 5, 1000).
link(cabinet6, smartphone11, 5, 1000).
link(smartphone11, cabinet9, 5, 1000).
link(cabinet9, smartphone11, 5, 1000).
link(smartphone11, cabinet10, 5, 1000).
link(cabinet10, smartphone11, 5, 1000).
link(smartphone11, cabinet12, 5, 1000).
link(cabinet12, smartphone11, 5, 1000).
link(smartphone11, smartphone27, 5, 1000).
link(smartphone27, smartphone11, 5, 1000).
link(accesspoint1, smartphone12, 5, 1000).
link(smartphone12, accesspoint1, 5, 1000).
link(accesspoint1, smartphone13, 5, 1000).
link(smartphone13, accesspoint1, 5, 1000).
link(accesspoint1, smartphone15, 5, 1000).
link(smartphone15, accesspoint1, 5, 1000).
link(accesspoint1, cabinet8, 5, 1000).
link(cabinet8, accesspoint1, 5, 1000).
link(accesspoint1, cabinet11, 5, 1000).
link(cabinet11, accesspoint1, 5, 1000).
link(accesspoint1, isp8, 5, 1000).
link(isp8, accesspoint1, 5, 1000).
link(smartphone12, accesspoint2, 5, 1000).
link(accesspoint2, smartphone12, 5, 1000).
link(smartphone12, smartphone15, 5, 1000).
link(smartphone15, smartphone12, 5, 1000).
link(smartphone12, smartphone16, 5, 1000).
link(smartphone16, smartphone12, 5, 1000).
link(smartphone12, smartphone19, 5, 1000).
link(smartphone19, smartphone12, 5, 1000).
link(smartphone12, smartphone21, 5, 1000).
link(smartphone21, smartphone12, 5, 1000).
link(smartphone12, cabinet11, 5, 1000).
link(cabinet11, smartphone12, 5, 1000).
link(smartphone12, cabinet12, 5, 1000).
link(cabinet12, smartphone12, 5, 1000).
link(smartphone13, isp4, 5, 1000).
link(isp4, smartphone13, 5, 1000).
link(smartphone13, cabinet6, 5, 1000).
link(cabinet6, smartphone13, 5, 1000).
link(smartphone13, isp5, 5, 1000).
link(isp5, smartphone13, 5, 1000).
link(smartphone13, isp6, 5, 1000).
link(isp6, smartphone13, 5, 1000).
link(smartphone13, smartphone25, 5, 1000).
link(smartphone25, smartphone13, 5, 1000).
link(smartphone14, accesspoint2, 5, 1000).
link(accesspoint2, smartphone14, 5, 1000).
link(smartphone14, isp3, 5, 1000).
link(isp3, smartphone14, 5, 1000).
link(smartphone14, smartphone17, 5, 1000).
link(smartphone17, smartphone14, 5, 1000).
link(smartphone14, smartphone21, 5, 1000).
link(smartphone21, smartphone14, 5, 1000).
link(smartphone14, cabinet11, 5, 1000).
link(cabinet11, smartphone14, 5, 1000).
link(smartphone14, cabinet13, 5, 1000).
link(cabinet13, smartphone14, 5, 1000).
link(smartphone14, smartphone25, 5, 1000).
link(smartphone25, smartphone14, 5, 1000).
link(smartphone14, smartphone27, 5, 1000).
link(smartphone27, smartphone14, 5, 1000).
link(accesspoint2, isp7, 5, 1000).
link(isp7, accesspoint2, 5, 1000).
link(accesspoint2, cabinet9, 5, 1000).
link(cabinet9, accesspoint2, 5, 1000).
link(accesspoint2, cabinet10, 5, 1000).
link(cabinet10, accesspoint2, 5, 1000).
link(accesspoint2, smartphone28, 5, 1000).
link(smartphone28, accesspoint2, 5, 1000).
link(isp1, smartphone18, 5, 1000).
link(smartphone18, isp1, 5, 1000).
link(isp1, smartphone28, 5, 1000).
link(smartphone28, isp1, 5, 1000).
link(isp2, isp4, 5, 1000).
link(isp4, isp2, 5, 1000).
link(isp2, cabinet11, 5, 1000).
link(cabinet11, isp2, 5, 1000).
link(smartphone15, smartphone21, 5, 1000).
link(smartphone21, smartphone15, 5, 1000).
link(smartphone15, isp8, 5, 1000).
link(isp8, smartphone15, 5, 1000).
link(smartphone15, smartphone24, 5, 1000).
link(smartphone24, smartphone15, 5, 1000).
link(smartphone15, smartphone29, 5, 1000).
link(smartphone29, smartphone15, 5, 1000).
link(smartphone16, cabinet5, 5, 1000).
link(cabinet5, smartphone16, 5, 1000).
link(smartphone16, cabinet8, 5, 1000).
link(cabinet8, smartphone16, 5, 1000).
link(smartphone16, accesspoint4, 5, 1000).
link(accesspoint4, smartphone16, 5, 1000).
link(isp3, isp7, 5, 1000).
link(isp7, isp3, 5, 1000).
link(isp3, cabinet13, 5, 1000).
link(cabinet13, isp3, 5, 1000).
link(isp3, smartphone26, 5, 1000).
link(smartphone26, isp3, 5, 1000).
link(isp3, cabinet16, 5, 1000).
link(cabinet16, isp3, 5, 1000).
link(isp4, isp9, 5, 1000).
link(isp9, isp4, 5, 1000).
link(isp4, smartphone25, 5, 1000).
link(smartphone25, isp4, 5, 1000).
link(isp4, isp10, 5, 1000).
link(isp10, isp4, 5, 1000).
link(isp4, smartphone29, 5, 1000).
link(smartphone29, isp4, 5, 1000).
link(accesspoint3, cabinet5, 5, 1000).
link(cabinet5, accesspoint3, 5, 1000).
link(accesspoint3, isp7, 5, 1000).
link(isp7, accesspoint3, 5, 1000).
link(accesspoint3, cabinet7, 5, 1000).
link(cabinet7, accesspoint3, 5, 1000).
link(accesspoint3, cabinet10, 5, 1000).
link(cabinet10, accesspoint3, 5, 1000).
link(accesspoint3, cabinet11, 5, 1000).
link(cabinet11, accesspoint3, 5, 1000).
link(accesspoint3, isp8, 5, 1000).
link(isp8, accesspoint3, 5, 1000).
link(accesspoint3, accesspoint5, 5, 1000).
link(accesspoint5, accesspoint3, 5, 1000).
link(smartphone17, accesspoint4, 5, 1000).
link(accesspoint4, smartphone17, 5, 1000).
link(cabinet5, cabinet6, 5, 1000).
link(cabinet6, cabinet5, 5, 1000).
link(cabinet5, isp9, 5, 1000).
link(isp9, cabinet5, 5, 1000).
link(cabinet5, cabinet12, 5, 1000).
link(cabinet12, cabinet5, 5, 1000).
link(cabinet5, smartphone27, 5, 1000).
link(smartphone27, cabinet5, 5, 1000).
link(cabinet6, cabinet7, 5, 1000).
link(cabinet7, cabinet6, 5, 1000).
link(cabinet6, smartphone22, 5, 1000).
link(smartphone22, cabinet6, 5, 1000).
link(isp5, isp6, 5, 1000).
link(isp6, isp5, 5, 1000).
link(isp5, smartphone23, 5, 1000).
link(smartphone23, isp5, 5, 1000).
link(isp5, cabinet15, 5, 1000).
link(cabinet15, isp5, 5, 1000).
link(isp6, cabinet7, 5, 1000).
link(cabinet7, isp6, 5, 1000).
link(isp6, smartphone19, 5, 1000).
link(smartphone19, isp6, 5, 1000).
link(isp6, smartphone20, 5, 1000).
link(smartphone20, isp6, 5, 1000).
link(isp6, smartphone21, 5, 1000).
link(smartphone21, isp6, 5, 1000).
link(isp6, accesspoint5, 5, 1000).
link(accesspoint5, isp6, 5, 1000).
link(smartphone18, isp10, 5, 1000).
link(isp10, smartphone18, 5, 1000).
link(isp7, cabinet8, 5, 1000).
link(cabinet8, isp7, 5, 1000).
link(isp7, smartphone26, 5, 1000).
link(smartphone26, isp7, 5, 1000).
link(isp7, smartphone29, 5, 1000).
link(smartphone29, isp7, 5, 1000).
link(cabinet7, cabinet14, 5, 1000).
link(cabinet14, cabinet7, 5, 1000).
link(cabinet8, cabinet12, 5, 1000).
link(cabinet12, cabinet8, 5, 1000).
link(cabinet9, smartphone20, 5, 1000).
link(smartphone20, cabinet9, 5, 1000).
link(cabinet9, cabinet11, 5, 1000).
link(cabinet11, cabinet9, 5, 1000).
link(smartphone20, cabinet14, 5, 1000).
link(cabinet14, smartphone20, 5, 1000).
link(smartphone21, accesspoint4, 5, 1000).
link(accesspoint4, smartphone21, 5, 1000).
link(smartphone22, cabinet15, 5, 1000).
link(cabinet15, smartphone22, 5, 1000).
link(cabinet11, cabinet15, 5, 1000).
link(cabinet15, cabinet11, 5, 1000).
link(cabinet11, smartphone29, 5, 1000).
link(smartphone29, cabinet11, 5, 1000).
link(isp9, smartphone24, 5, 1000).
link(smartphone24, isp9, 5, 1000).
link(isp9, smartphone25, 5, 1000).
link(smartphone25, isp9, 5, 1000).
link(smartphone23, cabinet14, 5, 1000).
link(cabinet14, smartphone23, 5, 1000).
link(smartphone25, cabinet16, 5, 1000).
link(cabinet16, smartphone25, 5, 1000).
link(accesspoint4, isp10, 5, 1000).
link(isp10, accesspoint4, 5, 1000).
link(accesspoint4, smartphone28, 5, 1000).
link(smartphone28, accesspoint4, 5, 1000).
link(accesspoint5, cabinet14, 5, 1000).
link(cabinet14, accesspoint5, 5, 1000).

