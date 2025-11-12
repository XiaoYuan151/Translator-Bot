import logging
from os import getenv

from aiohttp import ClientSession
from discord import Intents, Message, Client, DMChannel, User, Reaction, Activity, ActivityType, Webhook
from dotenv import load_dotenv

from model import get_translation

load_dotenv()
TOKEN = getenv("TOKEN")
GENERAL = int(getenv("GENERAL"))
GENERAL_CN = int(getenv("GENERAL_CN"))
GENERAL_URL = getenv("GENERAL_URL")
GENERAL_CN_URL = getenv("GENERAL_CN_URL")
client = Client(intents=Intents.all())
logging.basicConfig(level=logging.INFO, format="%(levelname)s | [%(asctime)s] %(message)s")


@client.event
async def on_ready():
    global general
    global general_cn
    general = client.get_channel(GENERAL)
    general_cn = client.get_channel(GENERAL_CN)
    activity = Activity(name="Just a Translator", type=ActivityType.playing)
    await client.change_presence(activity=activity)


@client.event
async def on_message(message: Message):
    if message.author == client.user or message.author.display_name.find("[Translated]") > -1:
        return
    if isinstance(message.channel, DMChannel):
        return
    if not message.content:
        return
    logging.info(f"({message.channel.name}) {message.author.display_name}: {message.content}")
    if message.channel == general:
        response = get_translation(message.content, 1)
        logging.info(f"Translated \"{message.content}\" to \"{response}\"")
        if response == "None":
            await message.channel.send("Someone tell XiaoYuan151 there is a problem with my AI.")
            return
        async with ClientSession() as session:
            webhook = Webhook.from_url(GENERAL_CN_URL, session=session)
            await webhook.send(content=response, username=f"[Translated] {message.author.display_name}",
                               avatar_url=message.author.avatar.url)
        return
    if message.channel == general_cn:
        response = get_translation(message.content, 0)
        logging.info(f"Translated \"{message.content}\" to \"{response}\"")
        if response == "None":
            await message.channel.send("Someone tell XiaoYuan151 there is a problem with my AI.")
            return
        async with ClientSession() as session:
            webhook = Webhook.from_url(GENERAL_URL, session=session)
            await webhook.send(content=response, username=f"[Translated] {message.author.display_name}",
                               avatar_url=message.author.avatar.url)
        return


@client.event
async def on_reaction_add(reaction: Reaction, user: User):
    if user == client.user:
        return
    if isinstance(reaction.message.channel, DMChannel):
        return
    if not reaction.emoji:
        return


if __name__ == "__main__":
    client.run(TOKEN)
