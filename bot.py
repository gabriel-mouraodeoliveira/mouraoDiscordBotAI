import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🚀")

@bot.command()
async def ask(ctx, *, pergunta):
    mensagem = await ctx.send("Pensando... 🤔")

    try:
        response = model.generate_content(
            pergunta
        )

        texto = response.text

        if len(texto) > 1900:
            texto = texto[:1900] + "..."

        await mensagem.edit(
            content=texto
        )

    except Exception as erro:
        await mensagem.edit(
            content=f"Erro: {erro}"
        )

bot.run(DISCORD_TOKEN)