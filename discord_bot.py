import discord
import telegram_bot
from tokens import DS_TOKEN, DS_CHAT_ID

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


# TODO: message-check decorator


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


# Send message to Discord methods
async def send_message(author: str, message: str) -> None:
    print(f"[TELEGRAM2DISCORD] {author}: {message}")

    channel = bot.get_channel(DS_CHAT_ID)
    await channel.send(f"**{author}:** {message}")


async def send_answer(quote_author: str, quote_text: str, reply_author: str, reply_text: str) -> None:    
    print(f"[TELEGRAM2DISCORD] > {quote_author}: {quote_text}\n*{reply_author}: {reply_text}")

    channel = bot.get_channel(DS_CHAT_ID)
    await channel.send(f"> **{quote_author}:** {quote_text}\n**{reply_author}:** {reply_text}")


# Bot startup function
@bot.event
async def on_ready():
    print(f"[INFO] Discord Bot started to work")


async def main():
    await bot.start(DS_TOKEN)
    await bot.wait_until_ready()