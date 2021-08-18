from aiogram.utils.exceptions import BadRequest

from Raya import bot
from Raya.decorator import register

from .utils.connections import chat_connection
from .utils.language import get_strings_dec
from .utils.message import get_arg


@register(cmds="unpin", user_can_pin_messages=True, bot_can_pin_messages=True)
@chat_connection(admin=True)
@get_strings_dec("pins")
async def unpin_message(message, chat, strings):
    # support unpinning all
    if get_arg(message) in {"all"}:
        return await bot.unpin_all_chat_messages(chat["chat_id"])

    try:
        await bot.unpin_chat_message(chat["chat_id"])
    except BadRequest:
        await message.reply(strings["chat_not_modified_unpin"])
        return


@register(cmds="pin", user_can_pin_messages=True, bot_can_pin_messages=True)
@get_strings_dec("pins")
async def pin_message(message, strings):
    if "reply_to_message" not in message:
        await message.reply(strings["no_reply_msg"])
        return
    msg = message.reply_to_message.message_id
    arg = get_arg(message).lower()

    dnd = True
    loud = ["loud", "notify"]
    if arg in loud:
        dnd = False

    try:
        await bot.pin_chat_message(message.chat.id, msg, disable_notification=dnd)
    except BadRequest:
        await message.reply(strings["chat_not_modified_pin"])


__mod_name__ = "Pinning"

__help__ = """
All the pin related commands can be found here; keep your chat up to date on the latest news with a simple pinned message!

<b> Basic Pins </b>
- /pin: silently pins the message replied to - add 'loud' or 'notify' to give notifs to users.
- /unpin: unpins the currently pinned message - add 'all' to unpin all pinned messages.

<b> Other </b>
- /permapin [reply]: Pin a custom message through the bot. This message can contain markdown, buttons, and all the other cool features.
- /unpinall: Unpins all pinned messages.
- /antichannelpin [yes/no/on/off]: Don't let telegram auto-pin linked channels. If no arguments are given, shows current setting.
- /cleanlinked [yes/no/on/off]: Delete messages sent by the linked channel.

Note: When using antichannel pins, make sure to use the /unpin command, instead of doing it manually. Otherwise, the old message will get re-pinned when the channel sends any messages.
"""
