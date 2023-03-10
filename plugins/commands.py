import os
import asyncio
from presets import Presets
import logging
logger = logging.getLogger(__name__)

from pyrogram import Client, filters
from bot import bot
from translation import Translation
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from library.support import users_info
from library.sql import add_user, query_msg


if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config

################################################################################################################################################################################################################################################
# Start Command

START = "Translation.START"

TELETIPS_MAIN_MENU_BUTTONS = [
            [
                InlineKeyboardButton('👨‍💻 Creator', url='https://t.me/Star_Movies_Karthik')
            ],
            [
                InlineKeyboardButton('😎 About', callback_data="TUTORIAL_CALLBACK"),
                InlineKeyboardButton('👥 Support', callback_data="GROUP_CALLBACK"),
                InlineKeyboardButton('😁 Help', callback_data="HELP_CALLBACK")
            ],
            [
                InlineKeyboardButton('📣 Update Channel', url='https://t.me/Star_Moviess_Tamil')
            ]
        ]

@Client.on_message(filters.command('start') & filters.private)
async def start(client, message):
    text = Translation.START
    reply_markup = InlineKeyboardMarkup(TELETIPS_MAIN_MENU_BUTTONS)
    await message.reply(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

@Client.on_callback_query()
async def callback_query(client: Client, query: CallbackQuery):
    if query.data=="HELP_CALLBACK":
        TELETIPS_HELP_BUTTONS = [
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK")
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_HELP_BUTTONS)
        try:
            await query.edit_message_text(
                Translation.HELP,
                disable_web_page_preview=True,
                quote=True,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="GROUP_CALLBACK":
        TELETIPS_GROUP_BUTTONS = [
            [
                InlineKeyboardButton("Star Movies Feedback", url="https://t.me/Star_Movies_Feedback_Bot")
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_GROUP_BUTTONS)
        try:
            await query.edit_message_text(
                Translation.SUPPORT,
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass    

    elif query.data=="TUTORIAL_CALLBACK":
        TELETIPS_TUTORIAL_BUTTONS = [
            [
                InlineKeyboardButton("🤵 Admin", url="https://t.me/Star_Movies_Karthik")
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_TUTORIAL_BUTTONS)
        try:
            await query.edit_message_text(
                Translation.ABOUT,
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass      
          
    elif query.data=="START_CALLBACK":
        TELETIPS_START_BUTTONS = [
            [
                InlineKeyboardButton('👨‍💻 Creator', url='https://t.me/Star_Movies_Karthik')
            ],
            [
                InlineKeyboardButton('😎 About', callback_data="TUTORIAL_CALLBACK"),
                InlineKeyboardButton('👥 Support', callback_data="GROUP_CALLBACK"),
                InlineKeyboardButton('😁 Help', callback_data="HELP_CALLBACK")
            ],
            [
                InlineKeyboardButton('📣 Update Channel', url='https://t.me/Star_Moviess_Tamil')
            ]
        ]

        reply_markup = InlineKeyboardMarkup(TELETIPS_START_BUTTONS)
        try:
            await query.edit_message_text(
                Translation.START,
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass    


################################################################################################################################################################################################################################################
# Help Command

@Client.on_message(filters.command("help") & filters.private & filters.incoming)
async def help(client, message):
    await message.reply(
        text=Translation.HELP,
        disable_web_page_preview=True,
        quote=True
    )

################################################################################################################################################################################################################################################
# About Command

@Client.on_message(filters.command("about") & filters.private & filters.incoming)
async def about(client, message):
    await message.reply(
        text=Translation.ABOUT,
        disable_web_page_preview=True,
        quote=True
    )

################################################################################################################################################################################################################################################
# View Subscribers

@Client.on_message(filters.private & filters.command('stats'))
async def stats_count(bot, m: Message):
    id = m.from_user.id
    if id not in Config.AUTH_USERS:
        return
    msg = await m.reply_text(Presets.WAIT_MSG)
    messages = await users_info(bot)
    active = messages[0]
    blocked = messages[1]

    await msg.edit(Presets.USERS_LIST.format(active, blocked))


################################################################################################################################################################################################################################################
#Send messages to Subscribers

@Client.on_message(filters.private & filters.command('broadcast'))
async def broadcast_text(bot, m: Message):
    id = m.from_user.id
    if id not in Config.AUTH_USERS:
        return
    if (" " not in m.text) and ("broadcast" in m.text) and (m.reply_to_message is not None):
        query = await query_msg()
        for row in query:
            chat_id = int(row[0])
            try:
                await bot.copy_message(
                    chat_id=chat_id,
                    from_chat_id=m.chat.id,
                    message_id=m.reply_to_message.message_id,
                    caption=m.reply_to_message.caption,
                    reply_markup=m.reply_to_message.reply_markup
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception:
                pass
    else:
        msg = await m.reply_text(Presets.REPLY_ERROR, m.message_id)
        await asyncio.sleep(8)

################################################################################################################################################################################################################################################

               # Star Movies Tamil

################################################################################################################################################################################################################################################
#Alien Covenant (2017)

@Client.on_message(filters.command("alien_covenant") & filters.private & filters.incoming)
async def alien_covenant(client, message):
    await message.reply_photo(
        caption = Translation.ALIEN_COVENANT.format(
                mention = message.from_user.mention
            ),
        photo="https://telegra.ph/file/206f9013802376b39ad03.jpg",
        quote=True
    )

################################################################################################################################################################################################################################################
