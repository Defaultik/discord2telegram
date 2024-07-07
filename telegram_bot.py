import asyncio
import discord_bot
from aiogram import Bot, Dispatcher, types
from tokens import TG_TOKEN, TG_CHAT_ID

dp = Dispatcher()
bot = Bot(token=TG_TOKEN)


@dp.message()
async def message_handler(message: types.Message):
    print(message.from_user.username, message.text)
    # await discord_bot.send_message("%s: %s" % (message.from_user.username, message.text))


def escape_text(text):
    escape_characters = ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!')

    for char in escape_characters:
        text = text.replace(char, f"\\{char}")
    
    return text


async def send_message(author, message):
    print("[INFO] %s: %s" % (author, message))
    await bot.send_message(chat_id=TG_CHAT_ID, text="*%s:* %s" % (author, message), parse_mode="Markdown")


async def send_answer(quote_author, quote_text, author, message):
    quote_author, quote_text, author, message = escape_text(quote_author), escape_text(quote_text), escape_text(author), escape_text(message)
    await bot.send_message(chat_id=TG_CHAT_ID, text=f">*{quote_author}:* {quote_text}\n*{author}:* {message}", disable_web_page_preview=True, parse_mode="MarkdownV2")


async def send_attachment(author, file_name, link):
    print("[INFO] %s: %s (attachment)" % (author, file_name))
    await bot.send_message(chat_id=TG_CHAT_ID, text="*%s:* [%s](%s)" % (author, file_name, link), parse_mode="Markdown")


async def main():
    print("[INFO] Bot started to work")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())