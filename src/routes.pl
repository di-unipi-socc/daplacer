getSecReqs([D|Ds],SecReqs) :-
    dataType(D, _, SecReqsD),
    getSecReqs(Ds, SecReqsDs), append(SecReqsD, SecReqsDs, TSecReqs),
    sort(TSecReqs, SecReqs).
  getSecReqs([],[]).
  
  findRoutes([S|Ss], P, AllocBW, PrevBW, Routes, NewAllocBW, NewRoutes) :-
    member(on(S,N),P),
    findall((S1S2, N1N2, Lat, BW), (relevantS2S(S1S2, N1N2, Lat, BW, S, N, P),\+ member((S1S2,_,_),Routes)), N2Ns),
    qosOK(N2Ns, AllocBW, PrevBW, Routes, TAllocBW, TRoutes),!,
    findRoutes(Ss, P, AllocBW, TAllocBW, TRoutes, NewAllocBW, NewRoutes).
  findRoutes([], _, _, AllocBW, Routes, AllocBW, Routes).
  
  qosOK([(S1S2, N1N2, ReqLat, ReqBW)|Rs], AllocBW, PrevBW, Routes, NewAllocBW, NewRoutes) :-
    route(N1N2, ReqLat, ReqBW, 0, AllocBW, PrevBW, [], TAllocBW, RR), reverse(RR, R),
    qosOK(Rs, AllocBW, TAllocBW, [(S1S2,ReqBW,R)|Routes], NewAllocBW, NewRoutes).
  qosOK([], _, AllocBW, Routes, AllocBW, Routes).
  
  route((N1,N2), ReqLat, ReqBW, OldLat, AllocBW, PrevBW, Route, NewAllocBW, NewRoute) :-
    dif(N1,N2), link(N1, X, FeatLat, FeatBW), \+ member(X, Route),
    latencyOK(ReqLat, FeatLat, OldLat, NewLat),
    bwOK(N1, X, ReqBW, FeatBW, AllocBW, PrevBW, TAllocBW),
    route((X,N2), ReqLat, ReqBW, NewLat, AllocBW, TAllocBW, [N1|Route], NewAllocBW, NewRoute).
  route((N,N), _, _, _, _, AllocBW, Route, AllocBW, [N|Route]).
  
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
  
  relevantS2S((S,S2), (N,N2), Lat, ReqBW, S, N, P) :-
    e2e(S,S2,Lat,DataIds),
    ((service(S2,_,_,_,_), member(on(S2, N2), P));
     (requirement(S2, AT, _), actuator(A, AT), dataBinding(S, S2, A), node(N2, _, _, _, IoT), member(A, IoT))),
    dif(N, N2),
    findall(BW, getBW(DataIds, BW), BWs), sum_list(BWs, ReqBW).
  
  relevantS2S((S1,S), (N1,N), Lat, ReqBW, S, N, P) :-
    e2e(S1,S,Lat,DataIds),
    ((service(S1,_,_,_,_), member(on(S1, N1), P));
     (requirement(S1, ST, _), sensor(Sns, ST, _), dataBinding(S, S1, Sns), node(N1, _, _, _, IoT), member(Sns, IoT))),
    dif(N, N1),
    findall(BW, getBW(DataIds, BW), BWs), sum_list(BWs, ReqBW).
  
  latencyOK(ReqLat, FeatLat, CurrLat, TotLat) :-
    TotLat is CurrLat + FeatLat, TotLat =< ReqLat.
  
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