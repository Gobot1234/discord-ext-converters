from __future__ import annotations

from typing import TYPE_CHECKING

from yarl import URL

from ..converter import CustomConverter

if TYPE_CHECKING:
    from discord.ext.commands import Context


class URLConverter(CustomConverter[URL]):
    def __init__(self, require_scheme: bool = True):
        self.require_scheme = require_scheme

    async def convert(self, ctx: Context, argument: str) -> URL:
        value = URL(argument)
        if not value.host or (self.require_scheme and not value.scheme):
            raise commands.BadArgument("{0} is not a valid URL".format(argument))

        return value
