import discord
import os
import requests
import json
import random
from discord.ext import commands
import youtube_dl
from keep_alive import keep_alive

bot = commands.Bot(command_prefix="!")

loop = False

@bot.command()
async def botcommands(ctx):
	await ctx.channel.send("Availible Commands: hello, ping, server, loop, play, leave, pause, resume, stop")

@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")

@bot.command()
async def hello(ctx, arg):
    print(ctx.author)
    print(ctx.message)
    print(ctx.guild)

@bot.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

@bot.command()
async def loop(ctx):
    global loop
    if loop:
        loop = False
        await ctx.channel.send("Looping is now OFF")
    else:
        loop = True
        await ctx.channel.send("Looping is now ON")

@bot.command()
async def play(ctx, url : str):
    global loop
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
    try:
        await voiceChannel.connect()
    except Exception:
        pass
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

keep_alive()
bot.run(os.getenv("DISCORD_BOT"))