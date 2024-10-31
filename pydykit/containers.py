from dependency_injector import containers, providers

from . import managers


class Container(containers.DeclarativeContainer):

    manager_factory = providers.Factory(managers.Manager)
