import logging
import discord
import telegram_bot
from main import setup_logging
from tokens import DS_TOKEN, DS_CHAT_ID

setup_logging()
logger = logging.getLogger('Discord')

intents = discord.Intents.default()
intents.message_content = True

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


async def send_message(author: str, text: str) -> None:
    channel = bot.get_channel(DS_CHAT_ID)

    logging.info(f"[MESSAGE2DISCORD] {author}: {text}")
    await channel.send(f"**{author}:** {text}")


async def send_answer(quote_author: str, quote_text: str, reply_author: str, reply_text: str) -> None:
    channel = bot.get_channel(DS_CHAT_ID)

    logging.info(f"[MESSAGE2DISCORD] > {quote_author}: {quote_text}\n*{reply_author}: {reply_text}")
    await channel.send(f"> **{quote_author}:** {quote_text}\n**{reply_author}:** {reply_text}")


async def main():
    await bot.start(DS_TOKEN)
    await bot.wait_until_ready()