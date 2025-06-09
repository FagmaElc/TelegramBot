import os
import random
import asyncio
import datetime
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# --- Flask ---
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Баба Маня живёт 🔮"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)

# --- Telegram логика ---
predictions = [
    "{user1} и {user2} сегодня объединятся ради великой цели.",
    "Между {user1} и {user2} пробежит искра... или метеорит.",
    # ...
]

love_predictions = [
    "{user1} втайне влюблён(а) в {user2} 💘",
    # ...
]

# Гороскопы
horoscope_texts = [
    "День будет удачным для новых начинаний.",
    "Сегодня лучше держаться подальше от конфликтов.",
    "Улыбнись — и день улыбнётся тебе в ответ.",
    "Время для отдыха и восстановления сил.",
    "Хороший момент для общения с близкими.",
    "Прислушайся к интуиции — она подскажет правильный путь.",
    "Небеса благоволят новым знакомствам.",
    "День подходит для творчества и вдохновения.",
    "Лучше не откладывать важные дела.",
    "Удели внимание своему здоровью.",
    "Возможны неожиданные, но приятные события.",
    "Пусть сегодняшний день будет началом чего-то важного.",
]

zodiac_signs = {
    "♈️Овен": "21.03–19.04",
    "♉️Телец": "20.04–20.05",
    "♊️Близнецы": "21.05–20.06",
    "♋️Рак": "21.06–22.07",
    "♌️Лев": "23.07–22.08",
    "♍️Дева": "23.08–22.09",
    "♎️Весы": "23.09–22.10",
    "♏️Скорпион": "23.10–21.11",
    "♐️Стрелец": "22.11–21.12",
    "♑️Козерог": "22.12–19.01",
    "♒️Водолей": "20.01–18.02",
    "♓️Рыбы": "19.02–20.03"
}

chat_members = {}
chat_ids = set()
last_horoscope_usage = {}

async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    chat_ids.add(chat_id)

    if chat_id not in chat_members:
        chat_members[chat_id] = set()
    username = f"@{user.username}" if user.username else user.full_name
    chat_members[chat_id].add(username)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Баба Маня. Напиши /prediction или /lovestory, чтобы узнать судьбу!")

async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, predictions)

async def love_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, love_predictions)

async def send_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE, source):
    chat_id = update.effective_chat.id
    members = list(chat_members.get(chat_id, []))
    if len(members) < 2:
        await update.message.reply_text("Мне нужно хотя бы два человека в чате, чтобы составить предсказание!")
        return
    user1, user2 = random.sample(members, 2)
    text = random.choice(source).format(user1=user1, user2=user2)
    await update.message.reply_text(text)

async def horoscope(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.datetime.now()
    last_used = last_horoscope_usage.get(user_id)

    if last_used and (now - last_used).total_seconds() < 86400:
        await update.message.reply_text("🔒 Гороскоп можно получать только раз в 24 часа.")
        return

    last_horoscope_usage[user_id] = now
    message = "🌟 Гороскоп на сегодня:\n\n"
    for sign, dates in zodiac_signs.items():
        prediction = random.choice(horoscope_texts)
        message += f"♈ {sign} ({dates}): {prediction}\n"
    await update.message.reply_text(message)

async def auto_post(app):
    await asyncio.sleep(10)
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
        await asyncio.sleep(300)

def main():
    Thread(target=run_flask).start()

    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prediction", prediction))
    app.add_handler(CommandHandler("lovestory", love_story))
    app.add_handler(CommandHandler("horoscope", horoscope))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_user))

    async def after_startup(app):
        asyncio.create_task(auto_post(app))

    app.post_init = after_startup

    print("🤖 Баба Маня запущена!")
    app.run_polling()

if __name__ == "__main__":
    main()
