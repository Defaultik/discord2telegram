import discord
import telegram_bot
from tokens import DS_TOKEN, DS_CHAT_ID

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():    
    print('[LOGS] %s started to work' % bot.user.name)


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


async def send_message(message):
    await bot.wait_until_ready()

    channel = bot.get_channel(DS_CHAT_ID)
    if channel:
        await channel.send(message)
    else:
        print(f"ERROR: Channel with ID {DS_CHAT_ID} not found")


def run_discord_bot():
    bot.run(DS_TOKEN)


if __name__ == "__main__":
    run_discord_bot()