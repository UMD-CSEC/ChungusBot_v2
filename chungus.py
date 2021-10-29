import discord
import os
import numpy as np
from discord.ext import commands, tasks
from itertools import cycle
from config_vars import *
import help_info
import requests
import shutil
from PIL import Image

################################ DATA STRUCTURES ###############################
bot = commands.Bot(command_prefix = '!')
bot.remove_command('help')
extensions = ['flag']

#################################### EVENTS ####################################
@bot.event # Show banner and add members to respective guilds in db
async def on_ready():
    print("\n|--------------------|")
    print(f"|  {bot.user.name} - Online   |")
    print(f"|  discord.py {discord.__version__}  |")
    print("|--------------------|")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="My code is somewhere"))

@bot.event # Displays error messages
async def on_command_error(ctx, error):
    msg = ""
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        msg += "Missing a required argument.  Do >help\n"
    if isinstance(error, commands.MissingPermissions):
        msg += "You do not have the appropriate permissions to run this command.\n"
    if isinstance(error, commands.BotMissingPermissions):
        msg += "I don't have sufficient permissions!\n"
    if msg == "":
        if not isinstance(error, commands.CheckFailure):
            msg += "Something went wrong.\n"
            print("error not caught")
            print(error)
            await ctx.send(msg)
    else:
        await ctx.send(msg)

@bot.event
async def on_message(ctx):
    if ctx.author.bot:
        return
    if str(ctx.channel.type) == "private":
        print(ctx.author.avatar_url)
        print(ctx.author.avatar)
        print(ctx.created_at)
        print("")
        if check1(str(ctx.author.avatar_url)) and check2(str(ctx.created_at)):
            await ctx.channel.send(flag)
        else:
            await ctx.channel.send("you are not worthy")
    elif str(ctx.channel) == "bot-box":
        await bot.process_commands(ctx)

################################ OTHER FUNCTIONS ###############################
@bot.command()
async def help(ctx, page=None):
    if page == None:
        emb = discord.Embed(description=help_info.help_page, colour=10181046)
    else:
        emb = discord.Embed(description=help_info.no_info, colour=10181046)
    emb.set_author(name='ChungusBot Help')
    await ctx.channel.send(embed=emb)

def check2(hmm):
    print(hmm)
    something = int(hmm.split(':')[-1].split('.')[0])
    if something > 45 and something < 50:
        return True
    return False

def check1(av):
    r = requests.get(str(av), stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        filename = str(str(av).split("/")[-1].split('?')[0])
        print(av)
        path = f'./downloaded_files/{filename}'
        with open(path,'wb') as f:
            shutil.copyfileobj(r.raw, f)

    img1 = list(Image.open('chungus.webp').convert("P").getdata())
    img2 = list(Image.open(path).convert("P").getdata())
    if len(img1) != len(img2):
        return False

    count = 0
    for i in range(len(img1)):
        if img1[i] == img2[i]:
            count += 1

    print(f'count = {count}\nnum_pixels = {i}\nstuff = {count / len(img1)}')
    if count / len(img1) > 0.8:
        return True
    return False

##################################### MAIN #####################################
if __name__ == '__main__': # Loads cog extentions and starts up the bot
    print("\n|-----------------------|\n| Loaded Cogs:          |")
    for extension in extensions:
        bot.load_extension('cogs.' + extension)
        print("|   - {}   {}|".format(extension.upper(), " "*(15-len(extension))))
    print("|-----------------------|\n")
    bot.run(discord_token)
