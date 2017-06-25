import discord
from config import Currency
from .mechanics import roll_rarity

values = {
    'trash': -500,
    'common': 25,
    'uncommon': 50,
    'rare': 100,
    'legendary': 500
}

async def fish(cmd, message, args):
    if not cmd.cooldown.on_cooldown(cmd, message):
        cmd.cooldown.set_cooldown(cmd, message, 5)
        kud = cmd.db.get_points(message.author)
        if kud['Current'] >= 200:
            cmd.db.take_points(message.guild, message.author, 20)
            rarity = roll_rarity()
            if rarity == 'trash':
                icon = 'ðŸ‘¢'
                text = 'You reeled in some trash'
            else:
                icon = 'ðŸŸ'
                text = f'You caught a {rarity} fish'
            cmd.db.add_points(message.guild, message.author, values[rarity])
            response = discord.Embed(color=0x1ABC9C, title=f'{icon} {text} earning you `{values[rarity]} {Currency}`!')
        else:
            response = discord.Embed(color=0xDB0000, title=f'You don\'t have enough {Currency}! Try and stop sucking yE?')
    else:
        timeout = cmd.cooldown.get_cooldown(cmd, message)
        response = discord.Embed(color=0x696969, title=f'ðŸ•™ Your new bait will be ready in {timeout} seconds.')
    await message.channel.send(embed=response)
