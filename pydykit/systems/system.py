import copy


class System:
    # inspired by mixin classes approach
    def copy(self, state):
        new = copy.deepcopy(self)
        new.state = state
        return new
