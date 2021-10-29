import discord
from discord import File
from discord.ext import commands, tasks
import string
import json
import requests
import sys
import time
import help_info
import random

class Tellme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def tellme(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("<https://go.umd.edu/UMDCTF-click_this_link_to_get_actual_flag>")

    @tellme.command()
    async def theflag(self, ctx):
        await ctx.channel.send("chungus is dissapointed")
    
    @tellme.command()
    async def ajoke(self,ctx):
        msg = ''
        with open('jokes.txt', 'r') as f:
            messages = f.read().split('\n')
            val = random.randrange(0, len(messages)-1)
            msg = messages[val]
        await ctx.channel.send(msg)

    @tellme.command()
    async def avatar(self,ctx):
        ctx.channel.send(file=File(f, 'chunga_diff.jpg'))

#################################### SETUP #####################################
def setup(bot):
    bot.add_cog(Tellme(bot))
