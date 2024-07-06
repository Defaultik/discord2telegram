import discord
import telegram_bot
from tokens import DISCORD_TOKEN as TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f'[LOGS] Bot started to work')


@bot.event
async def on_message(message):
    if message.channel.name == "💬┊chat":
        if message.type == discord.MessageType.default:
            if message.attachments:
                print(f"{message.author.display_name}: {message.attachments[0].filename}")
                await telegram_bot.send_attachment(f"*{message.author.display_name}:* [{message.attachments[0].filename}]({message.attachments[0].url})")
            elif message.content:
                print(f"{message.author.display_name}: {message.content}")
                await telegram_bot.send_message(f"*{message.author.display_name}:* {message.content}")

        elif message.type == discord.MessageType.reply:
            replied_message = (await message.channel.fetch_message(message.reference.message_id))
            
            if replied_message.attachments:
                # print(f"{message.author.display_name}: {message.attachments[0].filename}")
                await telegram_bot.send_message_advanced(f"<blockquote><b>{replied_message.author.display_name}:</b> {replied_message.attachments[0].filename}</blockquote><b>{message.author.display_name}:</b> {message.content}")
            elif replied_message.content:
                # print(f"{message.author.display_name}: {message.content}")
                await telegram_bot.send_message_advanced(f"<blockquote><b>{replied_message.author.display_name}:</b> {replied_message.content}</blockquote><b>{message.author.display_name}:</b> {message.content}")


bot.run(TOKEN)