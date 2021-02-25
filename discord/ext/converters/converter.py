from typing import TYPE_CHECKING, Generic, TypeVar

from typing_extensions import get_args

from discord.ext import commands

T = TypeVar("T")


class CustomConverter(commands.Converter, Generic[T]):
    def __init_subclass__(cls) -> None:
        from .core import CONVERTERS

        super().__init_subclass__()
        try:
            converter_for = get_args(cls.__orig_bases__[0])[0]
        except IndexError:
            raise TypeError(f"Converters should subclass CustomConverter using __class_getitem__") from None

        cls.converter_for = converter_for
        CONVERTERS[converter_for] = cls

    def __class_getitem__(cls, converter_for: ConverterTypes) -> CustomConverter[T]:
        if isinstance(converter_for, tuple) and len(converter_for) != 1:
            raise TypeError("CustomConverter only accepts one argument")
        return super().__class_getitem__(converter_for)

    if TYPE_CHECKING:

        async def convert(self, ctx: Context, argument: str) -> T:
            ...
