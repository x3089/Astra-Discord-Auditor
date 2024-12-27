import discord
from discord.ext import commands
import requests

# Configuración inicial
TOKEN = 'TU_BOT_TOKEN'  # Reemplaza con tu token de bot de Discord
PREFIX = '!'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


print("""
██████╗ ███████╗████████╗██████╗  █████╗ 
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
███████║███████╗   ██║   ██████╔╝███████║
██╔══██║╚════██║   ██║   ██╔══██╗██╔══██║
██║  ██║███████║   ██║   ██║  ██║██║  ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
""")

@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name} (ID: {bot.user.id})')

@bot.command()
async def scan(ctx, server_id: int):
    """Comando para escanear información del servidor Discord."""
    try:
        guild = await bot.fetch_guild(server_id)
        print(f'Servidor: {guild.name} (ID: {guild.id})')

        print('Miembros del servidor:')
        async for member in guild.fetch_members(limit=10):  # Limitar la cantidad para evitar overload
            print(f'{member.name} - {member.id}')
        
        print('Canales del servidor:')
        for channel in guild.text_channels:
            print(f'#{channel.name} (ID: {channel.id})')

    except Exception as e:
        print(f'Error al escanear el servidor: {e}')

@bot.command()
async def extract(ctx, server_id: int, channel_id: int):
    """Comando para extraer mensajes y datos de un canal privado o público."""
    try:
        channel = await bot.fetch_channel(channel_id)
        print(f'Extrayendo mensajes de #{channel.name} (ID: {channel.id})')

        async for message in channel.history(limit=100):
            print(f'{message.author.name}: {message.content}')

    except Exception as e:
        print(f'Error al extraer mensajes: {e}')

@bot.event
async def on_message(message):
    """Captura mensajes entrantes para monitoreo de actividad sospechosa."""
    if message.author == bot.user:
        return

    print(f'{message.author}: {message.content}')

@bot.command()
async def helpme(ctx):
    """Comando para mostrar los comandos disponibles."""
    help_text = f"""
    **Comandos disponibles:**
    - `{PREFIX}scan <server_id>`: Escanea un servidor por información.
    - `{PREFIX}extract <server_id> <channel_id>`: Extrae mensajes de un canal específico.
    - `{PREFIX}helpme`: Muestra este mensaje.
    """
    await ctx.send(help_text)

# Ejecutar el bot
bot.run(TOKEN)
