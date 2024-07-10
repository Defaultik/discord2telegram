import asyncio
import discord
import telegram_bot
from tokens import DS_TOKEN, DS_CHAT_ID

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


# TODO
# message-check decorator


@bot.event
async def on_ready():
    print(f"[DISCORD] Discord Bot started to work")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.id == DS_CHAT_ID:
        if message.type == discord.MessageType.default:
            if message.content:
                await telegram_bot.send_message(message.author.display_name, message.content)
            elif message.attachments:
                await telegram_bot.send_attachment(message.author.display_name, message.attachments[0].filename, message.attachments[0].url)

        elif message.type == discord.MessageType.reply:
            quote_msg = (await message.channel.fetch_message(message.reference.message_id))
            
            if quote_msg.content:
                await telegram_bot.send_answer(quote_msg.author.display_name, quote_msg.content, message.author.display_name, message.content)
            elif quote_msg.attachments:
                await telegram_bot.send_answer(quote_msg.author.display_name, quote_msg.attachments[0].filename, message.author.display_name, message.content)


async def send_message(author: str, message: str) -> None:
    channel = bot.get_channel(DS_CHAT_ID)

    print(f"[TELEGRAM2DISCORD] {author}: {message}")
    await channel.send(f"**{author}:** {message}")


async def send_answer(quote_author: str, quote_text: str, reply_author: str, reply_text: str) -> None:
    channel = bot.get_channel(DS_CHAT_ID)
    
    print(f"[TELEGRAM2DISCORD] > {quote_author}: {quote_text}\n*{reply_author}: {reply_text}")
    await channel.send(f"> **{quote_author}:** {quote_text}\n**{reply_author}:** {reply_text}")


async def main():
    await bot.start(DS_TOKEN)
    await bot.wait_until_ready()


if __name__ == "__main__":
    asyncio.run(main())