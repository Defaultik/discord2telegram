import logging
import discord_bot
from aiogram import Bot, Dispatcher, types
from main import setup_logging
from tokens import TG_TOKEN, TG_CHAT_ID

setup_logging()
logger = logging.getLogger("Telegram")

dp = Dispatcher()
bot = Bot(token=TG_TOKEN)


# Telegram message handler
@dp.message()
async def message_handler(message: types.Message):
    if (message.chat.type == "supergroup" or message.chat.type == "group") and message.chat.id == TG_CHAT_ID:
        if message.reply_to_message:
            await discord_bot.send_answer(
                quote_author=message.reply_to_message.from_user.username, 
                quote_text=message.reply_to_message.text, 
                reply_author=message.from_user.username, 
                reply_text=message.text
            )
        elif message.text:
            await discord_bot.send_message(
                author=message.from_user.username, 
                text=message.text
            )
    elif message.chat.type == "private":
        await message.answer(
            text="🇺🇸 This bot is designed only for interactions in groups\n\n🇷🇺 Данный бот предназначен только для взаимодействий в группах"
        )
        

# String escaping to avoid problems in message sending
def escape_text(text: str) -> str:
    escape_characters = ("_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!")

    for char in escape_characters:
        text = text.replace(char, f"\\{char}")
    
    return text


# Send message to Telegram methods
async def send_message(author: str, message: str) -> None:
    logging.info(f"[MESSAGE2TELEGRAM] {author}: {message}")
    await bot.send_message(
        chat_id=TG_CHAT_ID,
        text=f"*{author}:* {message}",
        parse_mode="Markdown"
    )


async def send_message_advanced(text: str) -> None:
    logging.info(f"[MESSAGE2TELEGRAM] {text}")
    await bot.send_message(
        chat_id=TG_CHAT_ID,
        text=f"{text}",
        parse_mode="Markdown"
    )


async def send_answer(quote_author: str, quote_text: str, reply_author: str, reply_text: str) -> None:    
    quote_author, quote_text, reply_author, reply_text = map(escape_text, [quote_author, quote_text, reply_author, reply_text])

    logging.info(f"[MESSAGE2TELEGRAM] > {quote_author}: {quote_text}\n*{reply_author}: {reply_text}")
    await bot.send_message(
        chat_id=TG_CHAT_ID,
        text=f">*{quote_author}:* {quote_text}\n*{reply_author}:* {reply_text}", 
        disable_web_page_preview=True, 
        parse_mode="MarkdownV2"
    )


async def send_attachment(author: str, file_name: str, link: str) -> None:
    logging.info(f"[MESSAGE2TELEGRAM] {author}: {file_name} (attachment)")
    await bot.send_message(
        chat_id=TG_CHAT_ID, 
        text=f"*{author}:* [{file_name}]({link})",
        parse_mode="Markdown"
    )


async def run():
    await dp.start_polling(bot)