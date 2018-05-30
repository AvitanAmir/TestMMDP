def calculate_reward(test_outcome):
    if test_outcome == 0:
        return 1
    else:
        return 0.1

def get_test_with_max_failure_probability(test_dict):
    test_name=""
    test_failure_probability = 0.0
    for tst in test_dict:
        if test_dict[tst].get_failure_probability()>test_failure_probability:
            test_name = tst
            test_failure_probability = test_dict[tst].get_failure_probability()

    #print(test_name,test_failure_probability)
    return (test_name,test_failure_probability)

def calculate_success_probability(test):
    return test.get_success_probability()

def calculate_failure_probability(test):
    return test.get_failure_probability()



