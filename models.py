import operations
class Component(object):

    def __init__(self, name, failure_prob):
        self._name = name
        self._failure_prob = failure_prob

    def get_failure_probability(self):
        return self._failure_prob

    def get_success_probability(self):
        return 1 - self.get_failure_probability()

class Test(object):

    def __init__(self, test_name,components):
        self._test_name = test_name
        self._components = components

    def get_failure_probability(self):
        return 1 - self.get_success_probability()

    def get_success_probability(self):
        prob = 1
        for component in self._components:
            prob *= component.get_success_probability()
        return prob

    def get_test_name(self):
        return self._test_name

    def get_expected_reward(self):
        return self.get_success_probability()* + operations.calculate_reward(1) +self.get_failure_probability()* + operations.calculate_reward(0)


'''class TestRun(object):
    def __init__(self,test,test_outcome):
        self._test = test
        self._test_outcome = test_outcome

    def get_test(self):
        return self._test

    def get_test_outcome(self):
        return self._test_outcome
'''

class State(object):
    def __init__(self,state_name,tests_run, test_left,state_outcomes):
        self._state_name = state_name
        self._tests_run = tests_run
        self._test_left = test_left
        self._state_outcomes = state_outcomes

    def get_state_info(self):
         return (self._state_name,self._tests_run,self._test_left,self._state_outcomes)

    def get_state_reward(self):
        state_reward=0
        for st_outcome in self._state_outcomes:
            state_reward += operations.calculate_reward(st_outcome)
        return state_reward

    def get_tests_run(self):
        return self._tests_run

    def get_tests_left(self):
        return self._tests_left

    def get_state_name(self):
        return self._state_name