# Discord bot import
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# my program import
# none

# main program
load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("接続しました！")

    # スラッシュコマンドを同期
    await bot.load_extension("Cogs.poll")

    await bot.tree.sync()
    print("グローバルコマンド同期完了！")

bot.run(os.environ['token'])