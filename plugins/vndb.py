from Shosetsu import Shosetsu

setsu = Shosetsu()
from plugin import Plugin
from config import cmd_vndb
import requests
import os
from PIL import Image
from io import BytesIO
import sys
from utils import create_logger


class VNDBSearch(Plugin):
    is_global = True
    log = create_logger(cmd_vndb)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_vndb + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'VNDB Search'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            vndb_input = (str(message.content[len(cmd_vndb) + 1 + len(pfx):]))
            search = message.content[len(pfx) + len(cmd_vndb) + 1:]
            sdata = await setsu.search_vndb('v', vndb_input)
            print(sdata)
            try:
                n = 0
                list_text = '```'
                for entry in sdata:
                    n += 1
                    list_text += '\n#' + str(n) + ' ' + entry['name']
                if len(sdata) > 1:
                    await self.client.send_message(message.channel, list_text + '\n```')
                    choice = await self.client.wait_for_message(author=message.author, channel=message.channel, timeout=20)
                    await self.client.send_typing(message.channel)
                    try:
                        nh_no = int(choice.content) - 1
                    except:
                        await self.client.send_message(message.channel,
                                                       'Not a number or timed out... Please start over')
                else:
                    nh_no = 0
            except:
                await self.client.send_message(message.channel, 'Error: ' + sys.exc_info()[0])
                return
            choice_id = sdata[nh_no]['id']
            data = await setsu.get_novel(choice_id)
            vn_title = data['titles']['english']
            vn_img = data['img']
            vn_devs = ''
            for dev in data['developers']:
                vn_devs += str(dev)
            vn_desc = data['description']
            vn_id = data['id']
            vn_len = data['length']
            if data['tags']['erotic'] == None:
                nsfw = 'Yes'
            else:
                nsfw = 'No'
            if len(vn_desc) > 300:
                suffix = '...'
            else:
                suffix = ''
            if len(vn_title) > 21:
                tit_sfx = '...'
            else:
                tit_sfx = ''
            vn_cover_raw = requests.get(vn_img).content
            vn_cover_res = Image.open(BytesIO(vn_cover_raw))
            vn_cover = vn_cover_res.resize((251, 321), Image.ANTIALIAS)
            base = Image.open('img/ani/base.png')
            overlay = Image.open('img/ani/overlay_vn.png')
            base.paste(vn_cover, (100, 0))
            base.paste(overlay, (0, 0), overlay)
            base.save('cache\\ani\\vn_' + message.author.id + '.png')
            print(vn_title)
            try:
                await self.client.send_file(message.channel, 'cache\\ani\\vn_' + message.author.id + '.png')
                await self.client.send_message(message.channel,
                                               'Title: `' + vn_title + '`\nDescription:```\n' + vn_desc[
                                                                                                       :300] + suffix + '\n```')
                os.remove('cache\\ani\\vn_' + message.author.id + '.png')
            except:
                await self.client.send_message(message.channel, 'Error: ' + sys.exc_info()[0])