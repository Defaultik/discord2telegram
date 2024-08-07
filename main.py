import logging
import asyncio
import telegram_bot
import discord_bot


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.create_task(discord_bot.run())
    loop.create_task(telegram_bot.run())

    loop.run_forever()


if __name__ == "__main__":
    main()