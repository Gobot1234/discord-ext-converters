import dataclasses
import re

from discord.ext.commands import BadArgument, Context, CommandError
from discord.utils import get
from discord.ext.converters import ConvertersBot

bot = ConvertersBot(command_prefix="!")
bot.converters.load("range", "regex")


@dataclasses.dataclass
class GameInfo:
    name: str
    price: float
    description: str


games = [
    GameInfo(name="Cool Game", price=2.99, description="A really cool game with guns"),
    GameInfo(name="Bad Game", price=299.99, description="A game where everything is lame"),
    GameInfo(name="Somewhat OK Game", price=-0.99, description="We give you 99 cents when you buy this game"),
]


def convert_game_info(arg: str) -> GameInfo:
    game_info = get(games, name=arg)
    if game_info:
        return game_info

    raise BadArgument(f"Game {arg!r} not found!")


bot.converters.set(GameInfo, convert_game_info)


@bot.command()
async def info(ctx: Context, *, game: GameInfo):
    await ctx.send(
        f"""```
Name: {game.name}
Price: ${game.price}
Description: {game.description}
```"""
    )


@info.error
async def handle_info(ctx: Context, error: CommandError):
    if isinstance(error, BadArgument):
        await ctx.send(error)


@bot.command()
async def greet(ctx, num: range[1, 4]):
    choice_list = ["", "Hello!", "Heya!", "Oh, it's you again."]
    await ctx.send(choice_list[num])


@bot.command()
async def match(ctx, text: re.Match[r"hello\d+"]):
    # slight caveat, it uses compile to match, which would return re.Match, not re.Pattern
    await ctx.send(f"`{text.group(0)}` is a match!")


bot.run("token")
