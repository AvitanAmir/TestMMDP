import pandas as pd
import numpy as np
import models
import operations
#import MMDP
def main():
    component_probabilities_df = pd.read_csv('data/ComponentProbabilities.csv')
    #test_components_df = pd.read_csv('data/TestComponents.csv')
    test_components_df = pd.read_csv('data/TestComponents_small.csv')
    #test_outcomes_df = pd.read_csv('data/TestOutcomes.csv')
    test_outcomes_df = pd.read_csv('data/TestOutcomes_small.csv')
    agent_count = 2
    comp_dict = {}
    comp_run_dict = {}
    test_comp_dict = {}
    #test_comp = []
    test_dict = {}
    test_outcomes_dict = {}
    #run_tests = {}
    #test_run_dict ={}
    action_dict ={}

    for index, row in component_probabilities_df.iterrows():
        # print(row['ComponentName'], row['FaultProbability'])
        if row['ComponentName'] in comp_dict.keys():
            pass
        else:
            comp_dict[row['ComponentName']] = models.Component(row['ComponentName'], row['FaultProbability'])
            comp_run_dict[row['ComponentName']] = 0

    for index, row in test_components_df.iterrows():
        # print(row['TestName'], row['ComponentName'])
        if row['TestName'] in test_comp_dict.keys():
            test_comp_dict[row['TestName']].append (comp_dict[row['ComponentName']])
        else:
            test_comp_dict[row['TestName']] = []
            test_comp_dict[row['TestName']].append(comp_dict[row['ComponentName']])

    for test in test_comp_dict:
        test_dict[test] = models.Test(test,test_comp_dict[test])
        #print(test,test_dict[test].get_failure_probability())

    for index, row in test_outcomes_df.iterrows():
        #print(row['TestName'], row['TestOutcome'])
        if row['TestName'] in test_outcomes_dict.keys():
           pass
        else:
            test_outcomes_dict[row['TestName']] = row['TestOutcome']

    # create 2 agents tuple of actions (test1,test2) and probability for failure when performing both actions in specific state
    # store it in action_dict which contains the actual set of actions
    for test1 in test_dict:
        for test2 in test_dict:
            if test1 == test2:
                pass
            else:
                action_key = (test1,test2)
                action_dict[action_key] = 1 - (float(test_dict[test1].get_success_probability()) * float(test_dict[test2].get_success_probability()))

    #print(action_dict)

    # Create all possible states and reward for the test run till current state
    states = []
    state_index = [0 for s in test_dict.keys()]
    for i, t in enumerate(test_dict.keys()):
        state_index[i] = t
    states_comb = operations.list_of_combs(state_index)
    #print(states_comb)
    state_counter = 0
    for s in states_comb:
            if len(s)%2==0:
                state_outcomes = []
                state_name = 'S'+str(state_counter)
                state_idx = state_counter
                tests_run = s
                test_left = list(set(state_index).difference(set(s)))
                for st in tests_run:
                    state_outcomes.append(test_outcomes_dict[st])
                state = models.State(state_name,state_idx,tests_run,test_left,state_outcomes)
                states.append(state)
                state_counter+=1
                #print(state.get_state_info(),state.get_state_reward())

    transitions = []
    transitions_act = {}
    actions = {}
    action_Pfailure = {}
    expected_reward={}
    action_counter = 0
    for s in states:
        source_state_run = s.get_tests_run()
        for t in states:
            target_state_run = t.get_tests_run()
            if s.get_state_name()!= t.get_state_name():
                action =  list(set(target_state_run).difference(set(source_state_run)))
                if len(action)==2:
                    action_tup = (action[0],action[1])
                    action_tup_reversed = (action[1],action[0])
                    if action_tup in actions:
                        action_name = actions[action_tup]
                    elif action_tup_reversed in actions:
                        action_name = actions[action_tup_reversed]
                    else:
                        action_name = 'A'+str(action_counter)
                        actions[action_tup] = action_name
                        action_Pfailure[action_name] = 1 - (float(test_dict[action_tup[0]].get_success_probability()) * float(test_dict[action_tup[1]].get_success_probability()))
                        action_counter += 1
                    tr = (s.get_state_name(),action_name,t.get_state_name())
                    tr_act = (s.get_state_name(), action_name)
                    expected_reward[tr] = action_Pfailure[action_name]*operations.calculate_reward(0) + (1- action_Pfailure[action_name])*operations.calculate_reward(1)
                    transitions.append(tr)
                    transitions_act[tr_act] =t.get_state_name()

    print(actions)
    print(action_Pfailure)
    print(transitions_act)
    print(expected_reward)
    print(states)

# calculate value iteration
    max_exp_utility = 0
    exp_utility = 0
    max_iter_num =100
    U1 = dict([(s.get_state_name(), 0) for s in states])
    counter =0
    while counter<max_iter_num:
        U = U1.copy()
        for s in states:
            for a in actions.values():
                if (s.get_state_name(), a) in transitions_act:
                    s1 = transitions_act[(s.get_state_name(), a)]
                    exp_utility = action_Pfailure[a] * U[s1]
                if max_exp_utility<exp_utility:
                    max_exp_utility = exp_utility
            U1[s.get_state_name()] = s.get_state_reward() + max_exp_utility
            #print(U)
            max_exp_utility = 0
            exp_utility = 0
        counter +=1
        #print(counter)
    print(U)
# calculate optimal policy
    current_state = 'S0'
    max_V = 0.0
    tran_V = 0.0
    best_act = ''
    number_of_tests = 10
    policy_actions = []
    for i in range(0,int(number_of_tests/agent_count)):
        for a in actions.values():
           if (current_state,a) in transitions_act:
               s1 =  transitions_act[(current_state,a)]
               tran_V = U[s1]
               if tran_V>max_V and a not in policy_actions:
                   max_V = tran_V
                   best_act = a
        if best_act!='':
            policy_actions.append(best_act)
            current_state = transitions_act[(current_state,best_act)]
        max_V = 0.0
        tran_V = 0.0
        best_act = ''

    print(policy_actions)


'''
    discount_factor = 1.0
    V = np.zeros(len(states))
    def one_step_lookahead(state, V):
            A = np.zeros(len(actions))
            for tr in transitions:
                if tr[0] ==state.get_state_name():
                    A[int(tr[1].replace('A',''))] +=action_Pfailure[tr[1]]*(expected_reward[tr] + discount_factor * V[int(tr[2].replace('S',''))])
            return A

    for s in states:
        # Do a one-step lookahead to find the best action
        A = one_step_lookahead(s, V)
        best_action_value = np.max(A)
        # Update the value function.
        V[s.get_state_index()] = best_action_value

    policy = np.zeros([len(states), len(actions)])
    for s in states:
        # One step lookahead to find the best action for this state
        A = one_step_lookahead(s, V)
        best_action = np.argmax(A)
        # Always take the best action
        policy[s.get_state_index(), best_action] = 1.0

    state_i = 0
    policy_route =[]
    for i in range(len(actions)):
        for j in range(len(policy[state_i])):
            if policy[state_i][j]==1:
                act = j
        for e in expected_reward:
            if e[0] =='S'+ str(state_i) and e[1]=='A'+str(act):
                if e[1] not in policy_route:
                    policy_route.append(e[1])
                    #print(e)
                    state_i = int(e[2].replace('S',''))
                    break

    print(policy_route)

'''


if __name__ == "__main__":
    main()