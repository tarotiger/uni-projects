sumsq_even([], 0).

sumsq_even([H|T], X) :-
	0 is mod(H, 2),
	sumsq_even(T, Y),
	X is H * H + Y.

sumsq_even([H|T], X) :-
	1 is mod(H,2),
	sumsq_even(T, X).
