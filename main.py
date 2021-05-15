try:
    import conf
except ImportError:
    pass
import discord
from discord.ext import commands
import img_handler as imhl
import os, random
from random import choice

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = "#", intents=intents)

whitelist = {
    825345301560557608: {825345301560557608: "Bots / general"},
}

#Декоратор
def allowed_channel():
    async def predicate(ctx:commands.Context):
        #Если guild id и channel id валидны => True
        if ctx.guild.id in whitelist:
            if ctx.channel.id in whitelist[ctx.guild.id].keys():
                return True

        return False

    return commands.check(predicate)
        #False

    return

@bot.command(name = "msg")
async def command_qq(ctx, *args):
    global channel
    message = "".join(args)
    if ctx.channel.id == channel:
        msg = f'Сотрудник *[ДАННЫЕ УДАЛЕНЫ]* отправил сообщение в *[ДАННЫЕ УДАЛЕНЫ]*: ||{message}||'
        await ctx.channel.send(msg)


@bot.command(name = "about_me")
async def command_members(ctx):
    global channel
    if ctx.channel.id == channel:
        msg = f'Получены данные о сотруднике **{ctx.author.name}**: ||ID Сотрудника: {ctx.author.id}||'
        await ctx.channel.send(msg)

@bot.command(name = "repeat")
async def command_repeat(ctx, *args):
    global channel
    message = "".join(args)
    if ctx.channel.id == channel:
        msg = f'{message}'
        await ctx.channel.send(msg)

@bot.command(name = "member")
@allowed_channel()
async def get_member(ctx, member:discord.Member=None):
    msg = None
    global channel      
    if member:
        msg = f'Получены данные о сотруднике {member.name}: ||{"({member.nick})" if member.nick else ""} ID Сотрудника: {member.id}||'

    if msg == None:
        msg = "Отказано в доступе. Причина: низкий уровень доступа, попробуйте использовать другое значение"
    
    await ctx.channel.send(msg)

@bot.command(name="mk")
@allowed_channel()
async def fight(ctx, f1:discord.Member=None, f2:discord.Member=None):
    global channel
    if f1 and f2:
        await imhl.vs_create(f1.avatar_url, f2.avatar_url)    
        await ctx.channel.send( file=discord.File(os.path.join("./img/result.png")))
        msg = f"{f1.name} VS {f2.name}"
        await ctx.channel.send(msg)
    elif f1:
        await imhl.vs_create(f1.avatar_url, bot.user.avatar_url)    
        await ctx.channel.send( file=discord.File(os.path.join("./img/result.png")))
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        msg = f"{f1.name} VS twinkle_bot"
        await ctx.channel.send(msg)
    voice_channel = ctx.author.voice.channel
    print(voice_channel)
    if voice_channel:
        await voice_channel.connect()
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        await voice_client.play(discord.FFmpegPCMAudio(executable="./sound/ffmpeg.exe", source="./sound/mk.mp3"))

@bot.command(name="mka")
async def mk(ctx, f1:discord.Member=None, f2:discord.Member=None):
    global channel
    if ctx.channel.id == channel:
        if f1 and f2:
            await imhl.vs_create_animated(f1.avatar_url, f2.avatar_url)
            await ctx.channel.send( file=discord.File(os.path.join("./img/result.gif")))
        elif f1:
            await imhl.vs_create_animated(f1.avatar_url, bot.user.avatar_url)
            await ctx.channel.send( file=discord.File(os.path.join("./img/result.gif")))
            

@bot.command(name="join")
@allowed_channel()
async def join(ctx):
    msg = ""
    global channel
    
    voice_channel = ctx.author.voice.channel
    print(voice_channel)
    if voice_channel:
        msg = f"Подключаюсь к {voice_channel.name}"

        await voice_channel.connect()

@bot.command(name="leave")
async def leave(ctx):
    msg = ""
    global channel
    
    if ctx.channel.id == channel:
        voice_channel = ctx.author.voice.channel
        print(voice_channel)
        if voice_channel:
            msg = f"Отключаюсь {voice_channel.name}"
            await ctx.channel.send(msg)
            await voice_channel.disconnect()

@bot.command(name="ost")
async def ost(ctx):
    msg = ""
    global channel

    if ctx.channel.id == channel:
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        msg = f"SALO"

        await ctx.channel.send(msg)
        await voice_client.play(discord.FFmpegPCMAudio(executable="./sound/ffmpeg.exe", source="./sound/mk.mp3"))

@bot.command(name="fight")
allowed_channel()
async def random(ctx):
    msg = ""
    global channel
    voice_channel = ctx.author.voice.channel
    if voice_channel:
            f1 = ctx.author
            f2 = choice(ctx.author.voice.channel.members)
            await imhl.vs_create(f1.avatar_url, f2.avatar_url)    
            await ctx.channel.send( file=discord.File(os.path.join("./img/result.png")))
            msg = f"{f1.name} VS {f2.name}"
            await ctx.channel.send(msg)            
            await voice_channel.connect()
            voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            await voice_client.play(discord.FFmpegPCMAudio(executable="./sound/ffmpeg.exe", source="./sound/mk.mp3"))

bot.run(conf.bot_token)