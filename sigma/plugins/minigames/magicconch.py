import random
import yaml
import discord


async def magicconch(cmd, message, args):
    # command name
    if args:
        question = ' '.join(args)
        with open(cmd.resource('eb_answers.yml')) as eball_file:
            content = yaml.safe_load(eball_file)
            answers = content['answers'] 
            # pulls content from "answers" file in "res"
            answer = random.choice(answers)
            # allows answers to be choose at a random interval
            embed = discord.Embed(color=0x1abc9c, title='🎱 You Gaze Into The Magic Conch')
            # Text at top
            embed.add_field(name='Question', value='```\n' + question + '\n```', inline=True)
            embed.add_field(name='Answer', value='```\n' + answer + '\n```', inline=True)
            await message.channel.send(None, embed=embed)
    else:
        await message.channel.send(cmd.help())
        return
