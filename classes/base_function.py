from abc import ABCMeta, abstractmethod, abstractproperty


class BaseFunction:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __log_event(self):
        raise NotImplementedError("Необходимо реализовать метод __log_event")


    @abstractmethod
    def get_function_info(self):
        raise NotImplementedError("Необходимо реализовать метод get_function_info")

    @abstractmethod
    def execute_function(self):
        raise NotImplementedError("Необходимо реализовать метод execute_function")