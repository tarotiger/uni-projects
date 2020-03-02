paruns([], []).

% Only number in the list
paruns([Num], [[Num]]).

% Head of list is odd and second number is even 
paruns([A,B|T], [[A]|Y]) :-
	0 is mod(A, 2),
	1 is mod(B, 2),
	paruns([B|T], Y).

% Head of list is even and second number is odd
paruns([A,B|T], [[A]|Y]) :-
	1 is mod(A, 2),
	0 is mod(B, 2),
	paruns([B|T], Y).

% Head of list and second number are both odd
paruns([A,B|T], [[A|X]|Y]) :-
	1 is mod(A, 2),
	1 is mod(B, 2),
	paruns([B|T], [X|Y]).

% Head of list and second number are both even
paruns([A,B|T], [[A|X]|Y]) :-
	0 is mod(A, 2),
	0 is mod(B, 2),
	paruns([B|T], [X|Y]).