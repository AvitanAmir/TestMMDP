Tests:
1	2	3	4	5	6	7	…	…	n
Pr1	Pr2	Pr3	Pr4	Pr5	Pr6	Pr7			Prn


Pri = Probability for Test i to fail.

Actual bugs in Tests:
1	2	3	4	5	6	7	…	…	n
0	1	1	0	0	0	1			0


State:
Running Test i
Test Left – collection of tests left
Test Run – collection of tests already ran

Action:
Do Test # after running Test i
Transition Function:
TR (Testi,A,Testi’)

Reward:
Test Fail = +1
Test Pass = 0.1

In each iteration we choose the max expected utility for each state according to transition function indicates the probability for being failed X expect max of choosing the next Test.
