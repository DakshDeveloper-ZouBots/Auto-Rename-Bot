import logging, sys
from pyrogram import Client
from aiohttp import web
from config import API_ID, API_HASH, BOT_TOKEN, PORT
from route import web_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("wzgram_bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("WzgramBot")

class WzgramBot(Client):
    def __init__(self):
        super().__init__("WzgramAutoRename", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins=dict(root="plugins"))

    async def start(self):
        await super().start()
        me = await self.get_me()
        logger.info(f"@{me.username} powered by Wzgram started successfully!")
        app = await web_server()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        logger.info(f"Web server running on port {PORT}")

    async def stop(self, *args):
        await super().stop()
        logger.info("Wzgram Bot stopped.")

if __name__ == "__main__":
    WzgramBot().run()
