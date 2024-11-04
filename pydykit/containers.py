from dependency_injector import containers, providers

from . import factories, managers


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    state = providers.Singleton()

    manager = providers.Singleton(managers.Manager)

    system = providers.Factory(
        factories.SystemFactory.get(),
        key=getattr(config, "system").class_name,
        manager=manager,
        state=state,
        **config.kwargs,
    )

    simulator = providers.Factory(
        factories.SimulatorFactory.get(),
        key=getattr(config, "simulator").class_name,
        manager=manager,
        **config.kwargs,
    )

    integrator = providers.Factory(
        factories.IntegratorFactory.get(),
        key=getattr(config, "integrator").class_name,
        manager=manager,
        **config.kwargs,
    )

    time_stepper = providers.Factory(
        factories.TimeStepperFactory.get(),
        key=getattr(config, "time_stepper").class_name,
        manager=manager,
        **config.kwargs,
    )

    result = providers.Factory(
        factories.result_factory.get(),
        key="results",
        manager=manager,
        **config.kwargs,
    )
