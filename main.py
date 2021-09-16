import pytube
import discord
import shutil
import asyncio
from discord.ext import commands
import os
import glob

bot = commands.Bot(command_prefix="%", description="The description")
loop_s = False
play_s = False
file_name = ''
queue = -1
play_queue = 0

def endsong(path):
    global loop_s
    if not loop_s:
        os.remove(path)

@bot.event
async def  on_ready():
    print("Ready !")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def play(ctx,url):
    global loop_s, play_s, file_name, queue_name, queue, play_queue
    channel = ctx.author.voice.channel
    try:
        try:
            await channel.connect()
            filelist = glob.glob('queue/*.mp4')
            for f in filelist:
                os.remove(f)
        except:
            pass
        server = ctx.message.guild
        voice_channel = server.voice_client
        print(server, voice_channel)
        print('joined')
        queue += 1

        print(queue, play_queue)
        while voice_channel.is_playing() or play_queue != queue:
            await asyncio.sleep(1)
        else:
            play_s = True

            t = pytube.YouTube(url).streams.filter(only_audio=True)
            time = pytube.YouTube(url).length
            print('length :', time)
            if time > 900:
                t[0].download("queue/")
                file_name = glob.glob("queue/*.mp4")[0]
                await ctx.send('playing '+t[0].title)
                print(file_name)
                print('downloaded')

                audio_source = discord.FFmpegPCMAudio(file_name)
                voice_channel.play(audio_source,after=lambda x : endsong(file_name))
                while play_s:
                    if voice_channel.is_playing() :
                        await asyncio.sleep(1)
                    elif not loop_s:
                        play_s = False
                    else:
                        audio_source = discord.FFmpegPCMAudio(file_name)
                        voice_channel.play(audio_source, after=lambda x : endsong(file_name))
                        print('played')
                play_queue += 1
                if play_queue > queue:
                    queue = -1
                    play_queue = 0
                    print(queue, play_queue)    
    except:
        pass

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command()
async def loop(ctx):
    global loop_s
    server = ctx.message.guild
    voice_channel = server.voice_client
    if voice_channel.is_playing():
        if loop_s == False:
            loop_s = True
            await ctx.send('loop is on')
        else:
            loop_s = False
            await ctx.send('loop is off')
    else:
        await ctx.send("nah it not work")

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    filelist = glob.glob('queue/*.mp4')
    for f in filelist:
        os.remove(f)
@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    queue = -1
    play_queue = 0

print('starting')

bot.run("NjEyOTY5NDk5OTkzNDQwMjU4.XVqGVQ.TNeSzamidiu7Y3k9bA1TlHsYbys")
