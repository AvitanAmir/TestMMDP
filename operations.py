def calculate_reward(test_outcome):
    if test_outcome == 0:
        return 1
    else:
        return 0.1

def calculate_success_probability(test):
    pass

def calculate_failure_probability(test):
    pass

def calculate_success_entropy(test):
    pass

def calculate_failure_entropy(test):
    pass

def calculate_test_entropy(test):
    return calculate_success_probability(test) * calculate_success_entropy(test) + calculate_failure_probability(test) * calculate_failure_entropy(test)

