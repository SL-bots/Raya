import re
from random import choice

import requests
from bs4 import BeautifulSoup

from Raya.decorator import register

from .utils.disable import disableable_dec
from .utils.message import get_arg


@register(cmds="direct")
@disableable_dec("direct")
async def direct_link_generator(message):
    text = get_arg(message)

    if not text:
        m = "Usage: <code>/direct (url)</code>"
        await message.reply(m)
        return

    if text:
        links = re.findall(r"\bhttps?://.*\.\S+", text)
    else:
        return

    reply = []
    if not links:
        await message.reply("No links found!")
        return

    for link in links:
        if "sourceforge.net" in link:
            reply.append(sourceforge(link))
        else:
            reply.append(
                re.findall(r"\bhttps?://(.*?[^/]+)", link)[0] + " is not supported"
            )

    await message.reply("\n".join(reply))


def sourceforge(url: str) -> str:
    try:
        link = re.findall(r"\bhttps?://.*sourceforge\.net\S+", url)[0]
    except IndexError:
        reply = "No SourceForge links found\n"
        return reply

    file_path = re.findall(r"/files(.*)/download", link)
    if not file_path:
        file_path = re.findall(r"/files(.*)", link)
    file_path = file_path[0]
    reply = f"Mirrors for <code>{file_path.split('/')[-1]}</code>\n"
    project = re.findall(r"projects?/(.*?)/files", link)[0]
    mirrors = (
        f"https://sourceforge.net/settings/mirror_choices?"
        f"projectname={project}&filename={file_path}"
    )
    page = BeautifulSoup(requests.get(mirrors).content, "lxml")
    info = page.find("ul", {"id": "mirrorList"}).findAll("li")

    for mirror in info[1:]:
        name = re.findall(r"\((.*)\)", mirror.text.strip())[0]
        dl_url = (
            f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
        )
        reply += f'<a href="{dl_url}">{name}</a> '
    return reply


def useragent():
    useragents = BeautifulSoup(
        requests.get(
            "https://developers.whatismybrowser.com/"
            "useragents/explore/operating_system_name/android/"
        ).content,
        "lxml",
    ).findAll("td", {"class": "useragent"})
    user_agent = choice(useragents)
    return user_agent.text
