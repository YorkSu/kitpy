import abc
import pytest
from kitpy.common.pattern import singleton


Singleton = singleton.Singleton
SingletonMetaclass = singleton.SingletonMetaclass
AbstractSingletonMetaclass = singleton.AbstractSingletonMetaclass


class TestSingleton:
    def test_singleton(self):
        a = Singleton()
        b = Singleton()
        assert a is b

    def test_singleton_instance(self):
        a = Singleton()
        b = Singleton.instance
        assert a is b

    def test_singleton_metaclass(self):
        class Apple(metaclass=SingletonMetaclass):
            def buy(self):
                return True

        a = Apple()
        b = Apple.instance
        assert a is b
        assert a.buy()

    def test_abstract_singleton_metaclass(self):
        class BaseApple(metaclass=AbstractSingletonMetaclass):
            @abc.abstractmethod
            def buy(self): ...

        class Apple(BaseApple):
            def buy(self):
                return True

        with pytest.raises(TypeError):
            a = BaseApple()

        a = Apple()
        b = Apple.instance
        assert a is b
        assert a.buy()

