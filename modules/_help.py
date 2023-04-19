# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

from telethon.errors.rpcerrorlist import (
    BotInlineDisabledError,
    BotMethodInvalidError,
    BotResponseTimeoutError,
)
from telethon.tl.custom import Button

from Ayra.dB._core import HELP, LIST
from Ayra.fns.tools import cmd_regex_replace

from . import HNDLR, LOGS, OWNER_NAME, asst, ayra_cmd, get_string, udB

_main_help_menu = [
    [
        Button.inline(get_string("help_4"), data="uh_Official_"),
        #Button.inline(get_string("help_5"), data="uh_Addons_"),
    ],
]


@ayra_cmd(pattern="help( (.*)|$)")
async def _help(ayra):
    plug = ayra.pattern_match.group(1).strip()
    chat = await ayra.get_chat()
    if plug:
        try:
            if plug in HELP["Official"]:
                output = f"**Plugin** - `{plug}`\n"
                for i in HELP["Official"][plug]:
                    output += i
                output += "\n◈ ʌʏꝛᴀ ꭙ ᴜꜱᴇꝛʙᴏᴛ"
                await ayra.eor(output)
            else:
                try:
                    x = get_string("help_11").format(plug)
                    for d in LIST[plug]:
                        x += HNDLR + d
                        x += "\n"
                    x += "\n◈ ʌʏꝛᴀ ꭙ ᴜꜱᴇꝛʙᴏᴛ"
                    await ayra.eor(x)
                except BaseException:
                    file = None
                    compare_strings = []
                    for file_name in LIST:
                        compare_strings.append(file_name)
                        value = LIST[file_name]
                        for j in value:
                            j = cmd_regex_replace(j)
                            compare_strings.append(j)
                            if j.strip() == plug:
                                file = file_name
                                break
                    if not file:
                        # the enter command/plugin name is not found
                        text = f"`{plug}` is not a valid plugin!"
                        best_match = None
                        for _ in compare_strings:
                            if plug in _ and not _.startswith("_"):
                                best_match = _
                                break
                        if best_match:
                            text += f"\nDid you mean `{best_match}`?"
                        return await ayra.eor(text)
                    output = f"**Command** `{plug}` **found in plugin** - `{file}`\n"
                    if file in HELP["Official"]:
                        for i in HELP["Official"][file]:
                            output += i
                    output += "\n◈ ʌʏꝛᴀ ꭙ ᴜꜱᴇꝛʙᴏᴛ"
                    await ayra.eor(output)
        except BaseException as er:
            LOGS.exception(er)
            await ayra.eor("Error 🤔 occured.")
    else:
        try:
            results = await ayra.client.inline_query(asst.me.username, "ayra")
        except BotMethodInvalidError:
            return await ayra.reply(
                get_string("inline_4").format(
                    len(HELP["Official"]),
                    cmd,
                ),
                buttons=_main_help_menu,
            )
        except BotResponseTimeoutError:
            return await ayra.eor(
                get_string("help_2").format(HNDLR),
            )
        except BotInlineDisabledError:
            return await ayra.eor(get_string("help_3"))
        await results[0].click(chat.id, reply_to=ayra.reply_to_msg_id, hide_via=True)
        await ayra.delete()
