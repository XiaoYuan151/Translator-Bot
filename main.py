import logging
from os import getenv

from discord import Intents, Message, Client, DMChannel, User, Reaction, Activity, ActivityType
from dotenv import load_dotenv

from model import get_translation

load_dotenv()
TOKEN = getenv("TOKEN")
GENERAL = int(getenv("GENERAL"))
GENERAL_CN = int(getenv("GENERAL_CN"))
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
    if message.author == client.user:
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
            await general_cn.send("Someone tell XiaoYuan151 there is a problem with my AI.")
            logging.info(f"({general_cn.name}) {client.user.display_name}: {response}")
            return
        await general_cn.send(f"{message.author.display_name}: {response}")
        logging.info(f"({general_cn.name}) {client.user.display_name}: {response}")
        return
    if message.channel == general_cn:
        response = get_translation(message.content, 0)
        logging.info(f"Translated \"{message.content}\" to \"{response}\"")
        if response == "None":
            await general.send("Someone tell XiaoYuan151 there is a problem with my AI.")
            logging.info(f"({general_cn.name}) {client.user.display_name}: {response}")
            return
        await general.send(f"{message.author.display_name}: {response}")
        logging.info(f"({general_cn.name}) {client.user.display_name}: {response}")
        return
        # \n[Jump to Message](https://discord.com/channels/{message.channel.guild.id}/{message.channel.id}/{message.id})


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
