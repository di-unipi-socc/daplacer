:-['infra.pl','app.pl'].
:-dynamic deployment/4.

:-set_prolog_flag(stack_limit, 16 000 000 000).
:-set_prolog_flag(last_call_optimisation, true).

dap(A,P,R,Infs,Time) :- 
  statistics(inferences, InfA),
        statistics(cputime, TimeA),
          daplacer(A,P,R),
        statistics(cputime, TimeB),
  statistics(inferences, InfB),

  Infs is InfB - InfA,
  Time is TimeB - TimeA.

% first query: daplacer(myShaders, P, A, R).
daplacer(App, Placement, Routes) :-
  \+ deployment(App, _, _, _), placement(App, Placement, Alloc, Routes),
  assert(deployment(App, Placement, Alloc, Routes)).

placement(App, Placement, Alloc, Routes) :-
  application(App, Services),
  partialPlacement(Services, ([],[]), [], [], Alloc, Routes, Placement).

partialPlacement(Services, (AllocHW,AllocBW), Routes, OkPlacement, (NewAllocHW,NewAllocBW), NewRoutes, NewPlacement) :-
  servicePlacement(Services, AllocHW, OkPlacement, NewPlacement),
  findRoutes(Services, NewPlacement, AllocBW, Routes, NewAllocBW, NewRoutes),
  hwAllocation(NewPlacement, NewAllocHW).

reasoningStep([on(S,_)|Ss], Alloc, Routes, KOs, NewBW, NewR, NewP) :-
  reasoningStep(Ss, Alloc, Routes, KOs, NewBW, NewR, NewP),
  \+ service(S, _, _, _).
reasoningStep([on(S,N)|Ss], (AllocHW,AllocBW), Routes, KOs, NewBW, NewR, [on(S,N)|NewP]) :-
  reasoningStep(Ss, (AllocHW,AllocBW), Routes, KOs, TmpBW, TmpR, NewP),
  nodeOK(S, N, NewP, AllocHW), serviceRoutesOK(S, N, NewP, AllocBW, Routes, TmpBW, TmpOkRoutes, NewBW), 
  append(TmpR, TmpOkRoutes, NewR).
reasoningStep([on(S,_)|Ss], (AllocHW,AllocBW), Routes, [S|KOs], NewBW, NewR, NewP) :-
  reasoningStep(Ss, (AllocHW,AllocBW), Routes, KOs, NewBW, NewR, NewP).
reasoningStep([],_,_,[],[],[],[]).

/*reasoningStep([on(S,_)|Ss], Alloc, Routes, OkBW, OkR, OkP, KOs, NewBW, NewR, NewP) :-
  \+ service(S, _, _, _),
  reasoningStep(Ss, Alloc, Routes, OkBW, OkR, OkP, KOs, NewBW, NewR, NewP). 
reasoningStep([on(S,N)|Ss], Alloc, Routes, OkBW, OkR, OkP, KOs, NewBW, NewR, NewP) :-
  Alloc = (AllocHW, AllocBW),
  nodeOK(S, N, OkP, AllocHW),
  serviceRoutesOK(S, N, OkP, AllocBW, Routes, OkBW, OldOkRoutes, TmpBW), append(OkR, OldOkRoutes, TmpRoutes),!, % green cut
  reasoningStep(Ss, Alloc, Routes, TmpBW, TmpRoutes, [on(S,N)|OkP], KOs, NewBW, NewR, NewP).
reasoningStep([on(S,_)|Ss], Alloc, Routes, OkBW, OkR, OkP, [S|KOs], NewBW, NewR, NewP) :-
  reasoningStep(Ss, Alloc, Routes, OkBW, OkR, OkP, KOs, NewBW, NewR, NewP).
reasoningStep([], _, _, AllocBW, Routes, StableP, [], AllocBW, Routes, StableP).*/

nodeOK(S, N, P, AllocHW):-
  service(S, SWReqs, HWReqs, DataIds),
  node(N, SWCaps, HWCaps, SecCaps, _),
  subset(SWReqs, SWCaps),
  hwOK(HWReqs, HWCaps, N, P, AllocHW),
  getSecReqs(DataIds, SecReqs), subset(SecReqs, SecCaps).

servicePlacement([S|Ss], AllocHW, P, NewP) :-
  nodeOK(S, N, P, AllocHW),
  servicePlacement(Ss, AllocHW, [on(S,N)|P], NewP).
servicePlacement([], _, P, P).

newServices(P, NewServices) :- findall(S, (service(S, _, _, _), \+ member(on(S,_), P)), NewServices).

hwOK(HWReqs, HWCaps, N, P, AllocHW) :-
  findall(HW,  member((N,HW),AllocHW),HWs), sumHW(HWs, CurrAllocHW),
  findall(HW, (service(S,_,HW,_), member(on(S,N), P)), OkHWs), sumHW(OkHWs, NewAllocHW), 
  checkHW(HWReqs, HWCaps, CurrAllocHW, NewAllocHW).

sumHW(HWs, AllocHW):- sumHW(HWs, (0,0,0), AllocHW).
sumHW([(CPU, RAM, HDD)|HWs], (AllocCPU, AllocRAM, AllocHDD), AllocHW) :-
  TAllocCPU is max(CPU,AllocCPU), TAllocRAM is RAM + AllocRAM, TAllocHDD is HDD + AllocHDD,
  sumHW(HWs, (TAllocCPU, TAllocRAM, TAllocHDD), AllocHW).
sumHW([], AllocHW, AllocHW).

checkHW((ReqCPU, ReqRAM, ReqHDD),(FeatCPU, FeatRAM, FeatHDD),(_, CurrRAM, CurrHDD),(_, NewRAM, NewHDD)) :-
  FeatCPU >= ReqCPU,
  FeatRAM >= ReqRAM - CurrRAM + NewRAM,
  FeatHDD >= ReqHDD - CurrHDD + NewHDD.

getSecReqs([D|Ds],SecReqs) :-
  dataType(D, _, SecReqsD),
  getSecReqs(Ds, SecReqsDs), append(SecReqsD, SecReqsDs, TSecReqs),
  sort(TSecReqs, SecReqs).
getSecReqs([],[]).

hwAllocation(P,AllocHW) :-
  findall((N,HW), (member(on(S,N), P), service(S,_,HW,_)), HWs),
  findall((N,SumHW), (group_by(N, HW, member((N,HW),HWs), Group), sumHW(Group, SumHW)), AllocHW).

findRoutes([S|Ss], P, AllocBW, Routes, NewAllocBW, NewRoutes) :-
  member(on(S,N),P),
  findall((S1S2, N1N2, Lat, BW), (relevantS2S(S1S2, N1N2, Lat, BW, S, N, P),\+ member((S1S2,_,_),Routes)), N2Ns),
  qosOK(N2Ns, AllocBW, Routes, TAllocBW, TRoutes),
  findRoutes(Ss, P, TAllocBW, TRoutes, NewAllocBW, NewRoutes).
findRoutes([], _, AllocBW, Routes, AllocBW, Routes).

qosOK([(S1S2, N1N2, ReqLat, ReqBW)|Rs], AllocBW, Routes, NewAllocBW, NewRoutes) :-
  route(N1N2, ReqLat, ReqBW, 0, AllocBW, [], TAllocBW, R),
  qosOK(Rs, TAllocBW, [(S1S2,ReqBW,R)|Routes], NewAllocBW, NewRoutes).
qosOK([], AllocBW, Routes, AllocBW, Routes).

/*route(N1N2, ReqLat, ReqBW, AllocBW, NewAllocBW, BestRoute) :-
  findall((R,L,BWAlloc), route(N1N2, ReqLat, ReqBW, B, L, AllocBW, [], BWAlloc, R), Routes),
  pickBestRoute(Routes, BestRoute, NewAllocBW).*/

/*route((N1,N2), ReqLat, ReqBW, MinBW, NewLat, AllocBW, Route, NewAllocBW, NewRoute):-
  link(N1, X, FeatLat, FeatBW), \+ member(X, Route),  
  route((X,N2), ReqLat, ReqBW, OldMinBW, OldLat, AllocBW, [N1|Route], TmpAllocBW, NewRoute),
  latencyOK(ReqLat, FeatLat, OldLat, NewLat),
  bwOK(N1, X, ReqBW, FeatBW, TmpAllocBW, [], NewAllocBW), MinBW is min(OldMinBW, FeatBW).
route((N,N), _, _, inf, 0, AllocBW, Route, AllocBW, [N|Route]).*/

route((N1,N2), ReqLat, ReqBW, OldLat, AllocBW, Route, NewAllocBW, NewRoute) :-
  dif(N1,N2), link(N1, X, FeatLat, FeatBW), \+ member(X, Route),
  latencyOK(ReqLat, FeatLat, OldLat, NewLat),
  bwOK(N1, X, ReqBW, FeatBW, AllocBW, [], TmpAllocBW),
  route((X,N2), ReqLat, ReqBW, NewLat, TmpAllocBW, [N1|Route], NewAllocBW, NewRoute).
route((N,N), _, _, _, AllocBW, Route, AllocBW, [N|Route]).

/*pickBestRoute(Routes, BestRoute, AllocBW) :-
  member((R,L,AllocBW), Routes),
  \+ (member((R1,L1,_), Routes), dif((R1,L1,_),(R,L,_)), L1<L),
  reverse(R, BestRoute).*/

serviceRoutesOK(S, N, P, AllocBW, Routes, OkBW, NewRoutes, NewBW) :-
  findall((S1S2, Lat, BW), relevantS2S(S1S2, _, Lat, BW, S, N, P),N2Ns),
  routesOK(N2Ns, AllocBW, Routes, OkBW, NewRoutes, NewBW).

routesOK([(S1S2,ReqLat, ReqBW)|Ps], AllocBW, Routes, OkBW, [(S1S2,ReqBW,R)|NewRoutes], NewBW) :-
  member((S1S2,_,R), Routes),
  checkPath(R, ReqLat, 0, ReqBW, AllocBW, OkBW, TmpBW),
  routesOK(Ps, AllocBW, Routes, TmpBW, NewRoutes, NewBW).
routesOK([], _, _, AllocBW, [], AllocBW).

checkPath([N1,N2|Ns], ReqLat, Lat, ReqBW, AllocBW, PrevAllocBW, NewAllocBW) :-
  link(N1, N2, FeatLat, FeatBW),
  latencyOK(ReqLat, FeatLat, Lat, TmpLat),
  bwOK(N1, N2, ReqBW, FeatBW, AllocBW, PrevAllocBW, TmpAllocBW),
  checkPath([N2|Ns], ReqLat, TmpLat, ReqBW, AllocBW, TmpAllocBW, NewAllocBW).
checkPath([_], _, _, _, _, NewAllocBW, NewAllocBW).

latencyOK(ReqLat, FeatLat, CurrLat, TotLat) :-
  TotLat is CurrLat + FeatLat, TotLat =< ReqLat.

relevantS2S((S,S2), (N,N2), Lat, ReqBW, S, N, P) :-
  e2e(S,S2,Lat,DataIds),
  ((service(S2, _, _, _), member(on(S2, N2), P));
   (requirement(S2, AT, _), actuator(A, AT), dataBinding(S, S2, A), node(N2, _, _, _, IoT), member(A, IoT))),
  dif(N, N2),
  findall(BW, getBW(DataIds, BW), BWs), sum_list(BWs, ReqBW).

relevantS2S((S1,S), (N1,N), Lat, ReqBW, S, N, P) :-
  e2e(S1,S,Lat,DataIds),
  ((service(S1, _, _, _), member(on(S1, N1), P));
   (requirement(S1, ST, _), sensor(Sns, ST, _), dataBinding(S, S1, Sns), node(N1, _, _, _, IoT), member(Sns, IoT))),
  dif(N, N1),
  findall(BW, getBW(DataIds, BW), BWs), sum_list(BWs, ReqBW).

getBW(DataIds, BW) :-
  dataType(D, Size, _),
  member((D,DataRate), DataIds),
  BW is Size*DataRate.

bwOK(N1, N2, ReqBW, FeatBW, AllocBW, PrevBW, NewBW):-
  findall(BW, member((N1,N2,BW),AllocBW), BWs), sum_list(BWs, CurrAllocBW), 
  findall(BW, member((N1,N2,BW),PrevBW), NewBWs), sum_list(NewBWs, NewAllocBW),
  bwTh(T), FeatBW >= ReqBW - CurrAllocBW + NewAllocBW + T,
  bwAllocation(N1, N2, ReqBW, PrevBW, NewBW).

bwAllocation(N1, N2, ReqBW, TBW, [(N1, N2, NewBW)|BWs]) :-
  select((N1, N2, BW), TBW, BWs), NewBW is BW+ReqBW.
bwAllocation(N1, N2, ReqBW, TBW, [(N1, N2, ReqBW)|TBW]).