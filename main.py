import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
import os
import datetime
import codecs
from disnake.ui import Select, View
import sqlite3
import io
import aiohttp
from io import BytesIO
from disnake.enums import ButtonStyle
import pymysql
import pymysql.cursors
import asyncio
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True
import config
bot = commands.Bot(command_prefix="!" , intents=disnake.Intents.all(), test_guilds=None, command_sync_flags=command_sync_flags )
bot.remove_command( 'help' )













try:
  connect = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)  #подключення до бд
  cursor = connect.cursor()
  try:
    cursor.execute(
      "CREATE DATABASE IF NOT EXISTS zhekazz4_vertual")  #тіп створює бд
  finally:
    connect.commit()
except Exception as ex:
  print(ex)
 
 


#---------------------------------------------------цей евентс означає коли бот добавляється на сервер-------------------------------------------------------------------------------------------
@bot.event
async def on_guild_join(guild):
    mrole = disnake.utils.get(guild.roles, name="Muted")
    if mrole not in guild.roles:
        await guild.create_role(name="Muted")

#----------------------------------------------------------создає таблицю узерс коли бот добавляється на сервер----------------------------------------------------------------------------------------------------
    cursor.execute(f"create table if not exists zhekazz4_vertual.users(guild_name varchar(50), user_name varchar(50),guild int default null, user_id int default null, mute int default null, ban int default null, warn int default null, admin int default null)")  # создає таблицю
    connect.commit()
 
    for guild in bot.guilds:
        for member in guild.members:
            cursor.execute(f"select * from zhekazz4_vertual.users where guild = {guild.id} and user_id = {member.id}")
            if cursor.fetchone() is None:
                cursor.execute(f"insert into zhekazz4_vertual.users values('{member.guild.name}', '{member}',{member.guild.id}, {member.id}, 0, 0, 0, 0)")
                connect.commit()
            else:
                print('\u200b')

    cursor.execute(f"UPDATE zhekazz4_vertual.users SET admin = 6 WHERE guild = {guild.id} AND user_id = {guild.owner.id}")
    connect.commit()


#--------------------------------------------------------------создає таблицю guilds коли бот добавляється на сервер-----------------------------------------------------------------------
    cursor.execute(f"create table if not exists zhekazz4_vertual.guilds(guild_name varchar(50) , guild_id bigint default null, welcome text, cmdkick int default 3, cmdwelcome int default 5)")  # создає таблицю
    connect.commit()
 
    for guild in bot.guilds:
        for member in guild.members:
            cursor.execute(f"select * from zhekazz4_vertual.guilds where guild_name = '{guild.name}' and guild_id = {guild.id}")
            if cursor.fetchone() is None:
                cursor.execute(f"insert into zhekazz4_vertual.guilds values('{member.guild.name}', {member.guild.id}, NOT NULL, NOT NULL, NOT NULL)")
                connect.commit()
            else:
                print('\u200b')
    








#-------------------------------------------------------------------------------прогрузка бота + статус бота--------------------------------------------------------------------
 
@bot.event
async def on_ready():



 #-------------------------------------------------------------------создає таблицю users коли бот включається-------------------------------------------------------------------
    cursor.execute(f"create table if not exists zhekazz4_vertual.users(guild_name varchar(33), user_name varchar(33),guild bigint default null, user_id bigint default null, mute int default null, ban int default null, warn int default null, admin int default null)")  # создає таблицю
    connect.commit()
 
    for guild in bot.guilds:
        for member in guild.members:
            cursor.execute(f"select * from zhekazz4_vertual.users where guild = {guild.id} and user_id = {member.id}")
            if cursor.fetchone() is None:
                cursor.execute(f"insert into zhekazz4_vertual.users values('{member.guild.name}', '{member}',{member.guild.id}, {member.id}, 0, 0, 0, 0)")
                connect.commit()
            else:
                print('\u200b')



        cursor.execute(f"UPDATE zhekazz4_vertual.users SET admin = 6 WHERE guild = {guild.id} AND user_id = {guild.owner.id}")
        connect.commit()
#-------------------------------------------------------------Создає таблицю guilds коли бот включається-------------------------------------------------------------------

    cursor.execute(f"create table if not exists zhekazz4_vertual.guilds(guild_name varchar(50), guild_id bigint default null, welcome text default null, cmdkick int default 3, cmdwelcome int default 5)")  # создає таблицю
    connect.commit()
 
    for guild in bot.guilds:
        cursor.execute(f"select * from zhekazz4_vertual.guilds where guild_name = '{guild.name}' and guild_id = {guild.id}")
        if cursor.fetchone() is None:
            cursor.execute(f"insert into zhekazz4_vertual.guilds(guild_name, guild_id) values('{guild.name}' , {guild.id})")
            connect.commit()
        else:
            print('\u200b')




#--------------------------------------------------------------------добавляє всю інфу в users про чела коли він заходить на сервер-----------------------------------------------------
 
@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = bot.get_channel(1060175369161953390)
    give_role = disnake.utils.get(member.guild.roles, id = 1059987183123038259)
    embed=disnake.Embed(description=f'**☆ VertualWorld ☆**', color= 0x00fa6a)
    embed.add_field(name= f' Добро пожаловать на\nсервер, {member}!', value="", inline=False)
    embed.set_footer(text = f"🌟 ∙ Вы {guild.member_count} Участник")
    embed.set_thumbnail(url = member.avatar)
    await member.add_roles(give_role)
    await channel.send(embed=embed)




    for member in member.guild.members:
        cursor.execute(f"select guild, user_id from zhekazz4_vertual.users where guild = {member.guild.id} and user_id = {member.id}")
        if cursor.fetchone() is None:
            cursor.execute(f"insert into zhekazz4_vertual.users values('{member.guild.name}', '{member}',{member.guild.id}, {member.id}, 0, 0, 0, 0)")
            connect.commit()
        else:
            print('\u200b')

#-------------------------------------------------------------------Добававляє всю інфу в guilds коли чел заходить на сервер----------------------------------------------
    for member in member.guild.members:
        cursor.execute(f"select guild_name ,guild_id from zhekazz4_vertual.guilds where guild_name = '{member.guild.name}' and guild_id = {member.guild.id}")
        if cursor.fetchone() is None:
            cursor.execute(
                f"insert into zhekazz4_vertual.guilds values({member.guild.id} ,{member.guild.id}, NOT NULL, NOT NULL, NOT NULL)")
            connect.commit()
        else:
            print('\u200b')




@bot.event
async def on_member_remove(member):
    guild = member.guild
    channel = bot.get_channel(1060175369161953390)
    embed=disnake.Embed(description=f'**☆ VertualWorld ☆**', color= 0x00fa6a)
    embed.add_field(name= f' Прощай {member}!', value="", inline=False)
    embed.set_footer(text = f"😞 ∙ Теперь нас {guild.member_count}")
    embed.set_thumbnail(url = member.avatar)
    await channel.send(embed=embed)

    cursor.execute(
        f"update zhekazz4_vertual.users set admin = 0 where user_id = {member.id} and guild = {member.guild.id}")
    connect.commit()


#---------------------------------------------------------!setadm-----------------------------------------------------
@bot.command(name = "setadm")
async def setadm(ctx, user:disnake.Member,* , lvl:int): 
    cursor.execute(f"select * from zhekazz4_vertual.users where guild = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
    _admin = cursor.fetchone()['admin']
    cursor.execute(f"select * from zhekazz4_vertual.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
    admins = cursor.fetchone()['admin']
    if _admin <5:
        emb4 = disnake.Embed(title=" Мне кажется, что что-то пошло не так ",  description= f'\n▹ У вас не хватает прав для использавания команды ', color=0x00fa6a)
        await ctx.send(embed = emb4)
    else:
        if _admin < admins:
            embed=disnake.Embed(title=f'Мне кажется, что что-то пошло не так', description=f'Вы не можете повысить пользователя у которого уровень больше вашего! ', color= 0x00fa6a)
            await ctx.send(embed=embed)
        else:
            if user == ctx.author:
                emb4 = disnake.Embed(title=" Мне кажется, что что-то пошло не та ",  description= f'\n▹ Мне кажеться вы хотите повысить самого себя \n Простите но вы не можете этого зделать ', color=0x00fa6a)
                await ctx.send(embed = emb4)
            else:
                if lvl <0:
                    emb4 = disnake.Embed(title=" Мне кажется, что что-то пошло не так ",  description= f'\n▹ Значение не должно быть ниже 0 ', color=0x00fa6a)
                    await ctx.send(embed = emb4)
                if lvl >5:
                        embed7 = disnake.Embed(title=" Мне кажется, что что-то пошло не так ", description=f"▹ Ви указали не верный уровень администратора! Должно быть от 0 до 5", color=0x00fa6a)
                        await ctx.send(embed=embed7)

                else:
                    if _admin == 5:
                        if lvl == 0:
                            cursor.execute(f"update zhekazz4_vertual.users set admin = 0 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам cняли права администратора на сервере `{ctx.guild.name}`', description=f'Команду выполнил пользователь: {ctx.author.mention}', color= 0x00fa6a)
                            await user.send(embed=embed)
                                
                            embed1=disnake.Embed(title= 'Выдача прав администратора' , description=f'Пользователь {user.mention} теперь обычный пользователь! ', color=0x00fa6a)
                            embed1.add_field(name='Команду выполнил:', value=f'{ctx.author.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 1:
                            cursor.execute(f"update zhekazz4_vertual.users set admin = 1 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам выдали `{lvl}` уровень администратора на сервере `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.author.mention}', color= 0x00fa6a)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права администратора' , description=f'Пользователь {user.mention} получил {lvl} уровень администратора ', color=0x00fa6a)
                            embed1.add_field(name='Команду выполнил:', value=f'{ctx.author.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 2:
                            cursor.execute(f"update zhekazz4_vertual.users set admin = 2 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам выдали `{lvl}` уровень администратора на сервере `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.author.mention}', color= 0x00fa6a)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права администратора' , description=f'Пользователь {user.mention} получил {lvl} уровень администратора ', color=0x00fa6a)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.author.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 3:
                            cursor.execute(f"update zhekazz4_vertual.users set admin = 3 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам выдали `{lvl}` уровень администратора на сервере `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.author.mention}', color= 0x00fa6a)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права администратора' , description=f'Пользователь {user.mention} получил {lvl} уровень администратора ', color=0x00fa6a)
                            embed1.add_field(name='Команду выполнил:', value=f'{ctx.author.mention}', inline=True)
                            await ctx.send(embed=embed1)


                        if lvl == 4:
                            cursor.execute(f"update zhekazz4_vertual.users set admin = 4 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам выдали `{lvl}` уровень администратора на сервере `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.author.mention}', color= 0x00fa6a)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права администратора' , description=f'Пользователь {user.mention} получил {lvl} уровень администратора ', color=0x00fa6a)
                            embed1.add_field(name='Команду виконав:', value=f'{ctx.author.mention}', inline=True)
                            await ctx.send(embed=embed1)


                        if lvl >=5:
                            embed7 = disnake.Embed(title="Мне кажется, что что-то пошло не так", description=f"▹ Максимальный уровень который вы можете выдать это `4`", color=0x00fa6a)
                            await ctx.reply(embed=embed7)


                    if _admin == 6:
                        if lvl == 0:
                            cursor.execute(f"update zhekazz4_vertual.users set admin = 0 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам cняли права администратора на сервере `{ctx.guild.name}`', description=f'Команду выполнил пользователь: {ctx.author.mention}', color= 0x00fa6a)
                            await user.send(embed=embed)
                                
                            embed1=disnake.Embed(title= 'Выдача прав администратора' , description=f'{user.mention} теперь обычный пользователь! ', color=0x00fa6a)
                            embed1.add_field(name='Команду выполнил:', value=f'{ctx.author.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 1:
                            cursor.execute(f"update zhekazz4_vertual.users set admin = 1 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам выдали `{lvl}` уровень администратора на сервере `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.author.mention}', color= 0x00fa6a)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права администратора' , description=f'Пользователь {user.mention} получил {lvl} уровень администратора ', color=0x00fa6a)
                            embed1.add_field(name='Команду выполнил:', value=f'{ctx.author.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 2:
                            cursor.execute(f"update zhekazz4_vertual.users set admin = 2 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам выдали `{lvl}` уровень администратора на сервере `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.author.mention}', color= 0x00fa6a)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права администратора' , description=f'Пользователь {user.mention} получил {lvl} уровень администратора ', color=0x00fa6a)
                            embed1.add_field(name='Команду выполнил:', value=f'{ctx.author.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 3:
                            cursor.execute(f"update zhekazz4_vertual.users set admin = 3 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам выдали `{lvl}` уровень администратора на сервере `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.author.mention}', color= 0x00fa6a)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права администратора' , description=f'Пользователь {user.mention} получил {lvl} уровень администратора ', color=0x00fa6a)
                            embed1.add_field(name='Команду выполнил:', value=f'{ctx.author.mention}', inline=True)
                            await ctx.send(embed=embed1)

                        if lvl == 4:
                            cursor.execute(f"update zhekazz4_vertual.users set admin = 4 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам выдали `{lvl}` уровень администратора на сервере `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.author.mention}', color= 0x00fa6a)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права администратора' , description=f'Пользователь {user.mention} получил {lvl} уровень администратора ', color=0x00fa6a)
                            embed1.add_field(name='Команду выполнил:', value=f'{ctx.author.mention}', inline=True)
                            await ctx.send(embed=embed1)
                        if lvl == 5:
                            cursor.execute(f"update zhekazz4_vertual.users set admin = 5 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=disnake.Embed(title=f'Вам выдали `{lvl}` уровень администратора на сервере `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.author.mention}', color= 0x00fa6a)
                            await user.send(embed=embed)
                            
                            embed1=disnake.Embed(title= 'Выдача права администратора' , description=f'Пользователь {user.mention} получил {lvl} уровень администратора ', color=0x00fa6a)
                            embed1.add_field(name='Команду выполнил:', value=f'{ctx.author.mention}', inline=True)
                            await ctx.send(embed=embed1)

@setadm.error
async def setadm(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb3 = disnake.Embed(title= "Изменить уровень администратора", description = "▹ Изменяйте уровни администратора на сервере", color=0x00fa6a)
        emb3.add_field(name = " Использование ", value = "▹!setadm  @<пользователь> <уровень>\n ┗ `<учасник>` - может принимать цифровой ID учасника или упоминание его.\n Обязательный параметр\n ┗ `<уровень>` - может принимать значение от 0-5. \n Обязательный параметр  " ,inline=False )
        await ctx.reply(embed=emb3)
    if isinstance(error, commands.BadArgument):
        emb4 = disnake.Embed(title="Мне кажется, что что-то пошло не так",  description= f'\n▹ Упс, кажеться пользователь не найден. ', color=0x00fa6a)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | VertualWorld (c) 2023 •   ', icon_url=ctx.author.avatar,  )
        message = await ctx.send(embed = emb4)



#---------------------------------------------------------!clear--------------------------------------------------------

@bot.command()
async def clear(ctx, amount):
    cursor.execute(f"select * from zhekazz4_vertual.users where guild = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
    _admin = cursor.fetchone()['admin']
    if _admin <2:
        emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0x00fa6a)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar,  )
        message = await ctx.send(embed = emb4)
    else:
        await ctx.channel.purge(limit=int(amount))
        emb4 = disnake.Embed(title="Успешно :white_check_mark: ",  description= f'Cообщений было очищено: {amount}', color=0x00fa6a)
        message = await ctx.send(embed = emb4)


@clear.error
async def сlear(ctx, error):
    try: 
        if isinstance(error, commands.MissingRequiredArgument):
            emb3 = disnake.Embed(title="Очистить последние сообщения в текущем канале", color=0x00fa6a)
            emb3.add_field(name = " Использование ", value = "`.clear <количество сообщений>`\n ┗ Параметр <> обезательное к использованию. " ,inline=False )
            emb3.add_field(name = " Пример ", value = "`!clear 10`\n ┗ Удалит последние 10 сообщений в текущем канале. " ,inline=False )
            emb3.add_field(name = " Важно ", value = "`При удалении большого количества сообщений нужно больше подождать до момента пока вы не получите сообщение от бота что все сообщения удалены`\n ┗ Проблема в лимитах Discord'а  " ,inline=False )
            await ctx.reply(embed=emb3)
    except Exception as ex:
        print(ex)


#------------------------------------------------------!info-------------------------------------------------------------

@bot.command(name = "info")
async def info(ctx): 
    embed=disnake.Embed(title=f'Вам не нужно играть на проекте VertualWorld!', description=f'', color= 0x00fa6a )
    embed.add_field(name=':crossed_swords:   Вы же не хотите быть участником войн, где принимают участие сотни игроков. Не хотите получать удовольствие от большого выбора серверов. Не хотите опробовать себя в чем-то новом.', value='', inline=False)
    embed.add_field(name=':brain:  Если же вы уже сомневаетесь, то уже есть смысл познакомиться с проектом!', value='', inline=False)
    embed.add_field(name=':boom:  VertualWorld – взрывной проект Minecraft, который предоставляет большое количество режимов: PrisonEVO, BossFight, Rpg( Vixion ),  MyLittleFarm, Towny, Evita. ', value='', inline=False)
    embed.add_field(name=':smiley:  Каждый игрок извлекает массу положительных эмоций, находит новых друзей, познает мир и даже развивается.', value='', inline=False)   
    embed.add_field(name=':computer:  Сервер каждый день движется вперед! Разрабатываются новые режимы, улучшаются старые, создаются уникальные механики и концепты.', value='', inline=False)
    embed.add_field(name=':book:  За соблюдением правил наблюдает профессиональная команда. Она грамотно следит за игровым процессом, наказывает нарушителей и разрешает конфликты.', value='', inline=False)
    embed.set_footer(text = f"Измени свою жизнь вместе с VertualWorld! ")
    await ctx.author.send(embed=embed)





#---------------------------------------------------!help------------------------------------------------------------------------
@bot.command(name = "help")
async def help(ctx):
    select = Select(
        placeholder= "Виберите тип помощи",
        options=[
            disnake.SelectOption(label = "Информационые команды", description = "Команды про информацию, сервера, пользователей и тд" ,emoji="💻"),
            disnake.SelectOption(label = "Команды для модерации", description = "Разные команды для модерации!" , emoji="⚙"),
            disnake.SelectOption(label = "Все команды", description = "Список всех команд" ,emoji="💾")
        ]
    )

    async def call_back(intaraction):
        if intaraction.author.id == ctx.author.id:
            value = select.values[0]
            view.remove_item(select)

            information = " ```!help - список всех команд``` ```!info - информация про VertualWorld```"
            moderation = "```!setadm - изменить уровень администратора```"
            others = "" 

            if value == "Информационые команды":
                emb = disnake.Embed(title = "Информационые команды:", description=information, color = 0x00fa6a)
                emb.set_footer(text = f"VertualWorld 2023©", icon_url=bot.user.display_avatar)
                await intaraction.response.edit_message(embed = emb)
            elif value == "Команды для модерации":
                emb = disnake.Embed(title = "Команды для модерации:", description=moderation, color = 0x00fa6a)
                emb.set_footer(text = f"VertualWorld 2023©", icon_url=bot.user.display_avatar)
                await intaraction.response.edit_message(embed = emb)
            elif value == "Все команды":
                emb = disnake.Embed(title ="Все команды:", description=f"{information}\n{moderation}\n{others}", color = 0x00fa6a)
                emb.set_footer(text = f"VertualWorld 2023©", icon_url=bot.user.display_avatar)
                await intaraction.response.edit_message(embed = emb)
        else:
            await intaraction.response.send_message("Это не твоя кнопка!", ephemeral=True)  

    select.callback = call_back
    view = View()
    view.add_item(select)

    emb = disnake.Embed(title = f"Cписок команд бота", description="Виберите тип помощи ниже!", color = 0x00fa6a)
    emb.set_thumbnail(url=ctx.guild.icon)
    emb.set_footer(text = f"VertualWorld 2023©", icon_url=bot.user.display_avatar)

    await ctx.send(embed = emb, view = view)



#-----------------------------------------!mute----------------------------------------------------

@bot.command(pass_context = True, aliases=["Mute", "MUte", "MUTe", "MUTE", "mutE", "muTE", "mUTE", "MuTe", "mUtE"])
async def mute(ctx, user: disnake.Member,  time:int = None,*, reason=None):
    try:
        cursor.execute(f"select * from zhekazz4_vertual.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
        _admin = cursor.fetchone()['admin']
        cursor.execute(f"select * from zhekazz4_vertual.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
        admins = cursor.fetchone()['admin']
        if _admin <3:
            emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0x00fa6a)
            emb4.set_footer(text=f'Отправлено: {ctx.author}  | VertualWorld 2023©   ', icon_url=bot.user.display_avatar  )
            message = await ctx.send(embed = emb4)
        else:
            if _admin < admins:
                embed=disnake.Embed(title=f'Что-то пошло не так', description=f'Вы не можете взаемодействовать с пользователем у которого уровень администратора выше вашего! ', color= 0x00fa6a)
                await ctx.send(embed=embed)
            else:
                role = disnake.utils.get(ctx.guild.roles, name='Muted') 
                if user == ctx.author :
                    emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Вы не можете выдать блокировку чата самому себе! ', color=0x00fa6a)
                    emb4.set_footer(text=f'Отправлено: {ctx.author}  | VertualWorld 2023©   ', icon_url=bot.user.display_avatar  )
                    message = await ctx.send(embed = emb4)  
                elif role in user.roles:
                    emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, учасник уже заблокирован в данных каналах ', color=0x00fa6a)
                    emb4.set_footer(text=f'Отправлено: {ctx.author}  | VertualWorld 2023©   ', icon_url=bot.user.display_avatar  )
                    message = await ctx.send(embed = emb4) 
                elif time >=1441:
                    emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Время должно быть больше/равно 1 и меньше/равно 1440 ', color=0x00fa6a)
                    emb4.set_footer(text=f'Отправлено: {ctx.author}  | VertualWorld 2023©   ', icon_url=bot.user.display_avatar  )
                    message = await ctx.send(embed = emb4)
                elif time <1:
                    emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Время должно быть больше/равно 1 и меньше/равно 1440 ', color=0x00fa6a)
                    emb4.set_footer(text=f'Отправлено: {ctx.author}  | VertualWorld 2023©   ', icon_url=bot.user.display_avatar  )
                    message = await ctx.send(embed = emb4)             

                else:
                    if not reason:
                        emb4 = disnake.Embed(title=f"Успешное выполнение команды", description = f"▹Учасник {user.mention} получил блокировку в текстовых каналах", color=0x00fa6a) 
                        emb4.add_field(name = "Команду выполнил", value = f"\n ▹ {ctx.message.author.mention} "  )
                        emb4.add_field(name = "Время", value = f"\n {time} мин. "  )
                        await ctx.send(embed=emb4)
                    else:
                        emb4 = disnake.Embed(title=f"Успешное выполнение команды", description = f"▹Учасник {user.mention} получил блокировку в текстовых каналах", color=0x00fa6a) 
                        emb4.add_field(name = "Команду выполнил", value = f"\n ▹ {ctx.message.author.mention} "  )
                        emb4.add_field(name = "Время", value = f"\n {time} мин. "  )
                        emb4.add_field(name = "Причиной тому стало", value = f"\n ▹ {reason}", inline = False) 
                        await ctx.send(embed=emb4)
                    await user.add_roles(role) 
                    guild = ctx.guild
                    for channels in guild.channels:
                        await channels.set_permissions(role, send_messages=False)
                    time = time * 60
                    await asyncio.sleep(time)
                    await user.remove_roles(role)
    except Exception as ex:
        print(ex)

@mute.error
async def mute(ctx, error):
    try: 
        if isinstance(error, commands.MissingRequiredArgument):
            emb3 = disnake.Embed(title= "Бан в текстовых каналах", description = "▹ Участник нарушает правила текстового канала? Накажите его блокировкой чата. Вы можете выдать мут от 1 минуты и до 24-ех часов", color=0x00fa6a)
            emb3.add_field(name = " Используйте ", value = "▹`.mute  @<учасник> <время> <причина>`\n ┗ `<участник>` - может принимать цифровой ID участника или упоминание его. Обязательный параметр\n ┗ `<время>` - принимает только числа от 1 и до 1440 (24 часа). Обязательный параметр \n ┗ `<причина>` - Необязательный параметр" ,inline=False )
            await ctx.reply(embed=emb3)
    except Exception as ex:
        print(ex)




@bot.command()
async def unmute(ctx, user: disnake.Member):
    cursor.execute(f"select * from zhekazz4_vertual.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
    _admin = cursor.fetchone()['admin']
    cursor.execute(f"select * from zhekazz4_vertual.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
    admins = cursor.fetchone()['admin']
    if _admin <3:
        emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | VertualWorld 2023©   ', icon_url=bot.user.display_avatar  )
        message = await ctx.send(embed = emb4)
    else:
        if _admin < admins:
            embed=disnake.Embed(title=f'Что-то пошло не так', description=f'Вы не можете взаемодействовать с пользователем у которого уровень администратора выше вашего! ', color= 0xffff00)
            await ctx.send(embed=embed)
        else:
            try: 
                mutedRole = disnake.utils.get(ctx.guild.roles, name="Muted")
                author = ctx.message.author
                if user == author:
                    emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, вы не можете розмутить самого себя ', color=0x008080)
                    emb4.set_footer(text=f'Отправлено: {ctx.author}  | VertualWorld 2023©   ', icon_url=bot.user.display_avatar  )
                    message = await ctx.send(embed = emb4)
                elif mutedRole not in user.roles:
                        emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, кажеться пользователь не замучен ', color=0x008080)
                        emb4.set_footer(text=f'Отправлено: {ctx.author}  | VertualWorld 2023©   ', icon_url=bot.user.display_avatar  )
                        message = await ctx.send(embed = emb4)
                else:
                    await user.remove_roles(mutedRole)
                    emb4 = disnake.Embed(title=f"Амнистия", description = f"▹ Учасник {user.mention} разблокирован в текстовых каналах администратором", color = 0x008080) 
                    emb4.add_field(name = "Пожалел", value = f"\n ▹ {ctx.author.mention} "  )
                    await ctx.send(embed=emb4)
            except Exception as ex:
                print(ex)

@unmute.error
async def unmute_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, кажеться пользователь не найден. ', color=0x008080)
            emb4.set_footer(text=f'Отправлено: {ctx.author}  | VertualWorld 2023©   ', icon_url=bot.user.display_avatar  )
            message = await ctx.send(embed = emb4)



#---------------------------------------------------------logs---------------------------------------------------


@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(1074071089346527232)
    embed = disnake.Embed(title= f"Логирование\n", description = f"Удаленые сообщения", color=0x00fa6a )
    embed.add_field(name = "Кто удалил:", value = f"\n ▹ {message.author.name} ", inline = False )
    embed.add_field(name = "Сообщение:", value = f"\n ▹ {message.content} ", inline = False  )
    embed.add_field(name = "Где удалено:", value = f"\n ▹ {message.channel.name} "  )
    await channel.send(embed=embed)

@bot.event
async def on_message_edit(message_before, message_after):
    channel = bot.get_channel(1074071089346527232)
    embed = disnake.Embed(title= f"Логирование\n", description = f"Изменение сообщения", color=0x00fa6a )
    embed.add_field(name = "Кто изменил:", value = f"\n ▹ {message_before.author.name} ", inline = False )
    embed.add_field(name = "Сообщение до:", value = f"\n ▹ {message_before.content} ", inline = False  )
    embed.add_field(name = "Сообщение после:", value = f"\n ▹ {message_after.content} ", inline = False )
    embed.add_field(name = "Где изменено:", value = f"\n ▹ {message_before.channel.name} "  )
    await channel.send(embed=embed)

#---------------------------------------!embed-------------------------------------------------------------------------




@bot.command()
async def embed(ctx,channel:disnake.TextChannel, title, *, arg):
    await ctx.channel.purge(limit=1)
    embed=disnake.Embed(title=f'{title}', description=f'{arg}', color=0x00fa6a)
    await channel.send(embed=embed)


@embed.error
async def embed(ctx, error):
    try: 
        if isinstance(error, commands.MissingRequiredArgument):
            emb3 = disnake.Embed(title= "Отправить EMBED", description = "▹  Используйте эту команду для того чтобы отправить EMBED сообщение", color=0x00fa6a)
            emb3.add_field(name = " Используйте ", value = "▹`!embed  #<канал> <title> <arg> `\n ┗ `#<канал>` - может принимать упоминание канала. Обязательный параметр\n ┗ `<title>` - Загаловок Embed'a. Обязательный параметр \n ┗ `<arg>` - Основной текст Embed'a. Обязательный параметр" ,inline=False )
            await ctx.reply(embed=emb3)
    except Exception as ex:
        print(ex)

#-----------------------------------------------!kick------------------------------------------------------------
@bot.command()
async def kick(ctx, user: disnake.Member, *, reason = None):
    cursor.execute(f"select * from zhekazz4_vertual.users where guild = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
    _admin = cursor.fetchone()['admin']
    cursor.execute(f"select * from zhekazz4_vertual.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
    admins = cursor.fetchone()['admin']
    if _admin <3:
        emb4 = disnake.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar,  )
        message = await ctx.send(embed = emb4)
    else:
        if _admin < admins:
            embed=disnake.Embed(title=f'Что-то пошло не так', description=f'Вы не можете взаимодействовать с пользователем у которого уровень администратора выше вашего! ', color= 0xffff00)
            await ctx.send(embed=embed)
        else:
          if not reason:
            await user.kick()
            emb4 = disnake.Embed(title="Успешное выполнение команды :white_check_mark: ",  description= f'▹Учасник {user.mention} исключен\n ', color=0x008080)
            emb4.add_field(name = " Команду выполнил \n ", value = f"▹ {ctx.author.mention}")
            message = await ctx.send(embed = emb4)
          else:
            await user.kick(reason=reason)
            emb4 = disnake.Embed(title="Успешное выполнение команды :white_check_mark: ",  description= f'▹Учасник {user.mention} исключен\n ', color=0x008080)
            emb4.add_field(name = " Команду выполнил \n ", value = f"▹ {ctx.author.mention}")
            emb4.add_field(name = " Причиной тому стало \n ", value =  f"▹ {reason}")
            message = await ctx.send(embed = emb4)


@kick.error
async def kick(ctx, error):
    try: 
        if isinstance(error, commands.MissingRequiredArgument):
            emb3 = disnake.Embed(title= "Исключить из сервера", description = "▹ У вас есть возможность изгнать учасника, но при этом у него останеться возможность вернуться обратно.",color=0x008080)
            emb3.add_field(name = " Использование ", value = "▹`!kick  @<учасник> <причина>`\n ┗ `<учасник>` - может принимать цифровой ID учасника или упоминание его.\n Обезательный параметр\n ┗ `<причина>` - Необезательный параметр  " ,inline=False )
            await ctx.reply(embed=emb3)
    except Exception as ex:
        print(ex)

#-------------------------------------роль по реации--------------------------------------




bot.run('')

