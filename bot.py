import discord.ext
import datetime
from random import randint
import json
import os
from asyncio import sleep
from discord import ActivityType
import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import requests
import io
from Cogs import music
import asyncio


TokenFile = open("./data/Token.txt", "r")
TOKEN = TokenFile.read()


OWNERID = 505750675758514197


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", case_insensitive=True, intents=intents)
bot.remove_command('help')
now = datetime.datetime.now()


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


@bot.event
async def on_ready():
    print("Bot is ready")
    while True:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name="за булочками", type=ActivityType.watching))
        await sleep(15)
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name="за холодильником", type=ActivityType.watching))
        await sleep(15)
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name="за телевизором", type=ActivityType.watching))
        await sleep(15)
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name="за диваном", type=ActivityType.watching))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        emb = discord.Embed(description=f'Данной команды не существует! :person_shrugging:', colour=discord.Color.red())
        await ctx.send(embed=emb)

    if isinstance(error, commands.MemberNotFound):
        emb = discord.Embed(description=f'Участник не найден! :person_shrugging:', colour=discord.Color.red())
        await ctx.send(embed=emb)

    if isinstance(error, commands.CommandInvokeError):
        emb = discord.Embed(description=f'**Недостатончо прав**, чтобы выполнить это действие! :person_shrugging:', colour=discord.Color.red())
        await ctx.send(embed=emb)

    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description=f'**Вот хитрюга!** Ты не админ чтобы использовать эту команду :smirk:', colour=discord.Color.red())
        await ctx.send(embed=emb)


@bot.event
async def on_message(message):
    with open('lvl.json', 'r') as f:
        global users
        users = json.load(f)

    async def ziro_exp(users, user):
        if users[user]['exp'] == 1000:
            users[user]['exp'] = 0
            users[user]['lvl'] += 1

    async def update_data(users, user):
        if not user in users:
            users[user] = {}
            users[user]['exp'] = 0
            users[user]['lvl'] = 1
            users[user]['pred'] = 0
            users[user]['ducreator'] = 1
            users[user]['duplayer'] = 1
            users[user]['duwins'] = 0

    async def add_exp(users, user, exp):
        if message.author.bot:
            pass
        else:
            if expp == 0:
                users[user]['exp'] = 1
            elif expp > 0:
                users[user]['exp'] += exp


    async def add_lvl(users, user):
        global expp
        lvl = users[user]['lvl']
        expp = users[user]['exp']
        if expp == 999:
            expp = 1
            await message.channel.send(f'{message.author.mention} повысил свой уровень!')
            users[user]['exp'] = 1

    await update_data(users, str(message.author.id))
    await add_lvl(users, str(message.author.id))
    await add_exp(users, str(message.author.id), 1)
    await ziro_exp(users, str(message.author.id))
    with open('lvl.json', 'w') as f:
        json.dump(users, f)
    await bot.process_commands(message)


@bot.command(name='help', aliases=['commands', '', 'command'])
async def help(ctx, command=""):
    if command.lower() == "repeat":
        msg = f"**`#repeat (текст)`** - повторить текст"
        emb = discord.Embed(title=f"Repeat:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "loop":
        msg = f"**`#loop (текст) (кол-во раз)`** - повторить текст некоторое кол-во раз"
        emb = discord.Embed(title=f"Loop:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "about":
        msg = f"**`#about @id`** - информация о человеке, @id которого указано. Если @id человека не указано, выведется информация о человеке,написавшем команду"
        emb = discord.Embed(title=f"About:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "kick":
        msg = f"**`#kick @id (причина)`** - кикнуть участника, @id которого указано. Также можно объявить причину, по которой происходит кик"
        emb = discord.Embed(title=f"Kick:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "ban":
        msg = f"**`#ban @id (причина)`** - забанить участника, @id которого указано. Также можно объявить причину, по которой происходит бан"
        emb = discord.Embed(title=f"Ban:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "mute":
        msg = f"**`#mute @id (причина)`** - замутить участника, @id которого указано. Также можно объявить причину, по которой происходит мут (здесь обязательно стоит создать роль на сервере 'muted', которая отбирает полное право на сообщение у участника)"
        emb = discord.Embed(title=f"Ban:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "code":
        msg = f"**`#code (текст)`** - зашифровать текст, имеется русский и английский язык, а также основные знаки пунктуации"
        emb = discord.Embed(title=f"Code:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "decode":
        msg = f"**`#decode (текст)`** - расшифровать текст, имеется русский и английский язык, а также основные знаки пунктуации"
        emb = discord.Embed(title=f"Decode:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "ruletka":
        msg = f"**`#ruletka`** - игра 'Русская рулетка': если повезет, то пули не окажется в ячейке, а если нет, то ты умрешь и будешь кикнут с сервера!"
        emb = discord.Embed(title=f"Ruletka:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "play" or command.lower() == "sing":
        msg = f"**`#play/sing (url/слово/фраза)`** - сыграть аудио дорожку из видео по url или по названию"
        emb = discord.Embed(title=f"Play/Sing:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "join" or command.lower() == "connect":
        msg = f"**`#join/connect`** - подсоединиться к voice-каналу, в котором находится написавший"
        emb = discord.Embed(title=f"Join/Connect:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "pause":
        msg = f"**`#pause`** - приостановить аудиодорожку"
        emb = discord.Embed(title=f"Pause:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "resume":
        msg = f"**`#resume`** - возобновить аудиодорожку"
        emb = discord.Embed(title=f"Resume:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "leave" or command.lower() == "stop":
        msg = f"**`#leave/stop`** - выйти из voice-канала"
        emb = discord.Embed(title=f"Leave/Stop:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "queue" or command.lower() == "playlist" or command.lower() == "q":
        msg = f"**`#queue/playlist/q`** - показать плейслист из аудиодорожек"
        emb = discord.Embed(title=f"Queue/Playlist/Q:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "skip":
        msg = f"**`#skip`** - включить следующую аудиодорожку"
        emb = discord.Embed(title=f"Skip:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "now_playing":
        msg = f"**`#volume 1-100`** - установить громкость от 1 до 100"
        emb = discord.Embed(title=f"Now_playing:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "volume" or command.lower() == "vol":
        msg = f"**`#volume 1-100`** - установить громкость от 1 до 100"
        emb = discord.Embed(title=f"Volume:\n", description=msg, colour=discord.Color.red())
    elif command.lower() == "roleplay" or command.lower() == "rp":
        msg = f"**`#выебать @id`** - выебать участника сервера через упоминание или **@id!**\n" \
              f"**`#ударить @id`** - ударить участника сервера через упоминание или **@id!**\n" \
              f"**`#трахнуть @id`** - трахнуть участника сервера через упоминание или **@id!**\n" \
              f"**`#обоссать @id`** - обоссать участника сервера через упоминание или **@id!**\n" \
              f"**`#изнасиловать @id`** - изнасиловать участника сервера через упоминание или **@id!**\n" \
              f"**`#убить @id`** - убить участника сервера через упоминание или **@id!**\n"
        emb = discord.Embed(title=f"RolePlay команды:\n", description=msg, colour=discord.Color.red())
    else:
        msg = f"**`#repeat (текст)`** - повторить текст\n" \
              f"**`#loop (текст) (кол-во раз)`** - повторить текст некоторое кол-во раз\n" \
              f"**`#about @id`** - информация о человеке, **@id** которого указано. Если **@id** человека не указано, выведется информация о человеке,написавшем команду\n" \
              f"**`#kick @id (причина)`** - кикнуть участника, **@id** которого указано. Также можно объявить причину, по которой происходит кик\n" \
              f"**`#ban @id (причина)`** - забанить участника, **@id** которого указано. Также можно объявить причину, по которой происходит бан\n" \
              f"**`#mute @id (причина)`** - замутить участника, **@id** которого указано. Также можно объявить причину, по которой происходит мут (здесь обязательно стоит создать роль на сервере 'muted', которая отбирает полное право на сообщение у участника)\n"\
              f"**`#code/#decode (текст)`** - зашифровать/расшифровать текст, имеется русский и английский язык, а также основные знаки пунктуации\n" \
              f"**`#ruletka`** - игра 'Русская рулетка': если повезет, то пули не окажется в ячейке, а если нет, то ты умрешь и будешь кикнут с сервера!\n" \
              f"**`#play/sing (url/слово/фраза)`** - сыграть аудио дорожку из видео по url или по названию\n" \
              f"**`#join/connect`** - подсоединиться к voice-каналу, в котором находится написавший\n"\
              f"**`#pause`** - приостановить аудиодорожку\n"\
              f"**`#resume`** - возобновить аудиодорожку\n"\
              f"**`#leave/stop`** - выйти из voice-канала\n"\
              f"**`#queue/playlist/q`** - показать плейслист из аудиодорожек\n"\
              f"**`#skip`** - включить следующую аудиодорожку\n"\
              f"**`#now_playing`** - показать ту аудидорожку, которая сейчас играет\n"\
              f"**`#volume 1-100`** - установить громкость от 1 до 100\n"\
              f"**`#help rp`** - RolePlay команды\n"
        emb = discord.Embed(title=f"Памятка по командам:\n", description=msg, colour=discord.Color.red())
    await ctx.send(embed=emb)


@bot.command()
async def repeat(ctx, msg=None):
    if msg == None:
        emb = discord.Embed(description=f'Мне **нечего** повторять :thinking:', colour=discord.Color.red())
        await ctx.send(embed=emb)
    else:
        await ctx.send(msg)


@bot.command()
async def ruletka(ctx):
    shoot = randint(1, 6)
    bully = randint(1, 6)
    if ctx.message.author.id == 473844505301221396:
        await ctx.send("Ты Sofar, тебе нельзя пользоваться этой командой!")
    else:
            if shoot == bully:
                for m in ctx.guild.members:
                    if m.id == bot.user.id:
                        bot_role = m.top_role
                if m.top_role >= bot_role:
                    emb = discord.Embed(description=f'**Недостатончо прав**, чтобы кикнуть тебя, но считай, что ты проиграл! :thinking:', colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    await ctx.author.kick(reason="Получил(a) пулю в бошку!")
                    emb = discord.Embed(title=f"Кик ⚠", description=f'Вы были кикнуты с сервера `{ctx.message.guild.name}`, по причине **проигрыша в русской рулетке**! :weary:', colour=discord.Color.red())
                    await ctx.author.send(embed=emb)
                    msg = f"{ctx.author.mention} умер и был кикнут, земля ему пухом! :worried:"
                    emb = discord.Embed(title=f"Не повезло! :x:\n", description=msg, colour=discord.Color.red())
                    await ctx.send(embed=emb)
            else:
                msg = f"Но лучше положи револьвер на место, а то мало ли! :wink:"
                emb = discord.Embed(title=f"Везунчик! :white_check_mark:\n", description=msg, colour=discord.Color.red())
                await ctx.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member = None, *, reason=None):
    if member == None:
        if ctx.message.mentions == []:
            emb = discord.Embed(description=f'Участник не найден! :person_shrugging:', colour=discord.Color.red())
            await ctx.send(embed=emb)
        else:
            member = ctx.message.mentions[0]
            for m in ctx.guild.members:
                if m.id == bot.user.id:
                    bot_role = m.top_role
            if ctx.author == member:
                emb = discord.Embed(description=f'**Ты** не можешь кикнуть сам себя! :person_shrugging:',
                                    colour=discord.Color.red())
                await ctx.send(embed=emb)
            elif member.id == 825328674583871539:
                emb = discord.Embed(
                    description=f'Король умер, да здравствует король? Не, так просто меня не свергнешь! :wink:',
                    colour=discord.Color.red())
                await ctx.send(embed=emb)
            elif member.bot:
                emb = discord.Embed(
                    description=f'Я не могу кикать ботов, а особенно **`{member.name}`**, они мои собратья! :disappointed_relieved:',
                    colour=discord.Color.red())
                await ctx.send(embed=emb)
            elif m.top_role >= bot_role or member.guild_permissions == 2147483647:
                emb = discord.Embed(
                    description=f'**Недостатончо прав**, чтобы выполнить это действие! :person_shrugging:',
                    colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if reason == None:
                    emb = discord.Embed(title=f"Кик ⚠", description=f'{member.mention} был кикнут с сервера! :weary: ',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                    emb1 = discord.Embed(title=f"Кик ⚠",
                                         description=f'Вы были кикнуты с сервера `{ctx.message.guild.name}`! :weary:',
                                         colour=discord.Color.red())
                    await member.send(embed=emb1)
                    await member.kick(reason=reason)
                else:
                    emb = discord.Embed(title=f"Кик ⚠",
                                        description=f'{member.mention} был кикнут с сервера, по причине: **{reason}**! :thinking:',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                    emb1 = discord.Embed(title=f"Кик ⚠",
                                         description=f'Вы были кикнуты с сервера `{ctx.message.guild.name}`, по причине: **{reason}**! :thinking:',
                                         colour=discord.Color.red())
                    await member.send(embed=emb1)
                    await member.kick(reason=reason)
    else:
        member = member
        for m in ctx.guild.members:
            if m.id == bot.user.id:
                bot_role = m.top_role
        if ctx.author == member:
            emb = discord.Embed(description=f'**Ты** не можешь кикнуть сам себя! :person_shrugging:', colour=discord.Color.red())
            await ctx.send(embed=emb)
        elif member.id == 825328674583871539:
            emb = discord.Embed(description=f'Король умер, да здравствует король? Не, так просто меня не свергнешь! :wink:', colour=discord.Color.red())
            await ctx.send(embed=emb)
        elif member.bot:
            emb = discord.Embed(description=f'Я не могу кикать ботов, а особенно **`{member.name}`**, они мои собратья! :disappointed_relieved:', colour=discord.Color.red())
            await ctx.send(embed=emb)
        elif m.top_role >= bot_role or member.guild_permissions == 2147483647:
            emb = discord.Embed(description=f'**Недостатончо прав**, чтобы выполнить это действие! :person_shrugging:', colour=discord.Color.red())
            await ctx.send(embed=emb)
        else:
            if reason == None:
                    emb = discord.Embed(title=f"Кик ⚠", description=f'{member.mention} был кикнут с сервера! :weary: ', colour=discord.Color.red())
                    await ctx.send(embed=emb)
                    emb1 = discord.Embed(title=f"Кик ⚠", description=f'Вы были кикнуты с сервера `{ctx.message.guild.name}`! :weary:', colour=discord.Color.red())
                    await member.send(embed=emb1)
                    await member.kick(reason=reason)
            else:
                emb = discord.Embed(title=f"Кик ⚠", description=f'{member.mention} был кикнут с сервера, по причине: **{reason}**! :thinking:', colour=discord.Color.red())
                await ctx.send(embed=emb)
                emb1 = discord.Embed(title=f"Кик ⚠", description=f'Вы были кикнуты с сервера `{ctx.message.guild.name}`, по причине: **{reason}**! :thinking:', colour=discord.Color.red())
                await member.send(embed=emb1)
                await member.kick(reason=reason)


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if member == None:
        if ctx.message.mentions == []:
            emb = discord.Embed(description=f'Участник не найден! :person_shrugging:', colour=discord.Color.red())
            await ctx.send(embed=emb)
        else:
            member = ctx.message.mentions[0]
            for m in ctx.guild.members:
                if m.id == bot.user.id:
                    bot_role = m.top_role
            if ctx.author == member:
                emb = discord.Embed(description=f'**Ты** не можешь забанить сам себя! :person_shrugging:',
                                    colour=discord.Color.red())
                await ctx.send(embed=emb)
            elif member.id == 825328674583871539:
                emb = discord.Embed(
                    description=f'Король умер, да здравствует король? Не, так просто меня не свергнешь! :wink:',
                    colour=discord.Color.red())
                await ctx.send(embed=emb)
            elif member.bot:
                emb = discord.Embed(
                    description=f'Я не могу банить ботов, а особенно **`{member.name}`**, они мои собратья! :disappointed_relieved:',
                    colour=discord.Color.red())
                await ctx.send(embed=emb)
            elif m.top_role >= bot_role or member.guild_permissions == 2147483647 or member.bot:
                emb = discord.Embed(
                    description=f'**Недостатончо прав**, чтобы выполнить это действие! :person_shrugging:',
                    colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if reason == None:
                    emb = discord.Embed(title=f"Бан ⚠", description=f'{member.mention} был забанен с сервера! :weary: ',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                    emb1 = discord.Embed(title=f"Бан ⚠",
                                         description=f'Вы были забанены на сервера `{ctx.message.guild.name}`! :weary:',
                                         colour=discord.Color.red())
                    await member.send(embed=emb1)
                    await member.ban(reason=reason)
                else:
                    emb = discord.Embed(title=f"Бан ⚠",
                                        description=f'{member.mention} был забанен с сервера, по причине: **{reason}**! :thinking:',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                    emb1 = discord.Embed(title=f"Бан ⚠",
                                         description=f'Вы были забанены на сервера `{ctx.message.guild.name}`, по причине: **{reason}**! :thinking:',
                                         colour=discord.Color.red())
                    await member.send(embed=emb1)
                    await member.ban(reason=reason)
    else:
        member = member
        for m in ctx.guild.members:
            if m.id == bot.user.id:
                bot_role = m.top_role
        if ctx.author == member:
            emb = discord.Embed(description=f'**Ты** не можешь забанить сам себя! :person_shrugging:',
                                colour=discord.Color.red())
            await ctx.send(embed=emb)
        elif member.id == 825328674583871539:
            emb = discord.Embed(
                description=f'Король умер, да здравствует король? Не, так просто меня не свергнешь! :wink:',
                colour=discord.Color.red())
            await ctx.send(embed=emb)
        elif member.bot:
            emb = discord.Embed(
                description=f'Я не могу банить ботов, а особенно **`{member.name}`**, они мои собратья! :disappointed_relieved:',
                colour=discord.Color.red())
            await ctx.send(embed=emb)
        elif m.top_role >= bot_role or member.guild_permissions == 2147483647 or member.bot:
            emb = discord.Embed(description=f'**Недостатончо прав**, чтобы выполнить это действие! :person_shrugging:',
                                colour=discord.Color.red())
            await ctx.send(embed=emb)
        else:
            if reason == None:
                emb = discord.Embed(title=f"Бан ⚠", description=f'{member.mention} был забанен с сервера! :weary: ',
                                    colour=discord.Color.red())
                await ctx.send(embed=emb)
                emb1 = discord.Embed(title=f"Бан ⚠",
                                     description=f'Вы были забанены на сервера `{ctx.message.guild.name}`! :weary:',
                                     colour=discord.Color.red())
                await member.send(embed=emb1)
                await member.ban(reason=reason)
            else:
                emb = discord.Embed(title=f"Бан ⚠",
                                    description=f'{member.mention} был забанен с сервера, по причине: **{reason}**! :thinking:',
                                    colour=discord.Color.red())
                await ctx.send(embed=emb)
                emb1 = discord.Embed(title=f"Бан ⚠",
                                     description=f'Вы были забанены на сервера `{ctx.message.guild.name}`, по причине: **{reason}**! :thinking:',
                                     colour=discord.Color.red())
                await member.send(embed=emb1)
                await member.ban(reason=reason)


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None, *, reason=None):
    if member == None:
        if ctx.message.mentions == []:
            emb = discord.Embed(description=f'Участник не найден! :person_shrugging:', colour=discord.Color.red())
            await ctx.send(embed=emb)
        else:
            member = ctx.message.mentions[0]
            mute_role1 = discord.utils.get(ctx.message.guild.roles, name='muted')
            mute_role2 = discord.utils.get(ctx.message.guild.roles, name='Muted')
            mute_role3 = discord.utils.get(ctx.message.guild.roles, name='Mute')
            mute_role4 = discord.utils.get(ctx.message.guild.roles, name='mute')
            mute_role5 = discord.utils.get(ctx.message.guild.roles, name='мут')
            if mute_role1 != None:
                if mute_role1 in member.roles:
                    emb = discord.Embed(description=f"Данная **роль** уже присутсвует у **`{member.display_name}`**!",
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    if reason == None:
                        await member.add_roles(mute_role1)
                        emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
                    else:
                        await member.add_roles(mute_role1)
                        emb = discord.Embed(title="Мут ⚠",
                                            description=f'{member.mention} был замучен на сервере, по причине: {reason}!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
            if mute_role2 != None:
                if mute_role2 in member.roles:
                    emb = discord.Embed(description=f"Данная **роль** уже присутсвует у **`{member.display_name}`**!",
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    if reason == None:
                        await member.add_roles(mute_role1)
                        emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
                    else:
                        await member.add_roles(mute_role1)
                        emb = discord.Embed(title="Мут ⚠",
                                            description=f'{member.mention} был замучен на сервере, по причине: {reason}!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
            if mute_role3 != None:
                if mute_role3 in member.roles:
                    emb = discord.Embed(description=f"Данная **роль** уже присутсвует у **`{member.display_name}`**!",
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    if reason == None:
                        await member.add_roles(mute_role1)
                        emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
                    else:
                        await member.add_roles(mute_role1)
                        emb = discord.Embed(title="Мут ⚠",
                                            description=f'{member.mention} был замучен на сервере, по причине: {reason}!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
            if mute_role4 != None:
                if mute_role4 in member.roles:
                    emb = discord.Embed(description=f"Данная **роль** уже присутсвует у **`{member.display_name}`**!",
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    if reason == None:
                        await member.add_roles(mute_role1)
                        emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
                    else:
                        await member.add_roles(mute_role1)
                        emb = discord.Embed(title="Мут ⚠",
                                            description=f'{member.mention} был замучен на сервере, по причине: {reason}!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
            if mute_role5 != None:
                if mute_role5 in member.roles:
                    emb = discord.Embed(description=f"Данная **роль** уже присутсвует у **`{member.display_name}`**!",
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    if reason == None:
                        await member.add_roles(mute_role1)
                        emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
                    else:
                        await member.add_roles(mute_role1)
                        emb = discord.Embed(title="Мут ⚠",
                                            description=f'{member.mention} был замучен на сервере, по причине: {reason}!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
    else:
        member = member
        mute_role1 = discord.utils.get(ctx.message.guild.roles, name='muted')
        mute_role2 = discord.utils.get(ctx.message.guild.roles, name='Muted')
        mute_role3 = discord.utils.get(ctx.message.guild.roles, name='Mute')
        mute_role4 = discord.utils.get(ctx.message.guild.roles, name='mute')
        mute_role5 = discord.utils.get(ctx.message.guild.roles, name='мут')
        if mute_role1 != None:
            if mute_role1 in member.roles:
                emb = discord.Embed(description=f"Данная **роль** уже присутсвует у **`{member.display_name}`**!", colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if reason == None:
                    await member.add_roles(mute_role1)
                    emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере!', colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    await member.add_roles(mute_role1)
                    emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере, по причине: {reason}!', colour=discord.Color.red())
                    await ctx.send(embed=emb)
        if mute_role2 != None:
            if mute_role2 in member.roles:
                emb = discord.Embed(description=f"Данная **роль** уже присутсвует у **`{member.display_name}`**!", colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if reason == None:
                    await member.add_roles(mute_role1)
                    emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере!', colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    await member.add_roles(mute_role1)
                    emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере, по причине: {reason}!',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
        if mute_role3 != None:
            if mute_role3 in member.roles:
                emb = discord.Embed(description=f"Данная **роль** уже присутсвует у **`{member.display_name}`**!", colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if reason == None:
                    await member.add_roles(mute_role1)
                    emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере!', colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    await member.add_roles(mute_role1)
                    emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере, по причине: {reason}!',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
        if mute_role4 != None:
            if mute_role4 in member.roles:
                emb = discord.Embed(description=f"Данная **роль** уже присутсвует у **`{member.display_name}`**!", colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if reason == None:
                    await member.add_roles(mute_role1)
                    emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере!', colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    await member.add_roles(mute_role1)
                    emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере, по причине: {reason}!',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
        if mute_role5 != None:
            if mute_role5 in member.roles:
                emb = discord.Embed(description=f"Данная **роль** уже присутсвует у **`{member.display_name}`**!", colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if reason == None:
                    await member.add_roles(mute_role1)
                    emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере!', colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    await member.add_roles(mute_role1)
                    emb = discord.Embed(title="Мут ⚠", description=f'{member.mention} был замучен на сервере, по причине: {reason}!',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None, *, reason=None):
    if member == None:
        if ctx.message.mentions == []:
            emb = discord.Embed(description=f'Участник не найден! :person_shrugging:', colour=discord.Color.red())
            await ctx.send(embed=emb)
        else:
            member = ctx.message.mentions[0]
            mute_role1 = discord.utils.get(ctx.message.guild.roles, name='muted')
            mute_role2 = discord.utils.get(ctx.message.guild.roles, name='Muted')
            mute_role3 = discord.utils.get(ctx.message.guild.roles, name='Mute')
            mute_role4 = discord.utils.get(ctx.message.guild.roles, name='mute')
            mute_role5 = discord.utils.get(ctx.message.guild.roles, name='мут')
            if mute_role1 != None:
                if mute_role1 not in member.roles:
                    emb = discord.Embed(description=f"У **`{member.display_name}'a`** нет роли **мута**!",
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    if reason == None:
                        await member.remove_roles(mute_role1)
                        emb = discord.Embed(title="Размут ⚠", description=f'{member.mention} был размучен на сервере!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
                    else:
                        await member.remove_roless(mute_role1)
                        emb = discord.Embed(title="Размут ⚠",
                                            description=f'{member.mention} был размучен на сервере, по причине: {reason}!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
            if mute_role2 != None:
                if mute_role2 not in member.roles:
                    emb = discord.Embed(description=f"У **`{member.display_name}'a`** нет роли **мута**!",
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    if reason == None:
                        await member.remove_roles(mute_role1)
                        emb = discord.Embed(title="Размут ⚠", description=f'{member.mention} был размучен на сервере!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
                    else:
                        await member.remove_roless(mute_role1)
                        emb = discord.Embed(title="Размут ⚠",
                                            description=f'{member.mention} был размучен на сервере, по причине: {reason}!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
            if mute_role3 != None:
                if mute_role3 not in member.roles:
                    emb = discord.Embed(description=f"У **`{member.display_name}'a`** нет роли **мута**!",
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    if reason == None:
                        await member.remove_roles(mute_role1)
                        emb = discord.Embed(title="Размут ⚠", description=f'{member.mention} был размучен на сервере!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
                    else:
                        await member.remove_roless(mute_role1)
                        emb = discord.Embed(title="Размут ⚠",
                                            description=f'{member.mention} был размучен на сервере, по причине: {reason}!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
            if mute_role4 != None:
                if mute_role4 not in member.roles:
                    emb = discord.Embed(description=f"У **`{member.display_name}'a`** нет роли **мута**!",
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    if reason == None:
                        await member.remove_roles(mute_role1)
                        emb = discord.Embed(title="Размут ⚠", description=f'{member.mention} был размучен на сервере!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
                    else:
                        await member.remove_roless(mute_role1)
                        emb = discord.Embed(title="Размут ⚠",
                                            description=f'{member.mention} был размучен на сервере, по причине: {reason}!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
            if mute_role5 != None:
                if mute_role5 not in member.roles:
                    emb = discord.Embed(description=f"У **`{member.display_name}'a`** нет роли **мута**!",
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    if reason == None:
                        await member.remove_roles(mute_role1)
                        emb = discord.Embed(title="Размут ⚠", description=f'{member.mention} был размучен на сервере!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
                    else:
                        await member.remove_roless(mute_role1)
                        emb = discord.Embed(title="Размут ⚠",
                                            description=f'{member.mention} был размучен на сервере, по причине: {reason}!',
                                            colour=discord.Color.red())
                        await ctx.send(embed=emb)
    else:
        member = member
        mute_role1 = discord.utils.get(ctx.message.guild.roles, name='muted')
        mute_role2 = discord.utils.get(ctx.message.guild.roles, name='Muted')
        mute_role3 = discord.utils.get(ctx.message.guild.roles, name='Mute')
        mute_role4 = discord.utils.get(ctx.message.guild.roles, name='mute')
        mute_role5 = discord.utils.get(ctx.message.guild.roles, name='мут')
        if mute_role1 != None:
            if mute_role1 not in member.roles:
                emb = discord.Embed(description=f"У **`{member.display_name}'a`** нет роли **мута**!", colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if reason == None:
                    await member.remove_roles(mute_role1)
                    emb = discord.Embed(title="Размут ⚠", description=f'{member.mention} был размучен на сервере!', colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    await member.remove_roless(mute_role1)
                    emb = discord.Embed(title="Размут ⚠", description=f'{member.mention} был размучен на сервере, по причине: {reason}!', colour=discord.Color.red())
                    await ctx.send(embed=emb)
        if mute_role2 != None:
            if mute_role2 not in member.roles:
                emb = discord.Embed(description=f"У **`{member.display_name}'a`** нет роли **мута**!", colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if reason == None:
                    await member.remove_roles(mute_role1)
                    emb = discord.Embed(title="Размут ⚠", description=f'{member.mention} был размучен на сервере!',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    await member.remove_roless(mute_role1)
                    emb = discord.Embed(title="Размут ⚠",
                                        description=f'{member.mention} был размучен на сервере, по причине: {reason}!',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
        if mute_role3 != None:
            if mute_role3 not in member.roles:
                emb = discord.Embed(description=f"У **`{member.display_name}'a`** нет роли **мута**!", colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if reason == None:
                    await member.remove_roles(mute_role1)
                    emb = discord.Embed(title="Размут ⚠", description=f'{member.mention} был размучен на сервере!',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    await member.remove_roless(mute_role1)
                    emb = discord.Embed(title="Размут ⚠",
                                        description=f'{member.mention} был размучен на сервере, по причине: {reason}!',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
        if mute_role4 != None:
            if mute_role4 not in member.roles:
                emb = discord.Embed(description=f"У **`{member.display_name}'a`** нет роли **мута**!", colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if reason == None:
                    await member.remove_roles(mute_role1)
                    emb = discord.Embed(title="Размут ⚠", description=f'{member.mention} был размучен на сервере!',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    await member.remove_roless(mute_role1)
                    emb = discord.Embed(title="Размут ⚠",
                                        description=f'{member.mention} был размучен на сервере, по причине: {reason}!',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
        if mute_role5 != None:
            if mute_role5 not in member.roles:
                emb = discord.Embed(description=f"У **`{member.display_name}'a`** нет роли **мута**!", colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if reason == None:
                    await member.remove_roles(mute_role1)
                    emb = discord.Embed(title="Размут ⚠", description=f'{member.mention} был размучен на сервере!',
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    await member.remove_roless(mute_role1)
                    emb = discord.Embed(title="Размут ⚠", description=f'{member.mention} был размучен на сервере, по причине: {reason}!', colour=discord.Color.red())
                    await ctx.send(embed=emb)


@bot.command()
async def about(ctx, member: discord.Member = None, guild: discord.Guild = None):
    if member == None:
            if ctx.message.author.activity == None:
                status = "Нету"
            else:
                status = ctx.message.author.activity
            emb = discord.Embed(title="Информация о пользователе", color=ctx.message.author.color)
            emb.add_field(name="Отображаемое имя:", value=ctx.message.author.display_name, inline=False)
            emb.add_field(name="Имя аккаунта:", value=ctx.message.author, inline=False)
            emb.add_field(name="id пользователя:", value=ctx.message.author.id, inline=False)
            t = ctx.message.author.status
            if t == discord.Status.online:
                d = " В сети"

            t = ctx.message.author.status
            if t == discord.Status.offline:
                d = "⚪ Не в сети"

            t = ctx.message.author.status
            if t == discord.Status.idle:
                d = " Не активен"

            t = ctx.message.author.status
            if t == discord.Status.dnd:
                d = " Не беспокоить"

            emb.add_field(name="Активность:", value=d, inline=False)
            emb.add_field(name="Статус:", value=status, inline=False)
            emb.add_field(name="Роль на сервере:", value=f"{ctx.message.author.top_role.mention}",inline=False)
            emb.add_field(name="Акаунт был создан:", value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
            emb.set_thumbnail(url=ctx.message.author.avatar_url)
            if str(ctx.message.author.id) in users:
                emb.add_field(name="XP:", value=f"{users[str(ctx.message.author.id)]['exp']}/1000", inline=False)
                emb.add_field(name="LVL:", value=f"{users[str(ctx.message.author.id)]['lvl']} уровень", inline=False)
                emb.add_field(name="Выигрыши в дуэлях:", value=f"{users[str(ctx.message.author.id)]['duwins']}",inline=False)
                emb.add_field(name="Предупреждения:", value=f"{users[str(ctx.message.author.id)]['pred']}/3",inline=False)
            else:
                emb.add_field(name="XP:", value=f"0/1000", inline=False)
                emb.add_field(name="LVL:", value=f"1 уровень", inline=False)
                emb.add_field(name="Выигрыши в дуэлях:", value=f"0", inline=False)
                emb.add_field(name="Предупреждения:", value=f"0/3", inline=False)
            await ctx.send(embed=emb)
    else:
        if member.bot == True:
            await ctx.send("Я не могу иметь в себе информацию бота :/")
        else:
            if member.activity == None:
                status = "Нету"
            else:
                status = member.activity
            emb = discord.Embed(title="Информация о пользователе", color=member.color)
            emb.add_field(name="Отображаемое имя:", value=member.display_name, inline=False)
            emb.add_field(name="Имя аккаунта:", value=member, inline=False)
            emb.add_field(name="id пользователя:", value=member.id, inline=False)
            t = member.status
            if t == discord.Status.online:
                d = " В сети"

            t = member.status
            if t == discord.Status.offline:
                d = "⚪ Не в сети"

            t = member.status
            if t == discord.Status.idle:
                d = " Не активен"

            t = member.status
            if t == discord.Status.dnd:
                d = " Не беспокоить"
            emb.add_field(name="Активность:", value=d, inline=False)
            emb.add_field(name="Статус:", value=status, inline=False)
            emb.add_field(name="Роль на сервере:", value=f"{member.top_role.mention}",inline=False)
            emb.add_field(name="Акаунт был создан:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p"),inline=False)
            emb.set_thumbnail(url=member.avatar_url)
            if str(member.id) in users:
                emb.add_field(name="XP:", value=f"{users[str(member.id)]['exp']}/1000", inline=False)
                emb.add_field(name="LVL:", value=f"{users[str(member.id)]['lvl']} уровень", inline=False)
                emb.add_field(name="Выигрыши в дуэлях:", value=f"{users[str(member.id)]['duwins']}", inline=False)
                emb.add_field(name="Предупреждения:", value=f"{users[str(member.id)]['pred']}/3", inline=False)
            else:
                emb.add_field(name="XP:", value=f"0/1000", inline=False)
                emb.add_field(name="LVL:", value=f"1 уровень", inline=False)
                emb.add_field(name="Выигрыши в дуэлях:", value=f"0", inline=False)
                emb.add_field(name="Предупреждения:", value=f"0/3", inline=False)
            await ctx.send(embed=emb)


@bot.command()
async def loop(ctx):
    msg = ""
    a = ctx.message.content.split()[-1]
    if a.isdigit() == True:
        print(int(ctx.message.content.split()[-1]))
        if int(ctx.message.content.split()[-1]) <= 20:
            for i in range(int(ctx.message.content.split()[-1])):
                msg += f"{ctx.message.content[6:-2]}\n"
        elif int(ctx.message.content.split()[-1]) >= 20:
            msg = "Ограничение - 20 раз, не надо засорять сервер бедным админам :wink:"
        elif int(ctx.message.content.split()[-1]) != 0:
            for i in range(int(ctx.message.content.split()[-1])):
                msg += f"{ctx.message.content[6:-2]}\n"
        if len(msg) >= 2000:
            await ctx.send("Э, дискорд запрещает больше 2000 символов в одном сообщении! :person_gesturing_no: ")
        else:
            await ctx.send(msg)
    else:
        await ctx.send(f"{ctx.message.content[6:]}\n")


@bot.command()
async def hello(ctx):
    emb = discord.Embed(description=f"Привет, **`{ctx.author.display_name}`**", colour=discord.Color.red())
    await ctx.send(embed=emb)


@bot.command()
async def oky(ctx):
    emb = discord.Embed(description=f"**Я** тут!", colour=discord.Color.red())
    await ctx.send(embed=emb)


@bot.command()
async def code(ctx):
    m = ""
    for char in ctx.message.content[6:].lower():
        if char == "a":
            m += "881"
        if char == "b":
            m += "312"
        if char == "c":
            m += "841"
        if char == "d":
            m += "541"
        if char == "e":
            m += "632"
        if char == "f":
            m += "463"
        if char == "g":
            m += "346"
        if char == "h":
            m += "436"
        if char == "j":
            m += "768"
        if char == "i":
            m += "111"
        if char == "k":
            m += "123"
        if char == "l":
            m += "985"
        if char == "m":
            m += "234"
        if char == "n":
            m += "652"
        if char == "o":
            m += "335"
        if char == "p":
            m += "665"
        if char == "q":
            m += "222"
        if char == "r":
            m += "435"
        if char == "s":
            m += "153"
        if char == "t":
            m += "980"
        if char == "u":
            m += "901"
        if char == "v":
            m += "990"
        if char == "w":
            m += "001"
        if char == "x":
            m += "219"
        if char == "y":
            m += "128"
        if char == "z":
            m += "098"
        if char == " ":
            m += "090"
        if char == ",":
            m += "494"
        if char == ".":
            m += "199"
        if char == ":":
            m += "393"
        if char == "/":
            m += "666"
        if char == "'":
            m += "228"
        if char == '"':
            m += "672"
        if char == '|':
            m += "563"
        if char == '(':
            m += "565"
        if char == ')':
            m += "571"
        if char == '-':
            m += "972"
        if char == '=':
            m += "867"
        if char == "а":
            m += "010"
        if char == "б":
            m += "020"
        if char == "в":
            m += "088"
        if char == "г":
            m += "019"
        if char == "д":
            m += "880"
        if char == "е":
            m += "771"
        if char == "ё":
            m += "810"
        if char == "ж":
            m += "911"
        if char == "з":
            m += "212"
        if char == "и":
            m += "653"
        if char == "й":
            m += "325"
        if char == "к":
            m += "050"
        if char == "л":
            m += "070"
        if char == "м":
            m += "007"
        if char == "н":
            m += "112"
        if char == "о":
            m += "856"
        if char == "п":
            m += "223"
        if char == "р":
            m += "900"
        if char == "с":
            m += "800"
        if char == "т":
            m += "100"
        if char == "у":
            m += "700"
        if char == "ф":
            m += "500"
        if char == "х":
            m += "200"
        if char == "ц":
            m += "300"
        if char == "ч":
            m += "400"
        if char == "ш":
            m += "009"
        if char == "щ":
            m += "004"
        if char == "ъ":
            m += "812"
        if char == "ы":
            m += "341"
        if char == "ь":
            m += "987"
        if char == "э":
            m += "413"
        if char == "ю":
            m += "236"
        if char == "я":
            m += "109"
        if char == "1":
            m += "101"
        if char == "2":
            m += "191"
        if char == "3":
            m += "141"
        if char == "4":
            m += "149"
        if char == "5":
            m += "361"
        if char == "6":
            m += "499"
        if char == "7":
            m += "477"
        if char == "8":
            m += "877"
        if char == "9":
            m += "970"
        if char == "0":
            m += "120"
    if m == "":
        emb = discord.Embed(description="А где то, что **надо зашифровать**? :thinking:", color=discord.Color.red())
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(title="Зашифрованное сообщение:", description=m, color=discord.Color.red())
        await ctx.send(embed=emb)


@bot.command()
async def decode(ctx):
    m = ""
    s = ([ctx.message.content[8:][i:i + 3] for i in range(0, len(ctx.message.content), 3)])
    for i in s:
        if i == "881":
            m += "a"
        if i == "312":
            m += "b"
        if i == "841":
            m += "c"
        if i == "541":
            m += "d"
        if i == "632":
            m += "e"
        if i == "463":
            m += "f"
        if i == "346":
            m += "g"
        if i == "436":
            m += "h"
        if i == "768":
            m += "j"
        if i == "111":
            m += "i"
        if i == "123":
            m += "k"
        if i == "985":
            m += "l"
        if i == "234":
            m += "m"
        if i == "652":
            m += "n"
        if i == "335":
            m += "o"
        if i == "665":
            m += "p"
        if i == "222":
            m += "q"
        if i == "435":
            m += "r"
        if i == "153":
            m += "s"
        if i == "980":
            m += "t"
        if i == "901":
            m += "u"
        if i == "990":
            m += "v"
        if i == "001":
            m += "w"
        if i == "219":
            m += "x"
        if i == "128":
            m += "y"
        if i == "098":
            m += "z"
        if i == "090":
            m += " "
        if i == "494":
            m += ","
        if i == "199":
            m += "."
        if i == "393":
            m += ":"
        if i == "666":
            m += "/"
        if i == "228":
            m += "'"
        if i == '672':
            m += '"'
        if i == '563':
            m += "|"
        if i == '565':
            m += "("
        if i == '571':
            m += ")"
        if i == '972':
            m += "-"
        if i == '867':
            m += "="
        if i == "010":
            m += "а"
        if i == "020":
            m += "б"
        if i == "088":
            m += "в"
        if i == "019":
            m += "г"
        if i == "880":
            m += "д"
        if i == "771":
            m += "е"
        if i == "810":
            m += "ё"
        if i == "911":
            m += "ж"
        if i == "212":
            m += "з"
        if i == "653":
            m += "и"
        if i == "325":
            m += "й"
        if i == "050":
            m += "к"
        if i == "070":
            m += "л"
        if i == "007":
            m += "м"
        if i == "112":
            m += "н"
        if i == "856":
            m += "о"
        if i == "223":
            m += "п"
        if i == "900":
            m += "р"
        if i == "800":
            m += "с"
        if i == "100":
            m += "т"
        if i == "700":
            m += "у"
        if i == "500":
            m += "ф"
        if i == "200":
            m += "х"
        if i == "300":
            m += "ц"
        if i == "400":
            m += "ч"
        if i == "009":
            m += "ш"
        if i == "004":
            m += "щ"
        if i == "812":
            m += "ъ"
        if i == "341":
            m += "ы"
        if i == "987":
            m += "ь"
        if i == "413":
            m += "э"
        if i == "236":
            m += "ю"
        if i == "109":
            m += "я"
        if i == "101":
            m += "1"
        if i == "191":
            m += "2"
        if i == "141":
            m += "3"
        if i == "149":
            m += "4"
        if i == "361":
            m += "5"
        if i == "499":
            m += "6"
        if i == "477":
            m += "7"
        if i == "877":
            m += "8"
        if i == "970":
            m += "9"
        if i == "120":
            m += "0"
    if m == "":
        emb = discord.Embed(description="А где то, что **надо расшифровать**? :thinking:", color=discord.Color.red())
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(title="Расшифрованное сообщение:", description=m, color=discord.Color.red())
        await ctx.send(embed=emb)


@bot.command()
async def load(ctx, extension):
    # Check if the user running the command is actually the owner of the bot 
    if ctx.author.id == OWNERID:
        bot.load_extension(f'Cogs.{extension}')
        await ctx.send(f"Enabled the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")


@bot.command()
async def unload(ctx, extension):
    # Check if the user running the command is actually the owner of the bot 
    if ctx.author.id == OWNERID:
        bot.unload_extension(f'Cogs.{extension}')
        await ctx.send(f"Disabled the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")


@bot.command(name="reload")
async def reload_(ctx, extension):
    # Check if the user running the command is actually the owner of the bot 
    if ctx.author.id == OWNERID:
        bot.reload_extension(f'Cogs.{extension}')
        await ctx.send(f"Reloaded the Cog!") 
    else:
        await ctx.send(f"You are not cool enough to use this command")


@bot.command()
async def get(ctx, func=None):
    if func == "members":
        n = 1
        msgg = ""
        for i in ctx.guild.members:
            msgg += f"**`{n}`**: **{i}**  -  *{i.id}*\n"
            n += 1
        emb = discord.Embed(title=f"Участники этого сервера:\n", description=msgg, colour=discord.Color.red())
        await ctx.send(embed=emb)
    elif func == "channels":
        n = 1
        msgg = ""
        for i in ctx.guild.channels:
            msgg += f"**`{n}`**: **{i}**  -  *{i.id}*\n"
            n += 1
        emb = discord.Embed(title=f"Каналы этого сервера:\n", description=msgg, colour=discord.Color.red())
        await ctx.send(embed=emb)
    elif func == None:
        await ctx.send("Ты забыл указать что хочешь получить! :man_shrugging: ")


@bot.command()
async def time(ctx):
    if now.hour <= 9:
        hour = f"0{now.hour}"
    else:
        hour = now.hour
    if now.minute <= 9:
        minute = f"0{now.minute}"
    else:
        minute = now.minute
    if now.day <= 9:
        day = f"0{now.day}"
    else:
        day = now.day
    if now.month <= 9:
        month = f"0{now.month}"
    else:
        month = now.month
    msg = f"Время: `{hour}:{minute}`\n"\
          f"Дата: `{day}.{month}.{now.year}`"
    emb = discord.Embed(title=f"Время и дата:\n", description=msg, colour=discord.Color.red())
    await ctx.send(embed=emb)


@bot.command()
async def ударить(ctx, member: discord.Member = None):
    if member == None:
        emb = discord.Embed(description=f"{ctx.message.author.mention} жёстко вдарил по {ctx.message.mentions[0].mention}! :punch: :head_bandage: ", colour=discord.Color.red())
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f"{ctx.message.author.mention} жёстко вдарил по {member.mention}! :punch: :head_bandage: ", colour=discord.Color.red())
        await ctx.send(embed=emb)


@bot.command()
async def трахнуть(ctx, member: discord.Member = None):
    if member == None:
        emb = discord.Embed(description=f"{ctx.message.author.mention} дико трахнул {ctx.message.mentions[0].mention} :hot_face: :underage: ", colour=discord.Color.red())
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f"{ctx.message.author.mention} дико трахнул {member.mention} :hot_face: :underage: ", colour=discord.Color.red())
        await ctx.send(embed=emb)


@bot.command()
async def обоссать(ctx, member: discord.Member = None):
    if member == None:
        emb = discord.Embed(description=f"{ctx.message.author.mention} обоссал {ctx.message.mentions[0].mention} :banana: :tropical_drink: ", colour=discord.Color.red())
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f"{ctx.message.author.mention} обоссал {member.mention} :banana: :tropical_drink:  ", colour=discord.Color.red())
        await ctx.send(embed=emb)


@bot.command()
async def изнасиловать(ctx, member: discord.Member = None):
    if member == None:
        emb = discord.Embed(description=f"{ctx.message.author.mention} изнасиловал бедного {ctx.message.mentions[0].mention} :woozy_face: :dizzy_face:  ", colour=discord.Color.red())
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f"{ctx.message.author.mention} изнасиловал бедного {member.mention} :woozy_face: :dizzy_face:  ", colour=discord.Color.red())
        await ctx.send(embed=emb)


@bot.command()
async def выебать(ctx, member: discord.Member = None):
    if member == None:
        emb = discord.Embed(description=f"{ctx.message.author.mention} выебал {ctx.message.mentions[0].mention} :woozy_face: :dizzy_face:  ", colour=discord.Color.red())
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f"{ctx.message.author.mention} выебал {member.mention} :woozy_face: :dizzy_face:  ", colour=discord.Color.red())
        await ctx.send(embed=emb)


@bot.command()
async def bump(ctx):
    lst = ["**Ай** блять!", "**Бро** так не троллят!", "**Блять**, больно нахуй!", "**Сука**, теперь на один зуб меньше!"]
    emb = discord.Embed(
        description=lst[randint(0, 3)],
        colour=discord.Color.red())
    await ctx.send(embed=emb)


@bot.command()
async def убить(ctx, member: discord.Member = None):
    list = ["убил", "зарезал", "вырвал глаза у"]
    if member == None:
        emb = discord.Embed(description=f"{ctx.message.author.mention} {list[randint(0,2)]} {ctx.message.mentions[0].mention} :knife: :dizzy_face:   ", colour=discord.Color.red())
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f"{ctx.message.author.mention} {list[randint(0,2)]} {member.mention} :knife: :dizzy_face:   ", colour=discord.Color.red())
        await ctx.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member):
    if member == ctx.author:
        emb = discord.Embed(description="Ты не можешь кинуть варн сам на себя!", colour=discord.Color.red())
        await ctx.send(embed=emb)
    else:
        with open('lvl.json', 'r') as f:
            users = json.load(f)
            if not str(member.id) in users:
                users[str(member.id)] = {}
                users[str(member.id)]['exp'] = 0
                users[str(member.id)]['lvl'] = 1
                users[str(member.id)]['pred'] = 0
                if users[str(member.id)]['pred'] >= 2:
                    users[str(member.id)]['pred'] = 0
                    emb = discord.Embed(title=f"Кик ⚠", description=f"**3** из **3** предупреждений! {member.mention} был кикнут с сервера!", colour=discord.Color.red())
                    await ctx.send(embed=emb)
                    emb1 = discord.Embed(title=f"Кик ⚠", description=f"**3** из **3** предупреждений! Вы были кикнуты с сервера **`{ctx.guild}`**!", colour=discord.Color.red())
                    await member.send(embed=emb1)
                    await member.kick(reason="3 из 3 предупреждений!")
                    users[str(member.id)]['pred'] = 0
                else:
                    users[str(member.id)]['pred'] += 1
                    emb = discord.Embed(title=f"Warn ⚠", description=f"{member.mention} получил **предупреждение**! Осталось: **`{3 - users[str(member.id)]['pred']}`**", colour=discord.Color.red())
                    await ctx.send(embed=emb)
            else:
                if users[str(member.id)]['pred'] >= 2:
                    users[str(member.id)]['pred'] = 0
                    emb = discord.Embed(title=f"Кик ⚠", description=f"**3** из **3** предупреждений! {member.mention} был кикнут с сервера!", colour=discord.Color.red())
                    await ctx.send(embed=emb)
                    emb1 = discord.Embed(title=f"Кик ⚠", description=f"**3** из **3** предупреждений! Вы были кикнуты с сервера **`{ctx.guild}`**!", colour=discord.Color.red())
                    await member.send(embed=emb1)
                    await member.kick(reason="3 из 3 предупреждений!")
                    users[str(member.id)]['pred'] = 0
                else:
                    users[str(member.id)]['pred'] += 1
                    emb = discord.Embed(title=f"Warn ⚠", description=f"{member.mention} получил **предупреждение**! Осталось: **`{3 - users[str(member.id)]['pred']}`**", colour=discord.Color.red())
                    await ctx.send(embed=emb)
        with open('lvl.json', 'w') as f:
            json.dump(users, f)


@bot.command()
@commands.has_permissions(administrator=True)
async def unwarn(ctx, member: discord.Member):
    if member == ctx.author:
        emb = discord.Embed(description="Ты не можешь снять варн сам у себя!", colour=discord.Color.red())
        await ctx.send(embed=emb)
    else:
        with open('lvl.json', 'r') as f:
            users = json.load(f)
            if not str(member.id) in users:
                users[str(member.id)] = {}
                users[str(member.id)]['exp'] = 0
                users[str(member.id)]['lvl'] = 1
                users[str(member.id)]['pred'] = 0
                if users[str(member.id)]['pred'] <= 0:
                    emb = discord.Embed(description=f"У {member.mention} итак **`0`** предупреждений!", colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    users[str(member.id)]['pred'] -= 1
                    emb = discord.Embed(title=f"Unwarn ⚠", description=f"У {member.mention} сняли **предупреждение**! Осталось: **`{3 - users[str(member.id)]['pred']}`**", colour=discord.Color.red())
                    await ctx.send(embed=emb)
            else:
                if users[str(member.id)]['pred'] <= 0:
                    emb = discord.Embed(description=f"У {member.mention} итак **`0`** предупреждений!", colour=discord.Color.red())
                    await ctx.send(embed=emb)
                else:
                    users[str(member.id)]['pred'] -= 1
                    emb = discord.Embed(title=f"Unwarn ⚠", description=f"У {member.mention} сняли **предупреждение**! Осталось: **`{3 - users[str(member.id)]['pred']}`**",colour=discord.Color.red())
                    await ctx.send(embed=emb)
        with open('lvl.json', 'w') as f:
            json.dump(users, f)


@bot.command()
async def duel(ctx, com, member: discord.Member = None):
    if com == "create":
        with open('lvl.json', 'r') as f:
            users = json.load(f)
            if member == ctx.author:
                emb = discord.Embed(description=f"**Ты** не можешь начать **`дуэль`** сам с собой!",
                                    colour=discord.Color.red())
                await ctx.send(embed=emb)
            else:
                if not str(ctx.message.author.id) in users:
                    users[str(ctx.message.author.id)] = {}
                    users[str(ctx.message.author.id)]['exp'] = 0
                    users[str(ctx.message.author.id)]['lvl'] = 1
                    users[str(ctx.message.author.id)]['pred'] = 1
                    users[str(ctx.message.author.id)]['duwins'] = 0
                    users[str(ctx.message.author.id)]['ducreator'] = ctx.author.id
                    users[str(ctx.message.author.id)]['duplayer'] = member.id
                    emb = discord.Embed(title=":gun: Дуэль!",
                                        description=f"**`{ctx.message.author.display_name}`** создал дуэль с **`{member.display_name}`**, ждём его **одобрения** или **отклонения**!\n"
                                                    f"#duel accept {ctx.message.author.mention} - **принять** дуэль"
                                                    f"#duel reject {ctx.message.author.mention} - **отклонить** дуэль",
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                    emb1 = discord.Embed(title=":gun: Дуэль!",
                                        description=f"**`{ctx.message.author.display_name}`** создал дуэль с **вами** на сервере **`{ctx.guild}`**, ждём вашего **одобрения** или **отклонения**!\n"
                                                    f"#duel accept {ctx.message.author.mention} - **принять** дуэль"
                                                    f"#duel reject {ctx.message.author.mention} - **отклонить** дуэль",
                                        colour=discord.Color.red())
                    await member.send(embed=emb1)
                else:
                    users[str(ctx.message.author.id)]['ducreator'] = ctx.author.id
                    users[str(ctx.message.author.id)]['duplayer'] = member.id
                    emb = discord.Embed(title=":gun: Дуэль!",
                                        description=f"**`{ctx.message.author.display_name}`** создал дуэль с **`{member.display_name}`**, ждём его **одобрения** или **отклонения**!\n"
                                                    f"#duel accept {ctx.message.author.mention} - **принять** дуэль\n"
                                                    f"#duel reject {ctx.message.author.mention} - **отклонить** дуэль",
                                        colour=discord.Color.red())
                    await ctx.send(embed=emb)
                    emb1 = discord.Embed(title=":gun: Дуэль!",
                                         description=f"**`{ctx.message.author.display_name}`** создал дуэль с **вами** на сервере **`{ctx.guild}`**, ждём вашего **одобрения** или **отклонения**!\n"
                                                     f"#duel accept {ctx.message.author.mention} - **принять** дуэль\n"
                                                     f"#duel reject {ctx.message.author.mention} - **отклонить** дуэль",
                                         colour=discord.Color.red())
                    await member.send(embed=emb1)
        with open('lvl.json', 'w') as f:
            json.dump(users, f)
    if com == "accept":
        with open('lvl.json', 'r') as f:
            users = json.load(f)
            if not str(ctx.message.author.id) in users:
                users[str(ctx.message.author.id)] = {}
                users[str(ctx.message.author.id)]['exp'] = 0
                users[str(ctx.message.author.id)]['lvl'] = 1
                users[str(ctx.message.author.id)]['pred'] = 1
                users[str(ctx.message.author.id)]['duwins'] = 0
                users[str(ctx.message.author.id)]['ducreator'] = member.id
                users[str(ctx.message.author.id)]['duplayer'] = ctx.author.id
            else:
                users[str(ctx.message.author.id)]['ducreator'] = member.id
                users[str(ctx.message.author.id)]['duplayer'] = ctx.author.id
            if not str(member.id) in users:
                users[str(member.id)] = {}
                users[str(member.id)]['exp'] = 0
                users[str(member.id)]['lvl'] = 1
                users[str(member.id)]['pred'] = 1
                users[str(member.id)]['duwins'] = 0
                users[str(member.id)]['ducreator'] = member.id
                users[str(member.id)]['duplayer'] = 0
            if member == ctx.author:
                emb = discord.Embed(description=f"**Ты** не можешь начать **`дуэль`** сам с собой!",
                                    colour=discord.Color.red())
                await ctx.send(embed=emb)
            elif users[str(member.id)]['duplayer'] == ctx.author.id:
                shoot = randint(1, 2)
                if shoot == 1:
                    emb = discord.Embed(title=":gun: Дуэль!", description=f"Происходит **дуэль** между {ctx.message.author.mention} и {member.mention}...\n"
                                                                          f"{ctx.message.author.mention} победил **`+500 xp`**, у {member.mention} **`-500 xp`**!",
                                        colour=discord.Color.red())
                    users[str(ctx.message.author.id)]['exp'] += 500
                    users[str(ctx.message.author.id)]['duwins'] += 1
                    users[str(member.id)]['exp'] -= 500
                    users[str(member.id)]['ducreator'] = 0
                    users[str(member.id)]['duplayer'] = 0
                    users[str(ctx.message.author.id)]['ducreator'] = 0
                    users[str(ctx.message.author.id)]['duplayer'] = 0
                elif shoot == 2:
                    emb = discord.Embed(title=":gun: Дуэль!",
                                        description=f"Происходит **дуэль** между {ctx.message.author.mention} и {member.mention}...\n"
                                                    f"{member.mention} победил, **`+500 xp`**, у {ctx.message.author.mention} **`-500 xp`**!",
                                        colour=discord.Color.red())
                    users[str(ctx.message.author.id)]['exp'] -= 500
                    users[str(member.id)]['duwins'] += 1
                    users[str(member.id)]['exp'] += 500
                    users[str(member.id)]['ducreator'] = 0
                    users[str(member.id)]['duplayer'] = 0
                    users[str(ctx.message.author.id)]['ducreator'] = 0
                    users[str(ctx.message.author.id)]['duplayer'] = 0
                await ctx.send(embed=emb)
            elif users[str(member.id)]['duplayer'] != ctx.author.id:
                emb = discord.Embed(description=f"{member.mention} **не начинал** с вами **`дуэль`**!", colour=discord.Color.red())
                await ctx.send(embed=emb)
        with open('lvl.json', 'w') as f:
            json.dump(users, f)
    if com == "reject":
        with open('lvl.json', 'r') as f:
            users = json.load(f)
            if not str(ctx.message.author.id) in users:
                users[str(ctx.message.author.id)] = {}
                users[str(ctx.message.author.id)]['exp'] = 0
                users[str(ctx.message.author.id)]['lvl'] = 1
                users[str(ctx.message.author.id)]['pred'] = 1
                users[str(ctx.message.author.id)]['duwins'] = 0
                users[str(ctx.message.author.id)]['ducreator'] = 0
                users[str(ctx.message.author.id)]['duplayer'] = 0
            else:
                users[str(ctx.message.author.id)]['ducreator'] = 0
                users[str(ctx.message.author.id)]['duplayer'] = 0
            if not str(member.id) in users:
                users[str(member.id)] = {}
                users[str(member.id)]['exp'] = 0
                users[str(member.id)]['lvl'] = 1
                users[str(member.id)]['pred'] = 1
                users[str(member.id)]['duwins'] = 0
                users[str(member.id)]['ducreator'] = member.id
                users[str(member.id)]['duplayer'] = 0
            if member == ctx.author:
                emb = discord.Embed(description=f"**Ты** не можешь начать **`дуэль`** сам с собой!",
                                    colour=discord.Color.red())
                await ctx.send(embed=emb)
            elif users[str(member.id)]['duplayer'] == ctx.author.id:
                emb = discord.Embed(title=":gun: Дуэль!", description=f"**`Дуэль`** успешно отклонена", colour=discord.Color.red())
                users[str(ctx.message.author.id)]['ducreator'] = 0
                users[str(ctx.message.author.id)]['duplayer'] = 0
                await ctx.send(embed=emb)
            elif users[str(member.id)]['duplayer'] != ctx.author.id:
                emb = discord.Embed(description=f"{member.mention} **не начинал** с вами **`дуэль`**!", colour=discord.Color.red())
                await ctx.send(embed=emb)
        with open('lvl.json', 'w') as f:
            json.dump(users, f)


@bot.command()
async def rand(ctx, a=None, b=None):
    if a == None and b == None:
        c = randint(0, 1000)
    elif a == None:
        c = randint(0, int(b))
    elif b == None:
        c = randint(0, int(a))
    elif a > b:
        c = randint(int(b), int(a))
    else:
        c = randint(int(a), int(b))
    emb = discord.Embed(title="Рандомное число:", description=str(c), color=discord.Color.red())
    await ctx.send(embed=emb)


@bot.command()
async def kooolfdkorguhohgawruoppearghagrephugraepuio(ctx):
    if ctx.author.voice.channel:
        if not ctx.guild.voice_client: # error would be thrown if bot already connected, this stops the error
            player = await ctx.author.voice.channel.connect()
        else:
            player = ctx.guild.voice_client
        player.play(discord.FFmpegPCMAudio("The_Immortals_-_Techno_Syndrome_Mortal_Kombat.mp3")) # or "path/to/your.mp3"
    else:
        await ctx.send("Please connect to a voice channel.")


@bot.command()
async def fight(ctx):
    members = []
    if ctx.message.author.voice == None:
        print("Нет канала")
    else:
        for member in ctx.message.author.voice.channel.members:
            if member.id == 825328674583871539:
                members.append(member)
            elif member == ctx.author:
                pass
            elif member.bot:
                pass
            else:
                members.append(member)
    if len(members) == 1:
        if "Oky#1333" in members:
            m = "Oky#1333"
            print(m)
        else:
            m = "Oky#1333"
            while m == "Oky#1333":
                m = members[randint(0, len(members)) - 1]
            print(m)
    else:
        m = members[randint(0, len(members))-1]
        print(m)
    img = Image.open('test.png')
    url = str(ctx.author.avatar_url)[:-10]
    response = requests.get(url, stream=True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((200, 200), Image.ANTIALIAS)

    img.paste(response, (30, 30, 230, 230))

    url2 = str(m.avatar_url)[:-10]
    response2 = requests.get(url2, stream=True)
    response2 = Image.open(io.BytesIO(response2.content))
    response2 = response2.convert('RGBA')
    response2 = response2.resize((200, 200), Image.ANTIALIAS)

    img.paste(response2, (620, 30, 820, 230))

    idraw = ImageDraw.Draw(img)
    name1 = ctx.author.display_name
    name2 = m.name

    nameline1 = ImageFont.truetype('arial.ttf', size=50)
    nameline2 = ImageFont.truetype('arial.ttf', size=50)

    idraw.text((30, 240), f'{name1}', font=nameline1)
    idraw.text((620, 240), f'{name2}', font=nameline2)

    img.save('1.png')

    await ctx.send(file=discord.File(fp='1.png'))
    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        raise InvalidVoiceChannel('Нет канала, к которому можно присоединиться.')

    vc = ctx.voice_client

    if vc:
        if vc.channel.id == channel.id:
            return
        try:
            await vc.move_to(channel)
        except asyncio.TimeoutError:
            raise VoiceConnectionError(f'При переходе в канал: <{channel}> время вышло.')
    else:
        try:
            await channel.connect()
        except asyncio.TimeoutError:
            await channel.connect()
    await kooolfdkorguhohgawruoppearghagrephugraepuio(ctx)


for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'Cogs.{filename[:-3]}')
        except Exception:
            raise Exception