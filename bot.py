import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

##dentro do arquivo .env, utilize o Token fornecido ao criar o bot no discord.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
##dentro do arquivo .env, utilize a chave criada da API da IA que escolheu, 
##Neste projeto, estamos utilizando a API do GEMINI.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

## aqui você utiliza o modelo de IA da Google que preferir.
model = genai.GenerativeModel(
    "models/gemini-3.1-flash-lite"
)

memoria_conversas = {}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()

        print(f"Slash commands sincronizados: {len(synced)}")
        print(f"Bot online como {bot.user}")

    except Exception as erro:
        print(erro)

@bot.tree.command(
    name="ping",
    description="Testa se o bot está online"
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Pong! 🚀"
    )

@bot.tree.command(
    name="ask",
    description="Faça uma pergunta para a IA"
)
@app_commands.describe(
    pergunta="Pergunta que será enviada para a IA"
)
async def ask(
    interaction: discord.Interaction,
    pergunta: str
):
    await interaction.response.defer()

    try:

        usuario_id = str(interaction.user.id)

        if usuario_id not in memoria_conversas:
            memoria_conversas[usuario_id] = []

        historico = memoria_conversas[usuario_id]

        historico.append({
            "role": "user",
            "parts": [pergunta]
        })

        chat = model.start_chat(
            history=historico
        )

        response = chat.send_message(
            pergunta
        )

        texto = response.text

        historico.append({
            "role": "model",
            "parts": [texto]
        })

        # if len(texto) > 1900:
        #     texto = texto[:1900] + "..."

        partes = [
            texto[i:i+3900]
            for i in range(0, len(texto), 3900)
        ]

        embed = discord.Embed(
            title="🤖 Resposta da IA",
            description=partes[0],
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📌 Pergunta",
            value=pergunta,
            inline=False
        )

        embed.set_footer(
            text="Mourao AI Bot"
        )

        await interaction.followup.send(
            embed=embed
        )

    except Exception as erro:
        embed = discord.Embed(
            title="❌ Erro",
            description=str(erro),
            color=discord.Color.red()
        )

        await interaction.followup.send(
        embed=embed
        )

        for parte in partes[1:]:
            extra_embed = discord.Embed(
                description=parte,
                color=discord.Color.blue()
            )

            await interaction.channel.send(
                embed=extra_embed
            )

@bot.tree.command(
    name="reset",
    description="Reseta a memória da conversa com a IA"
)
async def reset(
    interaction: discord.Interaction
):

    usuario_id = str(interaction.user.id)

    if usuario_id in memoria_conversas:
        memoria_conversas[usuario_id] = []

    embed = discord.Embed(
        title="🧠 Memória resetada",
        description="A conversa anterior foi apagada com sucesso.",
        color=discord.Color.green()
    )

    await interaction.response.send_message(
        embed=embed
    )
            
bot.run(DISCORD_TOKEN)