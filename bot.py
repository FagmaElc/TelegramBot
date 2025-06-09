import os
import random
import asyncio
from flask import Flask
from threading import Thread

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# --- Flask для Render Health Check ---
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Баба Маня живёт 🔮"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)

# --- Telegram логика ---

# Обычные предсказания
predictions_today = [
    "{user1} и {user2} сегодня объединятся ради великой цели.",
    "Между {user1} и {user2} пробежит искра... или метеорит.",
    "{user1} узнает страшную тайну о {user2}.",
    "{user1} и {user2} случайно окажутся в одном лифте. Будет неловко.",
    "{user1} должен сегодня угостить {user2} пирожком.",
    "{user1} и {user2} — идеальная команда. Почти.",
    "{user1} сегодня наступит на ногу {user2}. Береги ноги!",
    "{user1} и {user2} не забудут этот день никогда.",
]

# Завтрашние предсказания
predictions_tomorrow = [
    "{user1} и {user2} завтра попадут в странную ситуацию.",
    "Завтра {user1} подумает о {user2} слишком часто.",
    "У {user1} и {user2} завтра появится общий враг.",
    "{user1} и {user2} устроят завтрашний флешмоб.",
    "{user1} нечаянно позвонит {user2} завтра ночью.",
    "{user1} и {user2} неожиданно прославятся завтра.",
    "{user1} завтра случайно откроет секрет {user2}.",
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

# Откровенные любовные предсказания
spicy_love_predictions = [
    "{user1} и {user2} — горячая смесь страсти и интриг 🔥🔥",
    "{user1} и {user2} устроят свидание, которое никто не забудет 💋",
    "{user1} посмотрит на {user2} иначе... и понравится 😉",
    "{user1} напишет {user2} сообщение, которое вызовет бурю эмоций 😘",
    "{user1} и {user2}... ну вы поняли 😏",
]

chat_members = {}
chat_ids = set()

async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user

    chat_ids.add(chat_id)

    if chat_id not in chat_members:
        chat_members[chat_id] = set()

    username = f"@{user.username}" if user.username else user.full_name
    chat_members[chat_id].add(username)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Баба Маня. Вот что я умею:\n"
        "/prediction — обычное предсказание\n"
        "/lovestory — романтическое предсказание\n"
        "/predictiontoday — предсказание на сегодня\n"
        "/predictiontomorrow — предсказание на завтра\n"
        "/loveball — откровенное любовное предсказание"
    )

async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, predictions_today)

async def prediction_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, predictions_today)

async def prediction_tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, predictions_tomorrow)

async def love_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, love_predictions)

async def love_ball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, spicy_love_predictions)

async def send_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE, source):
    chat_id = update.effective_chat.id
    members = list(chat_members.get(chat_id, []))
    if len(members) < 2:
        await update.message.reply_text("Мне нужно хотя бы два человека в чате, чтобы составить предсказание!")
        return
    user1, user2 = random.sample(members, 2)
    text = random.choice(source).format(user1=user1, user2=user2)
    await update.message.reply_text(text)

async def auto_post(app):
    await asyncio.sleep(10)
    while True:
        for chat_id in chat_ids:
            members = list(chat_members.get(chat_id, []))
            if len(members) >= 2:
                user1, user2 = random.sample(members, 2)
                text = random.choice(predictions_today).format(user1=user1, user2=user2)
                try:
                    await app.bot.send_message(chat_id=chat_id, text=f"🔮 Предсказание: {text}")
                except Exception as e:
                    print(f"Ошибка при отправке в чат {chat_id}: {e}")
        await asyncio.sleep(300)

def main():
    Thread(target=run_flask).start()  # Запускаем Flask в отдельном потоке

    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prediction", prediction))
    app.add_handler(CommandHandler("predictiontoday", prediction_today))
    app.add_handler(CommandHandler("predictiontomorrow", prediction_tomorrow))
    app.add_handler(CommandHandler("lovestory", love_story))
    app.add_handler(CommandHandler("loveball", love_ball))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_user))

    async def after_startup(app):
        asyncio.create_task(auto_post(app))

    app.post_init = after_startup

    print("🤖 Баба Маня запущена!")
    app.run_polling()

if __name__ == "__main__":
    main()
