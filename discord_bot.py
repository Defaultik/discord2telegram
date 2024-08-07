import logging
import discord
import telegram_bot
from main import setup_logging
from tokens import DS_TOKEN, DS_CHAT_ID

setup_logging()
logger = logging.getLogger('Discord')

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = discord.Client(intents=intents)


# Discord message handler
@bot.event
async def on_message(message):
    if message.channel.id == DS_CHAT_ID and message.author != bot.user:
        if message.type == discord.MessageType.default:
            if message.content:
                await telegram_bot.send_message(
                    author=message.author.display_name,
                    message=message.content
                )
            elif message.attachments:
                await telegram_bot.send_attachment(
                    author=message.author.display_name, 
                    file_name=message.attachments[0].filename, 
                    link=message.attachments[0].url
                )

        elif message.type == discord.MessageType.reply:
            quote_msg = (await message.channel.fetch_message(message.reference.message_id))
            
            if quote_msg.content:
                await telegram_bot.send_answer(
                    quote_author=quote_msg.author.display_name,
                    quote_text=quote_msg.content, 
                    reply_author=message.author.display_name, 
                    reply_text=message.content
                )
            elif quote_msg.attachments:
                await telegram_bot.send_answer(
                    quote_author=quote_msg.author.display_name, 
                    quote_text=quote_msg.attachments[0].filename, 
                    reply_author=message.author.display_name, 
                    reply_text=message.content
                )


@bot.event
async def on_voice_state_update(member, before, after) -> None:
    for channel in (before.channel, after.channel):
        if channel:
            channel.name = channel.name.replace("┊", "")

    if not before.channel and after.channel:
        print(f"{member} подключился к каналу {after.channel.name}")
        await telegram_bot.send_message_advanced(
            text=f"*{member}* подключился к голосовому каналу *__{after.channel.name}__*"
        )
    elif before.channel and not after.channel:
        print(f"{member} отключился от канала {before.channel.name}")
        await telegram_bot.send_message_advanced(
            text=f"*{member}* отключился от голосового канала *__{before.channel.name}__*"
        )
    elif before.channel and after.channel:
        print(f'{member} переместился из канала {before.channel.name} в {after.channel.name}')
        await telegram_bot.send_message_advanced(
            text=f"*{member}* переместился из канала *__{before.channel.name}__* в *__{after.channel.name}__*"
        )


async def send_message(author: str, text: str) -> None:
    channel = bot.get_channel(DS_CHAT_ID)

    logging.info(f"[MESSAGE2DISCORD] {author}: {text}")
    await channel.send(f"**{author}:** {text}")


async def send_answer(quote_author: str, quote_text: str, reply_author: str, reply_text: str) -> None:
    channel = bot.get_channel(DS_CHAT_ID)

    logging.info(f"[MESSAGE2DISCORD] > {quote_author}: {quote_text}\n*{reply_author}: {reply_text}")
    await channel.send(f"> **{quote_author}:** {quote_text}\n**{reply_author}:** {reply_text}")


async def run():
    await bot.start(DS_TOKEN)
    await bot.wait_until_ready()