import copy


class System:

    def copy(self, state):
        new = copy.deepcopy(self)
        new.state = state
        return new
