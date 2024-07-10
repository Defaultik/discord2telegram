import asyncio
import discord_bot
from aiogram import Bot, Dispatcher, types
from tokens import TG_TOKEN, TG_CHAT_ID

dp = Dispatcher()
bot = Bot(token=TG_TOKEN)


async def on_startup():
    print("[TELEGRAM] Telegram Bot started to work")


@dp.message()
async def message_handler(message: types.Message):
    if message.chat.id == TG_CHAT_ID:
        if message.reply_to_message:
            await discord_bot.send_answer(message.reply_to_message.from_user.username, message.reply_to_message.text, message.from_user.username, message.text)
        else:
            await discord_bot.send_message(message.from_user.username, message.text)


def escape_text(text):
    escape_characters = ("_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!")

    for char in escape_characters:
        text = text.replace(char, f"\\{char}")
    
    return text


async def send_message(author: str, message: str) -> None:
    print(f"[DISCORD2TELEGRAM] {author}: {message}")
    await bot.send_message(chat_id=TG_CHAT_ID, text=f"*{author}:* {message}", parse_mode="Markdown")


async def send_answer(quote_author: str, quote_text: str, reply_author: str, reply_text: str) -> None:
    print(f"[DISCORD2TELEGRAM] >{quote_author}: {quote_text}\n*{reply_author}: {reply_text}")
    quote_author, quote_text, reply_author, reply_text = escape_text(quote_author), escape_text(quote_text), escape_text(reply_author), escape_text(reply_text)
    await bot.send_message(chat_id=TG_CHAT_ID, text=f">*{quote_author}:* {quote_text}\n*{reply_author}:* {reply_text}", disable_web_page_preview=True, parse_mode="MarkdownV2")


async def send_attachment(author: str, file_name: str, link: str) -> None:
    print(f"[DISCORD2TELEGRAM] {author}: {file_name} (attachment)")
    await bot.send_message(chat_id=TG_CHAT_ID, text=f"*{author}:* [{file_name}]({link})", parse_mode="Markdown")


async def main():
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())