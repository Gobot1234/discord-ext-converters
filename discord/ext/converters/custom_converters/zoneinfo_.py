from __future__ import annotations

from typing import TYPE_CHECKING

try:
    import zoneinfo
except ImportError:
    try:
        from backports import zoneinfo
    except ImportError:
        raise RuntimeError("Could not import zoneinfo module.")


from ..converter import CustomConverter

if TYPE_CHECKING:
    from discord.ext.commands import Context


class ZoneInfoConverter(CustomConverter[zoneinfo.ZoneInfo]):
    async def convert(self, ctx: Context, argument: str) -> zoneinfo.ZoneInfo:
        try:
            value = zoneinfo.ZoneInfo(argument)
        except (ValueError, zoneinfo.ZoneInfoNotFoundError):
            raise commands.BadArgument(f"{argument} is not a valid IANA time zone")

        return value
