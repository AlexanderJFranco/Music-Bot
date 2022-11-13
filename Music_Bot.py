
import discord
from discord.ext import commands
import yt_dlp
import os
import time


intents = discord.Intents.all()
client = commands.Bot(intents=discord.Intents.all(),command_prefix = "!")

#Run music based off of elements currently in Queue
def run(voice):

    #Only execute when there are elements within the queue
    while queue:

        #Perform check if song file currentky exists
        song_there = os.path.isfile("song.mp3")
        #If file exists delete song mp3
        if song_there:
            os.remove("song.mp3")

        #Initializa youtube donwload options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(queue[0])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        source = discord.FFmpegPCMAudio("song.mp3")
        voice.play(source, after = lambda e: print("Error")if e else client.loop.create_task(run(voice)))
        queue.pop()

#Command bot to join currnet voice channel
@client.command()
async def join(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='[VOICE CHANNEL NAME]')
    global queue
    queue = []
    await voiceChannel.connect()

#Command bot to play audio from supplied url
@client.command()
async def play(ctx, url:str):
    queue.append(url)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    while voice.is_playing():
        return
    run(voice)

#Command bot to display current video queue in chat
@client.command()
async def queue (ctx):
    pos = 1
    await ctx.send('Current Queue:')

    if queue :
        for url in queue:
            if pos == 1:
                prefix = 'Next Song: \n'
            else:
                prefix = '#' + str(pos)+' In Queue:\n'

            await ctx.send(prefix + url);
            pos += 1

    else:
        return

#Command bot to leave voice channel
@client.command()
async def leave (ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await voice.disconnect()
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

#Command bot to pause current song
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing")

#Command bot to stop current song and begin playing next song
@client.command()
async def next(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if queue:
        voice.stop()
    else:
        await ctx.send("Currently no audio is playing")
    time.sleep(1)
    run(voice)

#Command bot to resume currently paused song
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing :
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

#Command bot to stop playing audio
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()



client.run('[DISCORD TOKEN]')




