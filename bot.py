import logging
import random

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackContext, ChatMemberHandler

from database import init_db
from funcs import *
from config import BOT_PARAMS

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


async def poo(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    chat = update.effective_chat

    await save_user(user)
    await save_log(user, chat)

    groups = await fetch_groups()
    nickname = await get_nickname(user.id)

    # message = f"💩 {nickname} رید!"
    random_message = await get_random_message()
    message = random_message.format(nickname=nickname)

    for (group_id,) in groups:
        if await is_user_in_group(context, group_id, user.id):
            try:
                await context.bot.send_message(chat_id=group_id, text=message)
            except Exception as e:
                logging.warning(f"Failed to send message to {group_id}: {e}")


async def set_nickname(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if not context.args:
        await update.message.reply_text("❌ یه اسم مستعار انتخاب کن. مثال: /setnickname مرد عنی")
        return

    nickname = " ".join(context.args)
    await save_nickname(user, nickname)
    await update.message.reply_text(f"✅ نام مستعارت به <b>{nickname}</b> تغییر کرد!", parse_mode=ParseMode.HTML)

def main():
    # init_db()

    app = Application.builder().token(BOT_PARAMS["token"]).build()

    app.add_handler(CommandHandler("poo", poo))
    app.add_handler(CommandHandler("setnickname", set_nickname))
    app.add_handler(ChatMemberHandler(save_group, ChatMemberHandler.MY_CHAT_MEMBER))

    logging.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
