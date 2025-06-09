import os
import random
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# Обычные предсказания
predictions = [
    "{user1} и {user2} сегодня объединятся ради великой цели.",
    "Между {user1} и {user2} пробежит искра... или метеорит.",
    "{user1} узнает страшную тайну о {user2}.",
    "{user1} и {user2} случайно окажутся в одном лифте. Будет неловко.",
    "{user1} должен сегодня угостить {user2} пирожком.",
    "{user1} и {user2} — идеальная команда. Почти.",
    "{user1} сегодня наступит на ногу {user2}. Береги ноги!",
    "{user1} и {user2} не забудут этот день никогда.",
]

# Любовные предсказания
love_predictions = [
    "{user1} втайне влюблён(а) в {user2} 💘",
    "Судьба приготовила {user1} и {user2} романтическое приключение 🌹",
    "{user1} и {user2} сегодня начнут новую историю любви 📖",
    "{user1} скоро получит сердечко от {user2} ❤️",
    "Между {user1} и {user2} вспыхнет искра... держитесь 🔥",
    "{user1} и {user2} — идеальная парочка. Ну, почти 😏",
    "{user1} напишет роман про {user2}, но не признается 🤫",
    "{user1} и {user2} поедут вместе в отпуск... во сне 🏖️",
]

chat_members = {}
chat_ids = set()  # сохраняем ID чатов, где бот активен

# Отслеживаем пользователей
async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user

    chat_ids.add(chat_id)  # добавляем чат в список для автопостинга

    if chat_id not in chat_members:
        chat_members[chat_id] = set()

    username = f"@{user.username}" if user.username else user.full_name
    chat_members[chat_id].add(username)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Баба Маня. Напиши /prediction или /lovestory, чтобы узнать судьбу!")

async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, predictions)

async def love_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, love_predictions)

# Общая функция отправки предсказания
async def send_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE, source):
    chat_id = update.effective_chat.id
    members = list(chat_members.get(chat_id, []))
    if len(members) < 2:
        await update.message.reply_text("Мне нужно хотя бы два человека в чате, чтобы составить предсказание!")
        return
    user1, user2 = random.sample(members, 2)
    text = random.choice(source).format(user1=user1, user2=user2)
    await update.message.reply_text(text)

# Фоновый автопостинг
async def auto_post(app):
    await asyncio.sleep(10)  # подождём немного после запуска
    while True:
        for chat_id in chat_ids:
            members = list(chat_members.get(chat_id, []))
            if len(members) >= 2:
                user1, user2 = random.sample(members, 2)
                text = random.choice(predictions).format(user1=user1, user2=user2)
                try:
                    await app.bot.send_message(chat_id=chat_id, text=f"🔮 Предсказание: {text}")
                except Exception as e:
                    print(f"Ошибка при отправке в чат {chat_id}: {e}")
        await asyncio.sleep(300)  # 5 минут

# Основной запуск
def main():
    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prediction", prediction))
    app.add_handler(CommandHandler("lovestory", love_story))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_user))

    async def after_startup(app):
        asyncio.create_task(auto_post(app))

    app.post_init = after_startup

    print("🤖 Баба Маня запущена!")
    app.run_polling()

if __name__ == "__main__":
    main()
