from geopy.geocoders import Nominatim
from telethon import *
from telethon.tl import *

from Raya.services.events import register
from Raya.services.telethon import tbot as client


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await client(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await client.get_peer_id(user)
        ps = (
            await client(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


GMAPS_LOC = "https://maps.googleapis.com/maps/api/geocode/json"


@register(pattern="^/gps (.*)")
async def _(event):
    if event.fwd_from:
        return
    if event.is_group:
        if not (await is_register_admin(event.input_chat, event.message.sender_id)):
            await event.reply(
                "You are not Admin. So, You can't use this. Try in my inbox"
            )
            return

    args = event.pattern_match.group(1)

    try:
        geolocator = Nominatim(user_agent="SkittBot")
        location = args
        geoloc = geolocator.geocode(location)
        longitude = geoloc.longitude
        latitude = geoloc.latitude
        gm = "https://www.google.com/maps/search/{},{}".format(latitude, longitude)
        await client.send_file(
            event.chat_id,
            file=types.InputMediaGeoPoint(
                types.InputGeoPoint(float(latitude), float(longitude))
            ),
        )
        await event.reply(
            "Open with: [Google Maps]({})".format(gm),
            link_preview=False,
        )
    except Exception as e:
        print(e)
        await event.reply("I can't find that")
