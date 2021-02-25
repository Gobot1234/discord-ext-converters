from typing import Any, Callable, Optional, Type, TypeVar
from typing_extensions import get_origin

from discord.ext.commands import Command, Context, Group, GroupMixin

from .model import CONVERTERS

__all__ = (
    "ConvertersCommand",
    "ConvertersGroup",
    "command",
    "group",
)


_CCT = TypeVar("_CCT", bound="ConvertersCommand")
_CGT = TypeVar("_CGT", bound="ConvertersGroup")


class ConvertersCommand(Command):
    async def _actual_conversion(
        self, ctx: Context, converter: Converter, argument: str, param: inspect.Parameter
    ) -> Any:
        converter = get_origin(converter) or converter
        converter = CONVERTERS.get(converter, converter)
        return await super()._actual_conversion(ctx, converter, argument, param)


class ConvertersGroupMixin(GroupMixin):
    def command(self, *args: Any, **kwargs: Any) -> Callable[..., _CCT]:
        return super().command(*args, cls=ConvertersCommand, **kwargs)

    def group(self, *args: Any, **kwargs: Any) -> Callable[..., _CCT]:
        return super().group(*args, cls=ConvertersGroup, **kwargs)


class ConvertersGroup(Group, ConvertersCommand):
    ...


def command(name: Optional[str] = None, cls: Type[_CCT] = ConvertersCommand, **attrs: Any) -> Callable[..., _CCT]:
    """A decorator that transforms a function into a :class:`.ConvertersCommand`."""

    def decorator(func: Callable[..., Any]) -> _CCT:
        if isinstance(func, ConvertersCommand):
            raise TypeError("Callback is already a command.")
        return cls(func, name=name, **attrs)

    return decorator


def group(name: Optional[str] = None, cls: Type[_CGT] = ConvertersGroup, **attrs: Any) -> Callable[..., _CGT]:
    """A decorator that transforms a function into a :class:`.ConvertersGroup`.

    This is similar to the :func:`.command` decorator but the ``cls`` parameter is set to :class:`.ConvertersGroup` by
    default.
    """

    return command(name=name, cls=cls, **attrs)
