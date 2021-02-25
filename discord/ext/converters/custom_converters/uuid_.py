from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from ..converter import CustomConverter

if TYPE_CHECKING:
    from discord.ext.commands import Context


class UUIDConverter(CustomConverter[UUID]):
    async def convert(self, ctx: Context, argument: str) -> UUID:
        try:
            value = UUID(argument)
        except ValueError:
            raise commands.BadArgument(f"{argument} is not a valid UUID")

        return value
