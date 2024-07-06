import asyncio
from aiogram import Bot, Dispatcher
from tokens import TG_TOKEN as TOKEN
from tokens import CHAT_ID


bot = Bot(token=TOKEN)
dp = Dispatcher()

async def send_message(message: str):
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")


async def send_message_advanced(message: str):
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")


async def send_attachment(link: str):
    await bot.send_message(chat_id=CHAT_ID, text=link, parse_mode="Markdown")


"""
@dp.message()
async def send_welcome(message: types.Message):
    if message.text == "/send":
        await send_message_to_group(-1002231109277, "Hello World!")
        await message.answer("Сообщение отправлено в группу.")
"""


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())