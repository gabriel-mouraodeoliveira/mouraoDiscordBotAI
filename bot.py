import os
import json

import discord
from discord import app_commands
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

# =========================
# Memória das conversas
# =========================

memoria_conversas = {}

# =========================
# Função de DM automática
# =========================

async def enviar_dm_por_nome(
    interaction,
    nome_usuario,
    mensagem
):

    for membro in interaction.guild.members:

        if membro.name.lower() == nome_usuario.lower():

            embed_dm = discord.Embed(
                title="📩 Nova mensagem",
                description=mensagem,
                color=discord.Color.blurple()
            )

            embed_dm.set_footer(
                text=f"Enviado por {interaction.user.name}"
            )

            await membro.send(
                embed=embed_dm
            )

            return membro

    return None

# =========================
# Configuração Discord
# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# =========================
# Evento Ready
# =========================

@bot.event
async def on_ready():

    try:

        synced = await bot.tree.sync()

        print(f"Slash commands sincronizados: {len(synced)}")
        print(f"Bot online como {bot.user}")

    except Exception as erro:
        print(erro)

# =========================
# /ping
# =========================

@bot.tree.command(
    name="ping",
    description="Testa se o bot está online"
)
async def ping(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🏓 Pong!",
        description="Bot online e funcionando.",
        color=discord.Color.green()
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# /ask
# =========================

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

        # Limita memória
        if len(historico) > 10:
            historico = historico[-10:]
            memoria_conversas[usuario_id] = historico

        chat = model.start_chat(
            history=historico
        )

        prompt_sistema = f"""
Você é um assistente Discord.

Quando o usuário pedir para enviar mensagem privada para alguém,
responda APENAS neste formato JSON:

{{
  "acao": "dm",
  "usuario": "NOME",
  "mensagem": "MENSAGEM"
}}

Se não for um pedido de ação,
responda normalmente.
"""

        response = chat.send_message(
            prompt_sistema + "\n\nUsuário: " + pergunta
        )

        texto = response.text

        # =========================
        # Tool Calling simples
        # =========================

        try:

            resposta_json = json.loads(texto)

            if resposta_json.get("acao") == "dm":

                usuario = resposta_json.get("usuario")
                mensagem = resposta_json.get("mensagem")

                membro = await enviar_dm_por_nome(
                    interaction,
                    usuario,
                    mensagem
                )

                if membro:

                    embed_tool = discord.Embed(
                        title="🤖 Ferramenta executada",
                        description=(
                            f"Mensagem enviada para "
                            f"{membro.mention}"
                        ),
                        color=discord.Color.green()
                    )

                    await interaction.followup.send(
                        embed=embed_tool
                    )

                    return

                else:

                    embed_tool = discord.Embed(
                        title="❌ Usuário não encontrado",
                        description=(
                            f"Não encontrei "
                            f"'{usuario}' no servidor."
                        ),
                        color=discord.Color.red()
                    )

                    await interaction.followup.send(
                        embed=embed_tool
                    )

                    return

        except:
            pass

        # =========================
        # Resposta normal
        # =========================

        historico.append({
            "role": "model",
            "parts": [texto]
        })

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

        # Continua enviando partes extras
        for parte in partes[1:]:

            extra_embed = discord.Embed(
                description=parte,
                color=discord.Color.blue()
            )

            await interaction.channel.send(
                embed=extra_embed
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

# =========================
# /reset
# =========================

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

# =========================
# /dm
# =========================

@bot.tree.command(
    name="dm",
    description="Envia mensagem privada para um usuário"
)
@app_commands.describe(
    usuario="Usuário que receberá a mensagem",
    mensagem="Mensagem que será enviada"
)
async def dm(
    interaction: discord.Interaction,
    usuario: discord.Member,
    mensagem: str
):

    await interaction.response.defer(
        ephemeral=True
    )

    try:

        embed_dm = discord.Embed(
            title="📩 Nova mensagem",
            description=mensagem,
            color=discord.Color.blurple()
        )

        embed_dm.set_footer(
            text=f"Enviado por {interaction.user.name}"
        )

        await usuario.send(
            embed=embed_dm
        )

        embed_confirmacao = discord.Embed(
            title="✅ Mensagem enviada",
            description=f"DM enviada para {usuario.mention}",
            color=discord.Color.green()
        )

        await interaction.followup.send(
            embed=embed_confirmacao,
            ephemeral=True
        )

    except Exception:

        embed_erro = discord.Embed(
            title="❌ Erro ao enviar DM",
            description=(
                "Não foi possível enviar a mensagem.\n"
                "O usuário pode estar com DMs fechadas."
            ),
            color=discord.Color.red()
        )

        await interaction.followup.send(
            embed=embed_erro,
            ephemeral=True
        )

# =========================
# Run Bot
# =========================

bot.run(DISCORD_TOKEN)