import discord
from discord.ext import commands
from discord import app_commands

import io
from bs4 import BeautifulSoup


class Img(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def make_safe_filename(self, s):
        return "".join((c if c.isalnum() or c == "." else "_") for c in s)

    @app_commands.command(description="Wyszukuje hujowo małe obrazki")
    @app_commands.describe(q="Wyszukiwana fraza")
    async def img(self, interaction: discord.Interaction, q: str):
        await interaction.response.defer()

        try:
            async with self.bot.http._HTTPClient__session.get(
                "https://www.google.com/search",
                params={"tbm": "isch", "q": q},
                headers={"User-Agent": "degenerat-bot/2137"},
            ) as r:
                if not r.ok:
                    raise Exception(f"**Error:** google search status code {r.status}")

                text = await r.text()

            soup = BeautifulSoup(text, "lxml")

            img = [x["src"] for x in soup.select("img")[1:4]]

            files = []

            for i, url in enumerate(img):
                async with self.bot.http._HTTPClient__session.get(url) as r:
                    if r.ok:
                        files.append(
                            discord.File(
                                io.BytesIO(await r.read()),
                                f"{self.make_safe_filename(q)}{i}.jpg",
                            )
                        )

            if not files:
                await interaction.followup.send(
                    f"**Brak wyników wyszukiwania dla:** `{q}`"
                )
                return

            await interaction.followup.send(files=files)

        except Exception as e:
            await interaction.followup.send(f"**Coś poszło nie tak:** {e}")

    # TODO: uncomment once context commands in cogs get fixed
    #
    # @app_commands.context_menu(name="Image Search")
    # async def img_context(
    #     self, interaction: discord.Interaction, message: discord.Message
    # ):
    #     if message.content:
    #         await self.img.callback(self, interaction, message.content)
    #     else:
    #         await interaction.response.send_message(
    #             "**Błąd: Wiadomość bez treści**", ephemeral=True
    #         )


def setup(bot: commands.Bot):
    bot.add_cog(Img(bot))
