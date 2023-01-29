import os
from pyrogram import Client
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(lineno)d - %(module)s - %(levelname)s - %(message)s'
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

uvloop.install()
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery



if bool(os.environ.get("ENV", False)):
    from sample_config import Config
    from sample_config import LOGGER
else:
    from config import Config
    from config import LOGGER


class Bot(Client):
    def __init__(self):
        super().__init__(
            "bot",
            bot_token=Config.BOT_TOKEN,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            workers=20,
            plugins={
                "root": "plugins"
            },
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.set_parse_mode("html")
        self.LOGGER(__name__).info(
            f"This Bot {me.first_name} Started..!!"
        )

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot Stopped. Bye.!")

app = Bot()
app.run()

