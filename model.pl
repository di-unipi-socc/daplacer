% APPLICATION
application(AppId, [ServiceIds]).

service(ServiceId, [SWReqs], [HWReqs], [DataIds]).
serviceCost(ServiceId, MaxCost).
serviceCI(ServiceId, MaxCI).

dataType(DataId, Size, [SecReqs]).
requirement(ReqID, Type, [DataIds]).

e2e(A, B, MaxLatency, [(DataId, DataRate)]).

% info at DEPLOYMENT TIME
dataBinding(ServiceId, ReqId, SensorId).

% INFRASTRUCTURE
sensor(SensorId, Type, [DataIds]).
actuator(ActuatorId, Type).

node(NodeId, [SWCaps], HWCaps, [SecCaps], [IoTCaps]).
nodeCost(NodeId, Cost).
nodeCI(NodeId, CarbonIntensity).

link(NodeId1, NodeId2, FeatLat, FeatBw).

% --- ADDITIONAL INFOs ----- %
% Latency in ms
% DataRate in Hz 
% HW* = (CPU GHz, RAM GB, HDD GB).
% IoTCaps = [list of SensorIds/ActuatorIds].

% SW / Sec / HW -> hard reqs
% CarbonIntensity, Cost -> soft reqs