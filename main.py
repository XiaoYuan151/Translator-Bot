from os import getenv

from discord import Intents, Message, Client, DMChannel, User, Reaction
from dotenv import load_dotenv

from model import get_translation

load_dotenv()
TOKEN = getenv("TOKEN")
client = Client(intents=Intents.all())


@client.event
async def on_ready():
    global general
    global general_cn
    general = client.get_channel(1397208612815769630)
    general_cn = client.get_channel(1014773752967467080)


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    if isinstance(message.channel, DMChannel):
        return
    if not message.content:
        return
    print(message.content)
    if message.channel == general:
        response = get_translation(message.content, 1)
        print(response)
        if response == "None":
            await general.send("Someone tell XiaoYuan151 there is a problem with my AI.")
            return
        await general_cn.send(f"{message.author.display_name}: {response}")
        return
    if message.channel == general_cn:
        response = get_translation(message.content, 0)
        print(response)
        if response == "None":
            await general.send("Someone tell XiaoYuan151 there is a problem with my AI.")
            return
        await general.send(f"{message.author.display_name}: {response}")
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
