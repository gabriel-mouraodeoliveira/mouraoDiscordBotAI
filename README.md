# 🤖 Mourao Discord AI Bot

Bot para Discord integrado com Google Gemini AI.

O projeto permite:
- responder perguntas usando IA
- interagir em tempo real no Discord
- servir como base para futuras integrações:
  - geração de imagens
  - memória de conversa
  - slash commands
  - deploy 24h
  - moderação inteligente

---

# 🚀 Tecnologias

- Python 3.11+
- discord.py
- Google Gemini API
- python-dotenv

---

# 📦 Instalação

## 1. Clone o projeto

```bash
git clone https://github.com/SEU_USUARIO/mouraoDiscordBotAI.git
```

---

## 2. Entre na pasta

```bash
cd mouraoDiscordBotAI
```

---

## 3. Crie ambiente virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Instale dependências

```bash
pip install -r requirements.txt
```

---

# 🔑 Configuração

Crie um arquivo:

```bash
.env
```

Use este modelo:

```env
DISCORD_TOKEN=SEU_TOKEN
GEMINI_API_KEY=SUA_API_KEY
```

---

# 🤖 Criando o Bot no Discord

1. Acesse:
https://discord.com/developers/applications

2. Crie uma aplicação

3. Vá em:
- Bot
- Add Bot

4. Ative:
- MESSAGE CONTENT INTENT

5. Gere URL em:
- OAuth2
- URL Generator

Scopes:
- bot
- applications.commands

---

# 🧠 Criando API Key Gemini

Acesse:

https://aistudio.google.com/app/apikey

Crie:
- API Key

---

# ▶️ Executando

```bash
python bot.py
```

Se tudo estiver correto:

```bash
Bot online como NomeDoBot
```

---

# 💬 Comandos

## Perguntar para IA

```bash
!ask explique o que é machine learning
```

## Teste de conexão

```bash
!ping
```

---

# 📁 Estrutura

```bash
mouraoDiscordBotAI/
│
├── bot.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🔒 Segurança

O arquivo `.env` NÃO deve ser enviado ao GitHub.

Ele já está protegido via `.gitignore`.

---

# 🛣️ Roadmap

## Próximas melhorias

- [ ] Slash Commands
- [ ] Embeds personalizados
- [ ] Geração de imagens
- [ ] Memória/contexto
- [ ] Deploy 24h
- [ ] Painel web
- [ ] Banco de dados

---

# 📜 Licença

MIT License

---

# 👨‍💻 Autor

Gabriel Mourão
