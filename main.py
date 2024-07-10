import asyncio
import telegram_bot
import discord_bot

loop = asyncio.get_event_loop()

loop.create_task(telegram_bot.main())
loop.create_task(discord_bot.main())

loop.run_forever()