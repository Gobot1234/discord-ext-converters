from __future__ import annotations

import inspect
import importlib
from typing import Any, Awaitable, Callable, Dict, TypeVar, Union
from types import new_class

import discord
from discord.ext.commands import Context, converter

from .converter import CustomConverter

BASE_CONVERTERS = {
    # fmt: off
    discord.CategoryChannel: converter.CategoryChannelConverter,
    discord.Colour:          converter.ColourConverter,
    discord.Emoji:           converter.EmojiConverter,
    discord.Game:            converter.GameConverter,
    discord.Invite:          converter.InviteConverter,
    discord.Member:          converter.MemberConverter,
    discord.Message:         converter.MessageConverter,
    discord.PartialEmoji:    converter.PartialEmojiConverter,
    discord.Role:            converter.RoleConverter,
    discord.TextChannel:     converter.TextChannelConverter,
    discord.User:            converter.UserConverter,
    discord.VoiceChannel:    converter.VoiceChannelConverter,
    # fmt: on
}

T = TypeVar("T")
_CDT = TypeVar("_CDT", bound="ConverterDict")


if discord.version_info >= (1, 7, 0):

    BASE_CONVERTERS.update(
        {
            # fmt: off
            discord.Guild:           converter.GuildConverter,
            discord.PartialMessage:  converter.PartialMessageConverter,
            # fmt: on
        }
    )


class ConverterDict(Dict[type, Union[converter.Converter, Callable[[str], Any]]]):
    def __init__(self):
        super().__init__(BASE_CONVERTERS)

    def __setitem__(self, key: type, value: Any) -> None:
        if not (callable(value) or issubclass(value, converter.Converter)):
            raise TypeError(f"Excepted value of type 'Converter' or built-in, received {value.__name__}")
        super().__setitem__(key, value)

    def set(self: _CDT, type_: type, converter: Union[converter.Converter, Callable[[str], Any]]) -> _CDT:
        self[type_] = converter
        return self

    def get(self, _type: Any, default: Any = None) -> Any:
        if inspect.isclass(_type):
            return super().get(_type, default)

        _converter = super().get(type(_type), default)

        if issubclass(_converter, CustomConverter):
            _converter = _converter[_type]

        return _converter

    def register(self, type: T) -> CustomConverter[T]:
        def predicate(
            converter: Union[Callable[[Context, str], Awaitable[T]], CustomConverter[T]]
        ) -> CustomConverter[T]:
            if inspect.iscoroutinefunction(converter):
                converter = new_class(
                    f"{type.__name__}Converter",
                    (CustomConverter[type],),
                    exec_body=lambda ns: ns.__setitem__("convert", lambda s, c, a: handler(c, a)),  # should mean it's a coroutine function.
                )

            self.set(type, converter)

            return converter

        return predicate

    def load(self, *converters: str) -> None:
        for c in converters:
            c = {"uuid": "uuid_", "zoneinfo": "zoneinfo_"}.get(c, c)
            importlib.import_module(f".custom_converters.{c}", package=__package__)


CONVERTERS = ConverterDict()
