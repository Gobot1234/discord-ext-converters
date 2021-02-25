from __future__ import annotations

from typing import TYPE_CHECKING

from ..converter import CustomConverter

if TYPE_CHECKING:
    from discord.ext.commands import Context


class ComplexConverter(CustomConverter[complex]):
    async def convert(self, ctx: Context, argument: str) -> complex:
        try:
            value = complex(argument.lower().replace("i", "j"))
        except ValueError:
            raise commands.BadArgument(f"{argument} is not a complex number")

        return value
