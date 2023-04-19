# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia
• `{i}q <color-optional>`
• `{i}q @username`
• `{i}q r <color-optional>`
• `{i}q count` : `multiple quotes`
    Buat kutipan..
"""
import os
import time
from datetime import datetime as dt
from random import choice
from shutil import rmtree

import pytz
from bs4 import BeautifulSoup as bs
from telethon.tl.types import DocumentAttributeVideo

from Ayra.fns.google_image import googleimagesdownload
from Ayra.fns.tools import metadata

from . import (
    HNDLR,
    AyConfig,
    async_searcher,
    bash,
    downloader,
    eod,
    get_string,
    mediainfo,
    quotly,
    ayra_bot,
    ayra_cmd,
    uploader,
)
from .Karbon import all_col

File = []


@ayra_cmd(pattern="q( (.*)|$)", manager=True, allow_pm=True)
async def quott_(event):
    match = event.pattern_match.group(1).strip()
    if not event.is_reply:
        return await event.eor("`Mohon Balas Ke Pesan..`")
    msg = await event.eor(get_string("com_1"))
    reply = await event.get_reply_message()
    replied_to, reply_ = None, None
    if match:
        spli_ = match.split(maxsplit=1)
        if (spli_[0] in ["r", "reply"]) or (
            spli_[0].isdigit() and int(spli_[0]) in range(1, 21)
        ):
            if spli_[0].isdigit():
                if not event.client._bot:
                    reply_ = await event.client.get_messages(
                        event.chat_id,
                        min_id=event.reply_to_msg_id - 1,
                        reverse=True,
                        limit=int(spli_[0]),
                    )
                else:
                    id_ = reply.id
                    reply_ = []
                    for msg_ in range(id_, id_ + int(spli_[0])):
                        msh = await event.client.get_messages(event.chat_id, ids=msg_)
                        if msh:
                            reply_.append(msh)
            else:
                replied_to = await reply.get_reply_message()
            try:
                match = spli_[1]
            except IndexError:
                match = None
    user = None
    if not reply_:
        reply_ = reply
    if match:
        match = match.split(maxsplit=1)
    if match:
        if match[0].startswith("@") or match[0].isdigit():
            try:
                match_ = await event.client.parse_id(match[0])
                user = await event.client.get_entity(match_)
            except ValueError:
                pass
            match = match[1] if len(match) == 2 else None
        else:
            match = match[0]
    if match == "random":
        match = choice(all_col)
    try:
        file = await quotly.create_quotly(
            reply_, bg=match, reply=replied_to, sender=user
        )
    except Exception as er:
        return await msg.edit(str(er))
    message = await reply.reply("Quotly by Ayra", file=file)
    os.remove(file)
    await msg.delete()
    return message