import itertools
def calculate_reward(test_outcome):
    if test_outcome == 0:
        return 10-1
    else:
        return -1

def get_test_with_max_failure_probability(test_dict):
    test_name=""
    test_failure_probability = 0.0
    for tst in test_dict:
        if test_dict[tst].get_failure_probability()>test_failure_probability:
            test_name = tst
            test_failure_probability = test_dict[tst].get_failure_probability()

    return (test_name,test_failure_probability)

def calculate_success_probability(test):
    return test.get_success_probability()

def calculate_failure_probability(test):
    return test.get_failure_probability()


def list_of_combs(arr):
    """returns a list of all subsets of a list"""
    combs = []
    for i in range(0, len(arr) + 1):
        listing = [list(x) for x in itertools.combinations(arr, i)]
        combs.extend(listing)
    return combs

def calc_states_value_iteration(states,action_Pfailure,transitions_act,actions,n):
    max_exp_utility = 0
    exp_utility = 0
    U1 = dict([(s.get_state_name(), 0) for s in states])
    counter =0
    while counter<n:
        U = U1.copy()
        for s in states:
            for a in actions:
                if (s.get_state_name(), a) in transitions_act:
                    s1 = transitions_act[(s.get_state_name(), a)]
                    exp_utility = action_Pfailure[a] * U[s1]
                if max_exp_utility<exp_utility:
                    max_exp_utility = exp_utility

            U1[s.get_state_name()] = s.get_state_reward() + max_exp_utility
            print(U)
            max_exp_utility = 0
            exp_utility = 0
        counter +=1
        #print(counter)
        return U