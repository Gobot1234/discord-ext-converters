from discord.ext.commands.bot import AutoShardedBot, Bot, BotBase

from .core import CONVERTERS, ConvertersGroupMixin


class ConvertersBotBase(BotBase, ConvertersGroupMixin):
    @property
    def converters(self) -> ConverterDict:
        return CONVERTERS


class ConvertersBot(Bot, ConvertersBotBase):
    ...


class AutoShardedConvertersBot(AutoShardedBot, ConvertersBotBase):
    ...
