import random
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

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

# Сохраняем участников чата
chat_members = {}

# Отслеживаем пользователей
async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id not in chat_members:
        chat_members[chat_id] = set()

    username = f"@{user.username}" if user.username else user.full_name
    chat_members[chat_id].add(username)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Баба Маня. Напиши /prediction или /lovestory, чтобы узнать судьбу!")

# Команда /prediction
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_duo_prediction(update, context, predictions)

# Команда /lovestory
async def love_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_duo_prediction(update, context, love_predictions)

# Общая функция выбора двух участников и отправки предсказания
async def send_duo_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE, prediction_list):
    chat_id = update.effective_chat.id
    members = list(chat_members.get(chat_id, []))

    if len(members) < 2:
        await update.message.reply_text("Мне нужно хотя бы два человека в чате, чтобы составить парочку!")
        return

    user1, user2 = random.sample(members, 2)
    prediction = random.choice(prediction_list).format(user1=user1, user2=user2)
    await update.message.reply_text(prediction)

# Основной запуск бота
def main():
    
    TOKEN = os.environ["BOT_TOKEN"] # Замени токен на свой
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prediction", predict))
    app.add_handler(CommandHandler("lovestory", love_story))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_user))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
