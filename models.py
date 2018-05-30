
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

class TestRun(object):
    def __init__(self,test,test_outcome):
        self._test = test
        self._test_outcome = test_outcome

    def get_test(self):
        return self._test

    def get_test_outcome(self):
        return self._test_outcome


class State(object):
    def __init__(self,tests_run, test_left):
        self._tests_run = tests_run
        self._test_left = test_left