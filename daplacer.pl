:- ['src/placer.pl', 'src/routes.pl'].
:- ['data/infra.pl','data/app.pl'].
:- dynamic deployment/4.

:-set_prolog_flag(answer_write_options,[max_depth(0)]).
:-set_prolog_flag(stack_limit, 16 000 000 000).
:-set_prolog_flag(last_call_optimisation, true).

daplacer(App, NewP, NewRs) :-
  \+ deployment(App, _, _, _), application(App, Ss), Alloc=([],[]), Rs=[], P=[], PrevBW=[],
  placement(Ss, Alloc, PrevBW, Rs, P, NewAlloc, NewRs, NewP),
  assert(deployment(App, NewP, NewRs, NewAlloc)).
daplacer(App, NewP, NewRs) :-
  deployment(App, PrevP, PrevRs, PrevAlloc), newServices(PrevP, NewSs),
  sortByMigrationCost(PrevP, SPrevP),
  once(reasoningStep(SPrevP, PrevAlloc, PrevRs, SsToMove, TmpBW, TmpRs, TmpP)),
  append(NewSs, SsToMove, SsToPlace),
  placement(SsToPlace, PrevAlloc, TmpBW, TmpRs, TmpP, NewAlloc, NewRs, NewP),
  retract(deployment(App, _, _, _)), assert(deployment(App, NewP, NewRs, NewAlloc)).
daplacer(App, NewP, NewRs) :-
  deployment(App,_,_,Alloc), application(App, Ss), Rs=[], P=[], PrevBW=[],
  placement(Ss, Alloc, PrevBW, Rs, P, NewAlloc, NewRs, NewP),
  retract(deployment(App,_,_)), assert(deployment(App, NewP, NewRs, NewAlloc)).

reasoningStep([on(S,_)|P], (HW,BW), Rs, SsToMove, NewBW, NewRs, NewP) :-
  reasoningStep(P, (HW,BW), Rs, SsToMove, NewBW, NewRs, NewP),
  \+ service(S, _, _, _, _).
reasoningStep([on(S,N)|P], (HW,BW), Rs, SsToMove, NewBW, NewRs, [on(S,N)|NewP]) :-
  reasoningStep(P, (HW,BW), Rs, SsToMove, TmpBW, TmpRs, NewP),
  nodeOK(S, N, NewP, HW), 
  serviceRoutesOK(S, N, NewP, BW, Rs, TmpBW, Tmp2Routes, NewBW), 
  append(TmpRs, Tmp2Routes, NewRs).
reasoningStep([on(S,_)|P], (HW,BW), Rs, [S|SsToMove], NewBW, NewRs, NewP) :-
  reasoningStep(P, (HW,BW), Rs, SsToMove, NewBW, NewRs, NewP).
reasoningStep([],_,_,[],[],[],[]).

newServices(P, NewServices) :- findall(S, (service(S,_,_,_,_), \+ member(on(S,_), P)), NewServices).

sortByMigrationCost(P, SP) :-
  findall((C,(S,N)), (member(on(S,N), P), service(S,_,_,_,C)), Costs),
  sort(1, @>=, Costs, SCosts),
  findall(on(S,N), member((_,(S,N)), SCosts), SP).
