import pandas as pd
import numpy as np
import models
import operations
def main():
    component_probabilities_df = pd.read_csv('data/ComponentProbabilities.csv')
    #test_components_df = pd.read_csv('data/TestComponents.csv')
    test_components_df = pd.read_csv('data/TestComponents_small.csv')
    #test_outcomes_df = pd.read_csv('data/TestOutcomes.csv')
    test_outcomes_df = pd.read_csv('data/TestOutcomes_small.csv')
    agent_count = 1
    comp_dict = {}
    comp_run_dict = {}
    test_comp_dict = {}
    test_comp = []
    test_dict = {}
    test_outcomes_dict = {}
    run_tests = {}
    test_run_dict ={}
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
                tests_run = s
                test_left = list(set(state_index).difference(set(s)))
                for st in tests_run:
                    state_outcomes.append(test_outcomes_dict[st])
                state = models.State(state_name,tests_run,test_left,state_outcomes)
                states.append(state)
                state_counter+=1
                #print(state.get_state_info(),state.get_state_reward())


    transitions = []
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
                    expected_reward[tr] = action_Pfailure[action_name]*operations.calculate_reward(0) + (1- action_Pfailure[action_name])*operations.calculate_reward(1)
                    transitions.append(tr)

    print(actions)
    print(action_Pfailure)
    print(transitions)
    print(expected_reward)





''' 


       for test in test_dict:
        if test in test_outcomes_dict.keys():
            test_run_dict[test] = models.TestRun(test_dict[test],test_outcomes_dict[test])
            #print(test_run_dict[test].get_test().get_test_name(),test_run_dict[test].get_test_outcome(),operations.calculate_reward(test_run_dict[test].get_test_outcome()))

   state_index = [0 for s in test_dict.keys()]
   for i, t in enumerate(test_dict.keys()):
       state_index[i] = t

   print(state_index)

   states_comb = operations.list_of_combs(state_index)
   print(states_comb)

   transitions = []
   for s1 in states_comb:
       for s2 in states_comb:
           if len(s1)+ agent_count == len(s2):
               next_action= set(s2) - set(s1)
               if len(next_action)==agent_count:
                   transitions.append((s1,list(next_action),test_dict[list(next_action)[0]].get_failure_probability(),s2))  #TBD - change to support multi agents
                                                                                                                            # test_dict[list(next_action)[0]].get_failure_probability()

   print(transitions)
'''




if __name__ == "__main__":
    main()