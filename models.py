

class Component(object):

    def __init__(self, name, failure_prob):
        self._name = name
        self._failure_prob = failure_prob

    def get_failure_probability(self):
        return self._failure_prob

    def get_success_probability(self):
        return 1 - self.get_failure_probability()

class Test(object):

    def __init__(self, components):
        self._components = components

    def get_failure_probability(self):
        return 1 - self.get_success_probability()

    def get_success_probability(self):
        prob = 1

        for component in self._components:
            prob *= component.get_success_probability()

        return prob
