import os
import discord
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")
FRIEND_ID = int(os.getenv("FRIEND_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()


class MeuBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Comandos slash sincronizados.")

    async def on_ready(self):
        print(f"Bot conectado como {self.user}")
        print("Bot online esperando o comando /japinha.")


bot = MeuBot()


@bot.tree.command(name="japinha", description="Marca o Japinha em um canal específico")
async def japinha(interaction: discord.Interaction):
    canal = bot.get_channel(CHANNEL_ID)

    if canal is None:
        await interaction.response.send_message(
            "Não consegui encontrar o canal configurado. Verifique o CHANNEL_ID.",
            ephemeral=True
        )
        return

    await canal.send(f"<@{FRIEND_ID}>")

    await interaction.response.send_message(
        "Japinha marcado no canal configurado.",
        ephemeral=True
    )


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN não foi configurado.")

bot.run(TOKEN)
