﻿import discord
from sigma.core.utils import user_avatar
from config import Currency1


async def death(cmd, message, args):
    # command name
    if message.mentions:
        target = message.mentions[0]
        # @Name
    else:
        target = message.author
    point_data = cmd.db.get_points(target)
    if point_data:
        total_pts = point_data['Total']
        current_pts = point_data['Current']
        servers = point_data['Servers']
        curr_srv = 0
        if str(message.guild.id) in servers:
            curr_srv = servers[str(message.guild.id)]
        response = discord.Embed(color=0x1ABC9C)
        response.set_author(name=f'{target.name}\'s Currency1 Data', icon_url=user_avatar(target))
        response.add_field(name='Current Wallet', value=f'```py\n{current_pts} {Currency1}\n```')
        # displays current amount of points for "currency #1"
        response.add_field(name='This Server', value=f'```py\n{curr_srv} {Currency1}\n```')
        # displays amount of points in the current server the command was used in
        response.add_field(name='Total Gained', value=f'```py\n{total_pts} {Currency1}\n```')
        # displays total amount of points gained throughout every server the bot's resided in
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 I couldn\'t find {target.name} in my point database.')
        # Player pinged does not exist
    response.set_footer(text=f'{Currency1} can be earned by being an active member of the server.')
    # Has no points
    await message.channel.send(None, embed=response)
# everything {currency1} is the name of given points and can be altered
