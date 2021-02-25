from __future__ import annotations

import inspect
import re
from typing import TYPE_CHECKING

from typing_extensions import get_args

from ..converter import CustomConverter

if TYPE_CHECKING:
    from discord.ext.commands import Context


class MatchConverter(CustomConverter[re.Match]):
    async def convert(self, ctx: Context, argument: str) -> re.Match:
        try:
            param: inspect.Parameter = inspect.currentframe().f_back.f_locals["param"]
        except KeyError:
            raise TypeError(f"{self.__class__.__name__} cannot be used manually.") from None

        pattern = get_args(param.annotation)[0]

        match = re.fullmatch(pattern, argument)
        if match is None:
            raise commands.BadArgument(f"{argument} does not match the provided pattern")

        return match
