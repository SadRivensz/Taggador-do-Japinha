import os
import discord
from discord.ext import tasks
from datetime import time
from zoneinfo import ZoneInfo

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
FRIEND_ID = int(os.getenv("FRIEND_ID"))

# Horário de Fortaleza/Natal/Brasil: UTC-3
FUSO_BRASIL = ZoneInfo("America/Fortaleza")

intents = discord.Intents.default()


class MeuBot(discord.Client):
    async def setup_hook(self):
        ping_diario.start()

    async def on_ready(self):
        print(f"Bot conectado como {self.user}")


bot = MeuBot(intents=intents)


@tasks.loop(time=time(hour=0, minute=0, tzinfo=FUSO_BRASIL))
async def ping_diario():
    canal = bot.get_channel(CHANNEL_ID)

    if canal is None:
        print("Canal não encontrado. Verifique o CHANNEL_ID.")
        return

    await canal.send(f"<@{FRIEND_ID}> meia-noite chegou.")


@ping_diario.before_loop
async def antes_do_ping():
    await bot.wait_until_ready()


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN não foi configurado.")

bot.run(TOKEN)
