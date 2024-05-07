# import numpy as np
# import abc

# # class System(abc.ABC):
# #     @property


# from abc import ABC, abstractmethod


# class BaseController(ABC):
#     @property
#     @abstractmethod
#     def path(self) -> str: ...


# class Controller(BaseController):
#     path = "/home"


# class Controller2(BaseController):
#     def __init__(self):
#         self.path = "asd"


# # Instead of an elipsis, you can add a docstring for clarity
# class AnotherBaseController(ABC):
#     @property
#     @abstractmethod
#     def path(self) -> str:
#         """
#         :return: the url path of this controller
#         """


# from abc import ABC


# class Controller5(ABC):
#     path: str = NotImplemented


# class MyController5(Controller5):
#     path = "/home"
