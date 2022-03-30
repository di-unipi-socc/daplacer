% application(AppId, [ServiceIds]).
application(museuMonitor, [interface, controller, dataStorage]).

% service(ServiceId, [SWReqs], [HWReqs], [DataIds], MigrationCost).
service(interface, [ubuntu], (2.4, 4, 128), [videoStream], 5).
service(controller, [python, mySQL], (3, 6, 256), [artStats, visitorStats, videoStream], 30).
service(dataStorage, [mySQL, ubuntu], (5, 4, 512), [artStats, visitorStats], 100).

% dataType(DataId, Size, [SecReqs]).
dataType(artStats, 0.5, [encryption]).
dataType(visitorStats, 0.4, [auth, encryption]).
dataType(videoStream, 2, [auth, encryption]).

%requirement(ReqID, SensorType/ActuatorType, [DataIds]).
requirement(rCam, camera, [videoStream]).
requirement(rVst, smartphone, [visitorStats]).
requirement(rArt, heat, [artStats]).
requirement(rVid, display, [videoStream]).
requirement(rGls, smartphone, [artStats, visitorStats]).
requirement(rDor, smartdoor, [artStats, visitorStats]).

%e2e(A, B, MaxLatency, [(DataId, DataRate)]).
e2e(rArt, dataStorage, 120, [(artStats, 30)]).
e2e(rVst, dataStorage, 100, [(visitorStats, 60)]).
e2e(dataStorage, controller, 100, [(artStats, 20), (visitorStats, 20)]).
e2e(controller, rGls, 60, [(artStats, 30), (visitorStats, 30)]).
e2e(controller, rDor, 60, [(artStats, 25), (visitorStats, 25)]).
e2e(rCam, interface, 50, [(videoStream, 20)]).
e2e(interface, rVid, 80, [(videoStream, 10)]).
e2e(interface, controller, 100, [(videoStream, 20)]).
