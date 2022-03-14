import discord
from discord.ext import commands
from discord import app_commands, ui


l_to_e = {
    "A": ("🇦", "🅰️"),
    "B": ("🇧", "🅱️"),
    "C": ("🇨",),
    "D": ("🇩", "▶️"),
    "E": ("🇪",),  # need moar!!!
    "F": ("🇫",),
    "G": ("🇬",),
    "H": ("🇭",),
    "I": ("🇮", "ℹ️", "1⃣"),
    "J": ("🇯",),
    "K": ("🇰",),
    "L": ("🇱",),
    "M": ("🇲", "Ⓜ️"),
    "N": ("🇳",),
    "O": ("🇴", "🅾️", "0⃣"),
    "P": ("🇵", "🅿️"),
    "Q": ("🇶",),
    "R": ("🇷",),
    "S": ("🇸", "5⃣"),  # kinda meh using 5 as S
    "T": ("🇹",),
    "U": ("🇺",),
    "V": ("🇻",),
    "W": ("🇼",),
    "X": ("🇽", "❎", "❌"),
    "Y": ("🇾",),
    "Z": ("🇿",),
    "0": ("0⃣", "🇴"),
    "1": ("1⃣", "🇮"),
    "2": ("2⃣",),
    "3": ("3⃣",),
    "4": ("4⃣",),
    "5": ("5⃣",),
    "6": ("6⃣",),
    "7": ("7⃣",),
    "8": ("8⃣",),
    "9": ("9⃣",),
    "?": ("❓", "❔"),
    "!": ("❗", "❕"),
    "#": ("#️⃣",),
    "*": ("*️⃣",),
    "10": ("🔟",),
    "AB": ("🆎",),
    "WC": ("🚾",),
    "CL": ("🆑",),
    "VS": ("🆚",),
    "NG": ("🆖",),
    "OK": ("🆗",),
    "ID": ("🆔",),
    "!!": ("‼️",),
    "!?": ("⁉️",),
    "UP": ("🆙",),
    "ABC": ("🔤",),
    "SOS": ("🆘",),
    "NEW": ("🆕",),
    "UP!": ("🆙",),
    # basically unreadable as a reaction
    # "COOL": ("🆒", ),
    # "FREE": ("🆓", ),
}

pl = {
    "Ą": "A",
    "Ć": "C",
    "Ę": "E",
    "Ł": "L",
    "Ń": "N",
    "Ó": "O",
    "Ś": "S",
    "Ź": "Z",
    "Ż": "Z",
}


def text_to_emojis(text: str) -> list[str]:
    text = text.upper()
    text = "".join([pl.get(x, x) for x in text])  # replace polish characters
    text = "".join(
        [x for x in text if x in l_to_e.keys()]
    )  # remove any characters we dont have emojis for

    out = []

    while text:
        r = 1  # number of chars consumed (for combos)

        for i in [3, 2, 1]:
            s = l_to_e.get(text[:i], ())
            e = next(
                (x for x in s if x not in out), None
            )  # get first element of tuple that isnt in out, None if all already are
            if e:
                r = i
                break

        if not e:
            return []

        out.append(e)
        if len(out) > 20:
            return []

        text = text[r:]

    return out


class React(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def react(
        self, ctx: commands.Context, *, text: str
    ):  # good luck using slash commands
        if not ctx.message.reference:
            return

        tid = ctx.message.reference.message_id
        await ctx.message.delete()
        target = await ctx.channel.fetch_message(tid)

        out = text_to_emojis(text)
        if not out:
            return False

        await target.clear_reactions()

        for x in out:
            await target.add_reaction(x)


class ReactionModal(ui.Modal):
    text = ui.TextInput(label="Tekst")

    def __init__(self, message: discord.Message):
        super().__init__(title="Dodaj reakcje")
        self.target = message

    async def on_submit(self, interaction: discord.Interaction):
        out = text_to_emojis(self.text.value)
        if not out:
            await interaction.response.send_message(
                "**Błąd: nie da się dodać takiej reakcji**", ephemeral=True
            )
            return

        await interaction.response.defer()

        await self.target.clear_reactions()

        for x in out:
            await self.target.add_reaction(x)


# i hate how these can't be in cogs
@app_commands.context_menu(name="Dodaj reakcje")
async def react_context(interaction: discord.Interaction, message: discord.Message):
    modal = ReactionModal(message)
    await interaction.response.send_modal(modal)


async def setup(bot: commands.Bot):
    cog = React(bot)

    bot.tree.add_command(react_context)

    await bot.add_cog(cog)
