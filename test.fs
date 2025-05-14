\ Core arithmetic tests
5 3 + .
10 5 - .
7 3 * .
5 neg .
10 3 mod .
0 5 mod .
.s

\ Stack manipulation tests
1 dup .s
1 2 swap .s
11 2 over .s
1 2 nip .s
1 2 drop .s
1 2 tuck .s

\ Variable tests
variable a
variable b
5 a !
3 b !
a @ .
b @ .
a @ b @ + .
b @ a @ - .
.s

\ Edge cases for variables
variable x
x @
x !
x @
.s
