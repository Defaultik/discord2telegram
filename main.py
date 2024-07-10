import asyncio
import telegram_bot
import discord_bot


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.create_task(discord_bot.main())
    loop.create_task(telegram_bot.main())

    loop.run_forever()


if __name__ == "__main__":
    main()