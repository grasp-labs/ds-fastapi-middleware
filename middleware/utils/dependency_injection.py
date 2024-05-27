"""Module for injector pattern."""

from abc import ABC, abstractmethod
import asyncio
from typing import Type, Any, Callable


class WithLifeTime:
    """
    This class gathers lifetime definitions. The goal is to encapsulate
    lifetime management. Each definition implements `make` method that takes
    as input a callable that constructs the object and returns a callable
    that provides an object with its lifetime managed somehow.
    """

    class Base(ABC):
        """Base lifetime class"""

        @abstractmethod
        def make(self, builder_fn) -> Callable:
            """
            :param builder_fn: input factory function/callable that builds an object.
            :return: returns a callable that returns an object
            """
            raise NotImplementedError()

    class Transient(Base):
        """Transient lifetime: a new object is created each time"""

        def make(self, builder_fn) -> Callable:
            return builder_fn

    class Singleton(Base):
        """
        Singleton lifetime: only one instance is constructed, build at the
        first call then always provides this instance
        """

        def __init__(self):
            self._builder_fn = None
            self._instance = None

        def make(self, builder_fn) -> Callable:
            self._builder_fn = builder_fn
            return self  # return self, meaning the

        async def __call__(self, *args, **kwargs) -> Any:
            if self._instance is None:
                self._instance = await self._builder_fn(*args, **kwargs)
            return self._instance


class AppInjector(ABC):
    """
    A basic class to handle dependency injection. Module is responsible
    for managing the lifetime.
    """

    def __init__(self):
        self._factory_dict = {}

    def register(
        self,
        interface: Type,
        factory_coroutine,
        lifetime: WithLifeTime.Base = WithLifeTime.Transient(),
    ):
        """
        :param interface: with interface to register
        :param factory_coroutine: async builder callable
        :param lifetime: specific lifetime. By default it use transient
        lifetime which mean the build function is called
        everytime. Use WithLifeTime.Singleton to use a single
        instance instead
        :return:
        """
        if asyncio.iscoroutinefunction(factory_coroutine):
            self._factory_dict[self._key_from_type(interface)] = lifetime.make(
                factory_coroutine
            )

    async def get(self, interface: Type, *args, **kwargs) -> Any:
        """
        :param interface: interface require
        :param kwargs: parameters are passed as it to the factory func
        :return:
        """
        factory_coroutine = self._factory_dict[self._key_from_type(interface)]
        return await factory_coroutine(*args, **kwargs)

    @staticmethod
    def _key_from_type(t: Type) -> str:
        return str(t)


class AppInjectorModule(ABC):
    @abstractmethod
    def configure(self, injector: AppInjector):
        raise NotImplementedError("AppInjectorModule.configure is abstract")
