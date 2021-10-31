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
bot = commands.Bot(command_prefix = 'Oh Lord Chungus please ')
bot.remove_command('help')
extensions = ['tellme']

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
        msg += "Missing a required argument. Display the help menu to see what commands you can run\n"
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
    await bot.process_commands(ctx)
    if ctx.author.bot:
        return
    commands = ["help", "tellme ajoke", "tellme", "tellme theflag"]
    start = 'Oh Lord Chungus please '
    if str(ctx.channel.type) == "private" and start in str(ctx.content) and str(ctx.content).split(start)[1] in commands:
        first_check, msg = check1(str(ctx.author.avatar_url))
        if first_check:
            if check2(str(ctx.created_at)):
                await ctx.channel.send(f'`{flag}`')
            else:
                await ctx.channel.send("not the right time my friend")
        else:
            if len(msg) > 0:
                await ctx.channel.send(msg)
            elif msg == "nope":
                await ctx.channel.send("no flag for you :pensive:")

################################ OTHER FUNCTIONS ###############################
@bot.command()
async def help(ctx, page=None):
    if page == None:
        emb = discord.Embed(description=help_info.help_page, colour=10181046)
    else:
        emb = discord.Embed(description=help_info.no_info, colour=10181046)
    emb.set_author(name='ChungusBot v2 Help')
    await ctx.channel.send(embed=emb)

def check2(hmm):
    something = int(hmm.split(':')[-1].split('.')[0])
    if (something > 45 and something < 50) or (something > 14 and something < 19):
        return True
    return False

def check1(av):
    r = requests.get(str(av), stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        filename = str(str(av).split("/")[-1].split('?')[0])
        path = f'./downloaded_files/{filename}'
        with open(path,'wb') as f:
            shutil.copyfileobj(r.raw, f)

    img1 = list(Image.open('chungus_changed.jpg').convert("1").getdata())
    img2 = list(Image.open(path).convert("1").getdata())
    if len(img1) != len(img2):
        return False, ""

    count = 0
    for i in range(len(img1)):
        if img1[i] == img2[i]:
            count += 1

    message = "Percentage of pixels correct: " + str(count / len(img1))
    if count / len(img1) > 0.92:
        return True, message
    elif count / len(img1) > 0.6:
        return False, message
    else:
        return False, "nope"

##################################### MAIN #####################################
if __name__ == '__main__': # Loads cog extentions and starts up the bot
    print("\n|-----------------------|\n| Loaded Cogs:          |")
    for extension in extensions:
        bot.load_extension('cogs.' + extension)
        print("|   - {}   {}|".format(extension.upper(), " "*(15-len(extension))))
    print("|-----------------------|\n")
    bot.run(discord_token)
