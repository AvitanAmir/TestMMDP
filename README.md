The theory
-----------
Just repeating the theory quickly, an MDP is:

MDP=⟨S,A,T,R,γ⟩
where S are the states, A the actions, T the transition probabilities (i.e. the the probabilities Pr(s′|s,a) to go from one state to another given an action),
R the rewards (given a certain state, and possibly action),and γ is a discount factor that is used to reduce the importance of the of future rewards.

So in order to use it, you need to have predefined:

States: these can refer to for example grid maps in robotics, or for example door open and door closed.
Actions: a fixed set of actions, such as for example going north, south, east, etc for a robot, or opening and closing a door.
Transition probabilities: the probability of going from one state to another given an action. For example what is the probability of an open door if the action is open. In a perfect world the later could be 1.0, but if it is a robot, it could have failed in handling the door knob correctly. Another example in the case of a moving robot, would be the action north, which in most cases would bring it in the grid cell north of it, but in some cases could have moved too much and reached the next cell for example.
Rewards: these are used to guide the planning. In the case of the grid example we might want to go to a certain cell, and the reward will be higher if we get closer. In the case of the door example an open door might give a high reward.
Once the MDP is defined, a policy can be learned by doing Value Iteration or Policy Iteration which calculates the expected reward for each of the states. The policy then gives per state the best (given the MDP model) action to do.

In summary an MDP is useful when you want to plan an efficient sequence of actions in which your actions can be not always 100% effective.




Tests:
1	2	3	4	5	6	7	…	…	n
Pr1	Pr2	Pr3	Pr4	Pr5	Pr6	Pr7			Prn


Pri = Probability for Test i to fail.

Actual bugs in Tests:
1	2	3	4	5	6	7	…	…	n
0	1	1	0	0	0	1			0


State:
Test Left – collection of tests left
Test Run – collection of tests already ran

Action:
Test Left – collection of tests left
Transition Function(Pr(s′|s,a)):
TR (Testi,A,Testi’) = (Pri(Testi),1 - Pri(Testi))

Reward:
Test Fail = +10 -1
Test Pass = -1

In each iteration we choose the max expected utility for each state according to transition function indicates the probability for being failed X expect max of choosing the next Test.
