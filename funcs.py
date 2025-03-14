import logging
import random

from telegram import Update, User, Chat, ChatMember
from telegram.ext import CallbackContext
from database import connect_db

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


async def save_group(update: Update, context: CallbackContext):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO groups (chat_id, group_name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                       (chat.id, chat.full_name))
        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"Added group: {chat.id}")


async def fetch_groups():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM groups")
    groups = cursor.fetchall()
    cursor.close()
    conn.close()

    return groups


async def save_user(user: User):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (user_id, username, full_name) VALUES (%s, %s, %s)",
            (user.id, user.username, user.full_name),
        )
        conn.commit()
        logging.info(f"Added user: {user.id}")
    except Exception as e:
        pass


async def save_log(user: User, chat: Chat):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO poo_logs (user_id, chat_id) VALUES (%s, %s)",
        (user.id, chat.id),
    )
    conn.commit()
    logging.info(f"Added log: {user.id} pooped in {chat.id}")


async def is_user_in_group(context: CallbackContext, chat_id: int, user_id: int) -> bool:
    try:
        chat_member = await context.bot.get_chat_member(chat_id, user_id)
        return chat_member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except Exception as e:
        logging.warning(f"Failed to check membership for {user_id} in {chat_id}: {e}")
        return False


async def save_nickname(user: User, nickname: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET nickname=%s WHERE user_id=%s", (nickname, user.id)
    )
    conn.commit()
    cursor.close()
    conn.close()

async def get_nickname(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, nickname FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[1] if result and result[1] else result[0]

async def get_random_message():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * from messages")
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return random.choice(result)[1] if result else "💩 {nickname} رید!"