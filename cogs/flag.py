import discord
from discord.ext import commands, tasks
import string
import json
import requests
import sys
import time
import help_info

def in_dms():
    async def tocheck(ctx):
        # A check for ctf context specific commands
        if str(ctx.channel.type) == "private":
            return True
        else:
            await ctx.send("This command is only available over DM!")
            return False

    return commands.check(tocheck)

def in_channel():
    async def tocheck(ctx):
        # A check for ctf context specific commands
        if not str(ctx.channel.type) == "private":
            return True
        else:
            await ctx.send("This command is not available over DM!")
            return False

    return commands.check(tocheck)

class Flag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def flag(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("<https://go.umd.edu/UMDCTF-click_this_link_to_get_actual_flag>")

    @flag.command()
    @in_channel()
    async def printflag(self, ctx):
        await ctx.channel.send("chungus is dissapointed")

    @flag.command()
    @in_channel()
    async def rr(self, ctx):
        await ctx.channel.send("<https://bit.ly/1NbiVPe>")

    @flag.command()
    @in_dms()
    async def yeeee(self, ctx):
        tic = time.perf_counter()
        try:
            f = open(f'userfiles/{ctx.author.name}_time', 'r')
            stuff = f.read()
            count = len(stuff.split('\n'))

            if count == 2:
                f = open(f'userfiles/{ctx.author.name}_time', 'a')
                f.write(f'{tic}\n')
            else:
                await ctx.channel.send("Uh ohhh (count not 2)")
        except:
            await ctx.channel.send("Uh ohhh (no file)")

#################################### SETUP #####################################
def setup(bot):
    bot.add_cog(Flag(bot))
