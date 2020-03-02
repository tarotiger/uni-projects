log_table([], []).

log_table([H|T], [[H,Z]|Y]) :-
	Z is log(H),
	log_table(T, Y). 
	