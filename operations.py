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

