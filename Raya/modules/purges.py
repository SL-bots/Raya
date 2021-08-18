import asyncio

from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError

from Raya import bot
from Raya.decorator import register
from Raya.services.telethon import tbot

from .utils.language import get_strings_dec
from .utils.notes import BUTTONS


@register(cmds="del", bot_can_delete_messages=True, user_can_delete_messages=True)
@get_strings_dec("msg_deleting")
async def del_message(message, strings):
    if not message.reply_to_message:
        await message.reply(strings["reply_to_msg"])
        return
    msgs = [message.message_id, message.reply_to_message.message_id]
    await tbot.delete_messages(message.chat.id, msgs)


@register(
    cmds="purge",
    no_args=True,
    bot_can_delete_messages=True,
    user_can_delete_messages=True,
)
@get_strings_dec("msg_deleting")
async def fast_purge(message, strings):
    if not message.reply_to_message:
        await message.reply(strings["reply_to_msg"])
        return
    msg_id = message.reply_to_message.message_id
    delete_to = message.message_id

    chat_id = message.chat.id
    msgs = []
    for m_id in range(int(delete_to), msg_id - 1, -1):
        msgs.append(m_id)
        if len(msgs) == 100:
            await tbot.delete_messages(chat_id, msgs)
            msgs = []

    try:
        await tbot.delete_messages(chat_id, msgs)
    except MessageDeleteForbiddenError:
        await message.reply(strings["purge_error"])
        return

    msg = await bot.send_message(chat_id, strings["fast_purge_done"])
    await asyncio.sleep(5)
    await msg.delete()


BUTTONS.update({"delmsg": "btn_deletemsg_cb"})


@register(regexp=r"btn_deletemsg:(\w+)", f="cb", allow_kwargs=True)
async def delmsg_btn(event, regexp=None, **kwargs):
    await event.message.delete()


__mod_name__ = "Purges"

__help__ = """
Need to delete lots of messages? That's what purges are for!

<b>Available commands:</b>
- /purge: Deletes all messages from the message you replied to, to the current message.
- /del: Deletes the message you replied to and your "<code>/del</code>" command message.
"""
