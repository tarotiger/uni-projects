% Base case: Result is a number and not an expression
eval(Result, Result) :-
    number(Result).

% Addition operation case 
eval(add(X, Y), Result) :-
    eval(X, XResult),
    eval(Y, YResult),
    Result is XResult + YResult.

% Subtraction operation case
eval(sub(X,Y), Result) :-
    eval(X, XResult),
    eval(Y, YResult),
    Result is XResult - YResult.

% Division operation case 
eval(div(X,Y), Result) :-
    eval(X, XResult),
    eval(Y, YResult),
    Result is XResult / YResult.

% Multiplcation operation case
eval(mul(X,Y), Result) :-
    eval(X, XResult),
    eval(Y, YResult),
    Result is XResult * YResult.