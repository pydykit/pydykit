import abc
from collections import namedtuple


class Integrator(abc.ABC):
    integrator_output = namedtuple("integrator_output", "residuum tangent")

    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)

    @abc.abstractmethod
    def calc_residuum_tangent(self):
        pass


class Midpoint(Integrator):
    def calc_residuum_tangent(self):
        system = self.manager.system
        states = system.states

        state_n = states.state_n
        state_n1 = states.state_n1

        e_n = system.get_e_matrix(state_n)
        e_n1 = system.get_e_matrix(state_n1)

        z_vector = system.get_z_vector(
            state=0.5 * (state_n + state_n1),
        )
        jacobian = 0.5 * system.get_jacobian(state=state_n1)

        j_matrix = system.get_j_matrix()

        residuum = (
            e_n1 @ state_n1
            - e_n @ state_n
            - self.manager.time_stepper.stepsize * j_matrix @ z_vector
        )
        tangent = e_n1 - self.manager.time_stepper.stepsize * j_matrix @ jacobian

        return self.integrator_output(
            residuum=residuum,
            tangent=tangent,
        )


class EulerImplicit(Integrator):
    def calc_residuum_tangent(self):
        system = self.manager.system
        states = system.states

        state_n = states.state_n
        state_n1 = states.state_n1

        e_n = system.get_e_matrix(state_n)
        e_n1 = system.get_e_matrix(state_n1)

        z_vector = system.get_z_vector(
            state=state_n1,
        )
        jacobian = 0.5 * system.get_jacobian(
            state=state_n1,
        )

        j_matrix = system.get_j_matrix()

        residuum = (
            e_n1 @ state_n1
            - e_n @ state_n
            - self.manager.time_stepper.stepsize * j_matrix @ z_vector
        )
        tangent = e_n1 - self.manager.time_stepper.stepsize * j_matrix @ jacobian

        return self.integrator_output(
            residuum=residuum,
            tangent=tangent,
        )


class EulerExplicit(Integrator):
    def calc_residuum_tangent(self):
        system = self.manager.system
        states = system.states

        state_n = states.state_n
        state_n1 = states.state_n1

        e_n = system.get_e_matrix(state_n)
        e_n1 = system.get_e_matrix(state_n1)

        z_vector = system.get_z_vector(
            state=state_n,
        )

        j_matrix = system.get_j_matrix()

        residuum = (
            e_n1 @ state_n1
            - e_n @ state_n
            - self.manager.time_stepper.stepsize * j_matrix @ z_vector
        )
        tangent = e_n1

        return self.integrator_output(
            residuum=residuum,
            tangent=tangent,
        )
