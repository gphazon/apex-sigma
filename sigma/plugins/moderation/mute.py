﻿from sigma.core.permission import check_man_msg
from sigma.core.permission import check_man_roles
from sigma.core.permission import check_write
import discord
import asyncio


async def mute(cmd, message, args):
    channel = message.channel
    server = message.server
    if not message.mentions:
        await message.channel.send(cmd.help())
        return
    user_q = message.mentions[0]
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    if message.author is not user_q:
        if check_man_msg(message.author, channel) and check_man_roles(message.author, channel):
            if args:
                try:
                    timeout_period = int(args[0])
                except:
                    embed = discord.Embed(color=0xDB0000, title='❗ Invalid number of seconds for the timeout.')
                    await message.channel.send(None, embed=embed)
                    return
            else:
                timeout_period = None
            for chan in server.channels:
                if str(chan.type).lower() == 'text':
                    if check_write(user_q, chan):
                        await cmd.bot.edit_channel_permissions(chan, user_q, overwrite)
            embed = discord.Embed(color=0x66CC66, title='✅ ' + user_q.name + ' muted.')
            await message.channel.send(None, embed=embed)
            if timeout_period:
                await asyncio.sleep(timeout_period)
                for chan in server.channels:
                    if str(chan.type).lower() == 'text':
                        if not check_write(user_q, chan):
                            await cmd.bot.delete_channel_permissions(chan, user_q)
                embed = discord.Embed(color=0x66CC66, title='✅ ' + user_q.name + ' can write again.')
                await message.channel.send(None, embed=embed)
        else:
            out_content = discord.Embed(type='rich', color=0xDB0000,
                                        title='⛔ Insufficient Permissions. Requires Manage Messages and Manage Roles Permissions.')
            await message.channel.send(None, embed=out_content)
