# -*- coding: utf-8 -*-
"""Singleton Pattern

Singleton Pattern is one of the simplest design patterns.
This pattern involves a single class that is responsible for creating its own
objects while ensuring that only a single object is created.

"""
import abc
import threading


class SingletonMetaclass(type):
    """Metaclass for defining Singleton Classes

    You should use this class to create the ``Singleton`` class instead of
    instantiating it .

    Examples:
        >>> class Singleton(metaclass=SingletonMetaclass): ...

    """
    __instance_lock = threading.RLock()
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            with cls.__instance_lock:
                if cls.__instance is None:
                    cls.__instance = super(SingletonMetaclass, cls).\
                        __call__(*args, **kwargs)
        return cls.__instance

    @property
    def instance(cls):
        """Get instance

        Return instance of the Singleton.

        Returns:
            Singleton: the instance

        """
        return cls()


class AbstractSingletonMetaclass(abc.ABCMeta, SingletonMetaclass):
    """Metaclass for defining Abstract Singleton Classes

    Use this class to create an ``AbstractSingleton`` class.

    Extends the ``AbstractSingleton`` class to create a ``Singleton`` class.

    You should inherit this class instead of instantiating it.

    Examples:
        >>> class AbstractSingleton(metaclass=AbstractSingletonMetaclass):
        >>>     @abc.abstractmethod
        >>>     def example(self): ...
        >>>
        >>> class Singleton(AbstractSingleton):
        >>>     def example(self):
        >>>         pass

    """


class Singleton(metaclass=SingletonMetaclass):
    """Parent Class for a Singleton

    Inherit this class to Create a Singleton Class.

    SubClasses SHALL NOTE `This is a Singleton Class`.

    """
    _lock = threading.RLock()
