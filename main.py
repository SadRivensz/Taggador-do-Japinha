import os
import discord
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")
FRIEND_ID = int(os.getenv("FRIEND_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()


class MeuBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)

        # Copia os comandos globais para o servidor específico
        self.tree.copy_global_to(guild=guild)

        # Sincroniza os comandos diretamente nesse servidor
        await self.tree.sync(guild=guild)

        print("Comandos slash sincronizados no servidor.")

    async def on_ready(self):
        print(f"Bot conectado como {self.user}")
        print("Bot online esperando os comandos /japinha e /brad.")


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


@bot.tree.command(name="brad", description="Manda os emotes do Brad no canal específico")
async def brad(interaction: discord.Interaction):
    canal = bot.get_channel(CHANNEL_ID)

    if canal is None:
        await interaction.response.send_message(
            "Não consegui encontrar o canal configurado. Verifique o CHANNEL_ID.",
            ephemeral=True
        )
        return

    mensagem = (
        "<:bradBA:1405185253030756374> "
        "<:bradBless:1405762786377601054> "
        "<:bradFlu:1410784279780130816> "
        "<:bradIPHONE:1437251628372852876> "
        "<:bradKQ:1419466403462778900> "
        "<:bradSparrow:1440148797073129564> "
        "<:bradfla:1402800738194686063> "
        "<:bradnatal:1453390129954816235> "
        "<:branana:1078395075849101373>"
    )

    await canal.send(mensagem)

    await interaction.response.send_message(
        "Emotes enviados no canal configurado.",
        ephemeral=True
    )


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN não foi configurado.")

bot.run(TOKEN)
