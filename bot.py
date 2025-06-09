import os
import random
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# Предсказания
predictions = [
    "{user1} и {user2} сегодня объединятся ради великой цели.",
    "{user1} должен сегодня угостить {user2} пирожком.",
    "{user1} узнает страшную тайну о {user2}.",
    "Между {user1} и {user2} пробежит искра... или метеорит.",
]

love_predictions = [
    "{user1} втайне влюблён(а) в {user2} 💘",
    "Судьба приготовила {user1} и {user2} романтическое приключение 🌹",
    "{user1} и {user2} начнут новую историю любви 📖",
    "{user1} получит сердечко от {user2} ❤️",
]

chat_members = {}
target_chat_id = None

# Отслеживание пользователей
async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global target_chat_id
    chat_id = update.effective_chat.id
    user = update.effective_user

    if target_chat_id is None:
        target_chat_id = chat_id
        print(f"📌 Сохранён chat_id: {target_chat_id}")

    if chat_id not in chat_members:
        chat_members[chat_id] = set()

    username = f"@{user.username}" if user.username else user.full_name
    chat_members[chat_id].add(username)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Баба Маня. Напиши /prediction или /lovestory!")

async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update.effective_chat.id, context, predictions)

async def love_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update.effective_chat.id, context, love_predictions)

# Общая функция предсказания
async def send_prediction(chat_id, context: ContextTypes.DEFAULT_TYPE, pred_list):
    members = list(chat_members.get(chat_id, []))
    if len(members) < 2:
        await context.bot.send_message(chat_id, "Мне нужно хотя бы два человека в чате!")
        return
    user1, user2 = random.sample(members, 2)
    text = random.choice(pred_list).format(user1=user1, user2=user2)
    await context.bot.send_message(chat_id, text)

# Автопостинг каждые 5 минут (обычные предсказания)
async def auto_post(app):
    await app.bot.wait_until_ready()
    while True:
        if target_chat_id and target_chat_id in chat_members and len(chat_members[target_chat_id]) >= 2:
            user1, user2 = random.sample(list(chat_members[target_chat_id]), 2)
            text = random.choice(predictions).format(user1=user1, user2=user2)
        else:
            text = "Жду, когда в чате будет минимум два пользователя 🙃"

        try:
            if target_chat_id:
                await app.bot.send_message(chat_id=target_chat_id, text=text)
        except Exception as e:
            print(f"Ошибка автопоста: {e}")

        await asyncio.sleep(300)  # 5 минут

# Запуск
def main():
    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prediction", prediction))
    app.add_handler(CommandHandler("lovestory", love_story))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_user))

    app.post_init = lambda _: asyncio.create_task(auto_post(app))

    print("🤖 Баба Маня запущена!")
    app.run_polling()

if __name__ == "__main__":
    main()
