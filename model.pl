% APPLICATION
application(AppId, [ServiceIds]).

service(ServiceId, [SWReqs], [HWReqs], [DataIds]).
dataType(DataId, Size, [SecReqs]).
requirement(ReqID, Type, [DataIds]).

e2e(A, B, MaxLatency, [(DataId, DataRate)]).

% info at DEPLOYMENT TIME
dataBinding(ServiceId, ReqId, SensorId).

% INFRASTRUCTURE
sensor(SensorId, Type, [DataIds]).
actuator(ActuatorId, Type).

node(NodeId, [SWCaps], HWCaps, [SecCaps], [IoTCaps]).
link(NodeId1, NodeId2, FeatLat, FeatBw). 

% --- ADDITIONAL INFOs ----- %
% Latency in ms
% DataRate in Hz 
% HW* = (CPU GHz, RAM GB, HDD GB).
% IoTCaps = [list of SensorIds/ActuatorIds].
