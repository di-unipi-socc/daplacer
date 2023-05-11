placement(Ss, (HW,BW), PrevBW, Rs, P, (NewHW,NewBW), NewRs, NewP) :-
    compatible(Ss,SNs),
    servicePlacement(SNs, HW, NewHW, P, NewP),
    findRoutes(Ss, NewP, BW, PrevBW, Rs, NewBW, NewRs).
  
  compatible(Ss,SNs) :- findCompatibles(Ss, Cs), sort(1, @>=, Cs, SNs).
  
  findCompatibles([S|Ss], [(L,S,SCompatibles)|Rest]):-
    findCompatibles(Ss, Rest),
    findall((HWCaps, M), lightNodeOK(S, M, HWCaps), Compatibles),  
    sort(1, @>=, Compatibles, SCompatibles),
    length(SCompatibles,L).
  findCompatibles([],[]).
  
  lightNodeOK(S,N,HD) :-
    service(S, SWReqs, HWReqs, DataIds, _),
    node(N, SWCaps, HWCaps, SecCaps, _), HWCaps=(_, _,HD),
    subset(SWReqs,SWCaps),
    getSecReqs(DataIds, SecReqs), subset(SecReqs, SecCaps),
    checkHW(HWReqs,HWCaps).
  
  checkHW((ReqCPU, ReqRAM, ReqHDD),(FeatCPU, FeatRAM, FeatHDD)) :-
    FeatCPU >= ReqCPU,
    FeatRAM >= ReqRAM,
    FeatHDD >= ReqHDD.
  
  servicePlacement([(_,S,Cs)|Ss], HW, NewHW, P, NewP) :-
    member((_,N),Cs), nodeOK(S,N,P,HW),
    servicePlacement(Ss, HW, NewHW, [on(S,N)|P], NewP).
  servicePlacement([], _, NewHW, P, P) :- hwAllocation(P, NewHW).
  
  nodeOK(S, N, P, AllocHW):-
    service(S, _, HWReqs, _, _),
    node(N, _, HWCaps, _, _),
    hwOK(HWReqs, HWCaps, N, P, AllocHW).
  
  hwOK(HWReqs, HWCaps, N, P, AllocHW) :-
    findall(HW,  member((N,HW),AllocHW),HWs), sumHW(HWs, CurrAllocHW),
    findall(HW, (service(S,_,HW,_,_), member(on(S,N), P)), OkHWs), sumHW(OkHWs, NewAllocHW), 
    checkHW(HWReqs, HWCaps, CurrAllocHW, NewAllocHW).
  
  sumHW(HWs, AllocHW):- InitAllocHW=(0,0,0), sumHW(HWs, InitAllocHW, AllocHW).
  sumHW([(CPU, RAM, HDD)|HWs], (AllocCPU, AllocRAM, AllocHDD), AllocHW) :-
    TAllocCPU is max(CPU,AllocCPU), TAllocRAM is RAM + AllocRAM, TAllocHDD is HDD + AllocHDD,
    sumHW(HWs, (TAllocCPU, TAllocRAM, TAllocHDD), AllocHW).
  sumHW([], AllocHW, AllocHW).
  
  checkHW((ReqCPU, ReqRAM, ReqHDD),(FeatCPU, FeatRAM, FeatHDD),(_, CurrRAM, CurrHDD),(_, NewRAM, NewHDD)) :-
    FeatCPU >= ReqCPU,
    FeatRAM >= ReqRAM - CurrRAM + NewRAM,
    FeatHDD >= ReqHDD - CurrHDD + NewHDD.
  
  hwAllocation(P,AllocHW) :-
    findall((N,HW), (member(on(S,N), P), service(S,_,HW,_,_)), HWs),
    findall((N,SumHW), (group_by(N, HW, member((N,HW),HWs), Group), sumHW(Group, SumHW)), AllocHW).