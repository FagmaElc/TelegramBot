import os

import random
import asyncio
import datetime
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler

ADD_MEME = range(1)
# --- Flask ---
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Баба Маня живёт 🔮"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)

def load_list_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"⚠️ Файл не найден: {filename}")
        return []


predictions = load_list_from_file("predictions.txt")
predictionsToday = load_list_from_file("predictions_today.txt")
predictionsTomorrow = load_list_from_file("predictions_tomorrow.txt")
recom = load_list_from_file("recom.txt")
love_predictions = load_list_from_file("love_predictions.txt")
love = load_list_from_file("love.txt")
Ball = load_list_from_file("Ball.txt")
autopred = load_list_from_file("autopred.txt")
meme_urls = load_list_from_file("meme_urls.txt")
vibe = load_list_from_file("vibe.txt")
caption = load_list_from_file("caption.txt")

character_traits = load_list_from_file("character_traits.txt")
love_traits = load_list_from_file("love_traits.txt")
career_traits = load_list_from_file("career_traits.txt")
Work = load_list_from_file("Work.txt")
future_predictions = load_list_from_file("future.txt")
attractiveness = load_list_from_file("attractiveness.txt")
tyan_images = load_list_from_file("tyan_images.txt")


async def add_meme_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 Пришли изображение, чтобы добавить мем.")
    return ADD_MEME

async def handle_meme_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]  # самое большое качество
    file = await photo.get_file()
    file_url = file.file_path

    with open("meme_urls.txt", "a", encoding="utf-8") as f:
        f.write(file_url + "\n")

    await update.message.reply_text("✅ Мем добавлен в коллекцию!")
    return ConversationHandler.END

async def cancel_add_meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Отмена добавления.")
    return ConversationHandler.END


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
    "Пусть сегодняшний день будет началом чего-то важного.",    "Сегодня звезды советуют вам ничего не делать. И желательно с удовольствием.",
    "Вы обретёте внутренний покой... если отключите Wi-Fi.",
    "День подходит для новых начинаний. Например, пересмотреть все сезоны своего любимого сериала.",
    "Остерегайтесь людей в носках с сандалиями — они знают, что делают.",
    "Ваш кофе сегодня будет сильнее вашей мотивации.",
    "Наконец-то звезды расположены к вам... на расстоянии 500 световых лет.",
    "День хорош для романтики. Особенно с пиццей.",
    "Ваша харизма сегодня достигнет пика. Осталось убедить в этом окружающих.",
    "Если вы сегодня опоздаете — просто скажите, что планеты не сошлись.",
    "Ваша удача рядом… но она, как и вы, не спешит вставать с кровати.",
    "Ваш начальник сегодня на редкость добрый. Возможно, его похитили инопланетяне.",
    "Остерегайтесь зеркал — они сегодня слишком честны.",
    "Сегодня ваше настроение зависит от количества съеденного шоколада.",
    "Вам улыбнётся удача. И сразу потребует чаевые.",
    "Не верьте предсказаниям. Кроме этого.",
    "Вы сегодня такой привлекательный, что даже зеркало подмигнуло вам.",
    "Остерегайтесь тех, кто слишком счастлив по утрам.",
    "Сегодня у вас получится всё. Особенно откладывать дела на завтра.",
    "Луна в Тельце, а вы в одеяле. Всё логично.",
    "Ваш внутренний голос советует поспать ещё час. Прислушайтесь к мудрому человеку.",
    "Судьба даст вам шанс. Но он будет замаскирован под странного человека с булкой.",
    "Ваша душа просит приключений. Ваш холодильник — борща.",
    "Звезды говорят, что вы талантливы. Осталось понять, в чём именно.",
    "Если жизнь дала лимон — добавьте текилы.",
    "Не покупайте сегодня ничего с пометкой 'скидка 90%' — это ловушка.",
    "Сегодня вы будете неотразимы. Особенно, если вас никто не видит.",
    "Будьте проще. Например, поспите на работе.",
    "Луна в Скорпионе, и она тоже не в настроении. Вы не одиноки.",
    "Кто-то вас сегодня удивит. Надеемся, не налоговая.",
    "Если вам кажется, что вы на дне — посмотрите вниз. Там Wi-Fi ловит лучше.",
    "Будьте осторожны в словах. Особенно, если говорите с будильником.",
    "Ваше второе имя сегодня — 'не сейчас'.",
    "Не стесняйтесь своих желаний. Даже если это съесть весь торт в одиночку.",
    "День хорош для прогулки. В тапках. По дому.",
    "Сегодня вы наконец поймёте смысл жизни. Или хотя бы зачем нужна кнопка 'повторить будильник'.",
    "Вселенная шепчет вам: «Поспи ещё чуть-чуть...»",
    "У вас сегодня удачный день! Особенно для того, чтобы притвориться занятым.",
    "Судьба приготовила вам подарок. Осталось её найти и заставить отдать.",
    "Если ничего не хочется — не сопротивляйтесь. Звезды понимают.",
    "Не спорьте с Весами сегодня. Особенно если вы Весы.",
    "Ваше терпение будет испытано. Вероятно, автокорректором.",
    "Если день не задался — просто добавьте котика в ленту.",
    "Сегодня вы как Wi-Fi: всем нужен, но не всегда работаете.",
    "Пусть ваше внутреннее солнце светит. Или хотя бы не ворчит.",
    "Ваша сила — в лени. Никто не сможет вас переутомить!",
    "Сегодня не ваш день. Но никто об этом не узнает, если вы не выйдете из дома.",
    "Вы настолько обаятельны, что даже холодильник улыбается, когда вы его открываете.",
    "День принесёт много открытий. Например, где вы опять потеряли ключи.",
    "Планы на вечер: 1) Ничего. 2) И это отлично работает.",
    "Сегодня всё получится. Особенно, если этого не делать.",
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

truth_questions = [
    "💭 Ты когда-нибудь притворялся, что болен, чтобы избежать чего-то?",
    "😅 Какая самая неловкая вещь с тобой случалась в общественном месте?",
    "📖 Какая ложь из детства до сих пор никто не знает?",
    "🧛 Веришь ли ты в потустороннее?",
    "💔 Когда ты в последний раз кого-то ревновал?",
    "🕵️‍♀️ За кем ты когда-либо тайно следил в соцсетях?",
    "🎁 Какой подарок ты получал и ненавидел, но сказал, что нравится?",
    "🐍 Расскажи о моменте, когда ты предал друга.",
    "💸 Врал ли ты когда-либо про деньги, чтобы не делиться?",
    "📅 Какая дата вызывает у тебя плохие воспоминания?",
    "🔥 Кто тебе нравился, но ты скрывал это?",
    "📵 Бывает ли, что ты игнорируешь сообщения специально?",
    "🎓 Есть ли у тебя поддельный диплом или сертификат?",
    "🤐 Что ты никогда не рассказываешь даже близким?",
    "🧼 Ты когда-нибудь притворялся, что мылся, но нет?",
    "👻 Была ли в твоей жизни паранормальная ситуация?",
    "🎭 Притворялся ли ты в отношениях кем-то другим?",
    "🕳️ Какой момент из своей жизни ты бы вычеркнул?",
    "📲 Просматриваешь ли ты чужие переписки, если есть возможность?",
    "🧙‍♂️ В какой момент ты чувствовал(а) себя полностью беспомощным?",
    "🎮 Обманывал ли ты когда-либо в игре, притворяясь честным?",
    "💌 Отправлял(а) ли ты анонимные признания?",
    "👁️ Что бы ты изменил(а) в себе, если бы никто не узнал?",
    "😬 Самый стыдный сон, который тебе снился?",
    "📸 Был(а) ли у тебя фейковый аккаунт в соцсетях?",
    "🫣 Какой у тебя есть фетиш, о котором никто не знает?",
    "😈 Когда ты в последний раз делал(а) что-то плохое назло?",
    "🛑 Бывали ли у тебя фантазии о ком-то из этого чата?",
    "🎤 Врал(а) ли ты кому-то, что любишь его, но это было не так?",
    "😇 Есть ли у тебя секрет, за который тебе до сих пор стыдно?",
    "📵 Блокировал(а) кого-то несправедливо?",
    "🕯️ Ты когда-нибудь использовал(а) магию или гадание всерьёз?",
    "🏴‍☠️ Что ты украл(а), даже если это было мелкое?",
    "👀 Кто тебе не нравится в этом чате?",
    "💤 Что бы ты сделал(а), если бы мог быть невидимкой на день?",
    "🤖 Хотел(а) бы ты стереть кого-то из своей жизни?",
    "💣 Расскажи о тайне, которую ты держал(а) годами.",
    "🥴 Плакал(а) ли ты из-за сериала или фильма?",
    "🧛 Расскажи о моменте, когда ты манипулировал(а) кем-то.",
    "😶 Ты когда-либо был(а) причиной чужого конфликта?",
    "📉 Что самое грустное ты слышал(а) о себе?",
    "💀 Когда ты чувствовал(а) себя абсолютно одиноким?",
    "🧬 Какой факт из прошлого ты бы хотел(а) изменить?",
    "📩 Отправлял(а) ли ты фейковое признание или шутку от чужого имени?",
    "🧂 Расскажи о моменте, когда ты сплетничал(а) за чьей-то спиной.",
    "🧠 Что ты бы никогда не признал(а) родителям?",
    "🛌 Был(а) ли у тебя кринжовый роман?",
    "😱 Что самое безумное ты хотел(а) бы попробовать, но боишься?",
    "🎒 Притворялся ли ты добрым другом ради выгоды?",
    "🧃 Что тебе нравится, но ты стесняешься признать?"
]
truth_questions += [
     "😱 Что самое безумное ты хотел(а) бы попробовать, но боишься?",
    "🎒 Притворялся ли ты добрым другом ради выгоды?",
    "🧃 Что тебе нравится, но ты стесняешься признать?"
]
dare_challenges = [
    "🎤 Запиши голосовое, где ты говоришь как ведьма!",
    "📸 Отправь последнее фото из галереи, не объясняя его.",
    "👀 Признайся в чате в любви к первому человеку, кто ответит.",
]
dare_challenges += [
    "🎤 Запиши голосовое, где ты говоришь как ведьма!",
    "📸 Отправь последнее фото из галереи, не объясняя его.",
    "👀 Признайся в чате в любви к первому человеку, кто ответит.",
    "🎲 Напиши 'Я провёл обряд с Бабой Маней' в любой чат.",
    "🕺 Сними короткое видео, как ты танцуешь магический танец.",
    "📞 Позвони кому-нибудь и скажи, что ты ведьма.",
    "😈 Напиши кому-нибудь: 'Ты в опасности. Не спрашивай почему.'",
    "🧙 Измени имя на 'Посланник Маны' на 10 минут.",
    "📨 Отправь 3 случайным людям '🌕 Наступает магия'.",
    "🧼 Напиши в чат: 'Я клянусь больше не скрывать свою силу'.",
    "💌 Признайся в симпатии случайному человеку.",
    "💀 Отправь самый кринжовый стикер, что у тебя есть.",
    "🤳 Сделай селфи с самым странным выражением лица.",
    "🧛 Придумай и озвучь заклинание прямо сейчас!",
    "🪄 Нарисуй магический символ и скинь его в чат.",
    "📦 Расскажи свой последний странный сон как пророчество.",
    "📖 Прочитай заговор и скажи: 'Я пробуждаю силу внутри себя!'",
    "🍞 Отправь фото самой обычной еды, назвав её 'зелье'.",
    "🌪 Скажи: 'Я открываю врата хаоса' и замолчи на 5 минут.",
    "🐔 Напиши: 'Ко-ко-ко. Я магический петух' в чат.",
    "🦄 Отправь сообщение: 'Я верю в единорогов и не стыжусь этого!'",
    "🤝 Похвали кого-то в этом чате, но с сарказмом.",
    "🧞 Загадочно намекни кому-то на 'знак судьбы'.",
    "🐢 Назови себя 'Мудрой черепахой' до конца дня.",
    "📢 Напиши caps lock'ом: 'МЕНЯ ПОСЕТИЛА ВЕДЬМА'.",
    "📻 Включи музыку и кинь скрин того, что слушаешь.",
    "🍀 Поделись суеверием, в которое веришь.",
    "🎬 Отправь gif из любимого магического фильма.",
    "🦇 Сделай страшное лицо и скинь селфи.",
    "🧙‍♀️ Напиши: 'Я готов(а) к великому испытанию!' в чат.",
    "🔕 Замолчи на 10 минут, пока тебя не призовут командой.",
    "🧊 Отправь эмодзи, описывающий своё настроение как дух.",
    "📛 Придумай страшное ведьминское имя для себя.",
    "🐸 Напиши в чат: 'Ква! Я амфибия судьбы!'",
    "🐲 Изобрази дракона голосом в голосовухе.",
    "🧹 Сними, как подметаешь что угодно и назови это 'обрядом очищения'.",
    "📕 Назови любую случайную книгу 'Книга теней' и зачитай оттуда фразу.",
    "🧴 Напиши: 'Я освятил(а) руки магическим спиртом'.",
    "🕳 Притворись NPC и говори только шаблонные фразы 2 минуты.",
    "🌀 Назови случайного человека в чате своим 'мастером'.",
    "🐝 Отправь сообщение пчелиного языка: 'Ж-ж-ж!' + имя.",
    "🔒 Скажи: 'Мой разум закрыт, но сердце открыто.'",
    "💫 Спроси у любого: 'Ты тоже слышал(а) голос Мани?'",
    "🕯️ Загадай желание и публично озвучь его.",
    "🦉 Притворись совой и отправь сообщение с 'Угу!' + совет.",
    "🧃 Отправь фото напитка и скажи, что это 'зелье уверенности'.",
    "📿 Сделай вид, что предсказываешь судьбу и опиши чью-то жизнь.",
    "🌝 Напиши: 'Я видел(а) знак на луне прошлой ночью.'",
    "🧚 Напиши сообщение в стиле феи: с блёстками и розами."
]
keyword_reactions = {
    "магия": [
        "✨ Магия витает в воздухе!",
        "🪄 Кто-то сказал магия? Я уже тут!",
        "🌟 Тут явно что-то волшебное происходит...",
        "📜 Заклинание почти готово!",
        "✨ Шшш... не спугни магию!"
    ],
    "ведьма": [
        "🧙‍♀️ Баба Маня слушает внимательно...",
        "Ты звал ведьму? Я пришла!",
        "🕯️ Ведьма чувствует твои вибрации...",
        "🔮 У ведьмы было предчувствие...",
        "🧹 Метла заведена, полетела!"
    ],
    "пророчество": [
        "🔮 Сейчас будет пророчество...",
        "👁️ Я вижу знаки...",
        "📖 Судьба уже написана...",
        "🪬 Ветер шепчет что-то важное...",
        "🌘 Луна сегодня говорит ясно."
    ],
    "зелье": [
        "🧪 Варю зелье, не отвлекай!",
        "🥄 Один глоток — и всё изменится.",
        "🍵 Вкус странный, но работает.",
        "⚗️ Секретный ингредиент уже добавлен...",
        "🫙 Это зелье — не для слабонервных."
    ],
    "астрал": [
        "🌌 Я уже наполовину в астрале.",
        "🌀 Тонкие миры открываются...",
        "🛸 Кто-то зовёт из другого измерения.",
        "✨ Астральные токи сильны сегодня.",
        "👣 Только не забудь вернуться обратно!"
    ],
    "карты": [
        "🃏 Карты Таро уже наготове.",
        "🔁 Судьба тасуется снова.",
        "♠️ Карта выпала — держись.",
        "🂱 Перевернулась — это знак!",
        "📜 Спрашивай, и карты ответят."
    ],
    "луна": [
        "🌕 Луна полна силы сегодня.",
        "🌙 Лунный свет всё проясняет.",
        "🌑 В новолуние желания особенно сильны.",
        "🦉 Луна слушает твои мысли.",
        "🔭 Посмотри на небо — и всё поймёшь."
    ],
    "знаки": [
        "🪧 Присмотрись — вселенная подаёт сигналы.",
        "🦋 Знак может быть в самом неожиданном месте.",
        "🔎 Ты видишь, но не всегда замечаешь.",
        "📡 Космос вещает. Лови волну.",
        "🕊️ Знаки — это шепот судьбы."
    ],
    "ритуал": [
        "🕯️ Ритуал требует тишины и сосредоточенности.",
        "💀 Что-то начинается... обряд пошёл.",
        "🔥 Огонь очищает, как и намерение.",
        "🧿 Всё готово — только скажи слово.",
        "🌫️ Туман сгущается... пора начинать."
    ],
    "сила": [
        "⚡ Внутри тебя больше силы, чем ты думаешь.",
        "🛡️ Время взять силу в свои руки.",
        "🐉 Сила проснулась — будь осторожен.",
        "💥 Сила проявляется через действие.",
        "🌋 Не прячь свою энергию — она нужна миру."
    ],
    "предзнаменование": [
        "🕰️ Что-то странное витает в воздухе...",
        "🌫️ Это не просто совпадение.",
        "🕊️ Тень промелькнула — чувствовал?",
        "⏳ Время даёт знак, но молчит.",
        "🌪️ Предзнаменование близко — будь внимателен."
    ],
    "лакомство": [
        "🍬 Это лакомство – как маленькое волшебство.",
        "🍯 Сладкое, словно мёд с луговых цветов.",
        "🍪 Попробуй — и день станет ярче.",
        "🍫 Лакомство для души и тела.",
        "🍭 Вкус детства и радости в одном кусочке."
    ],
    "шкатулка": [
        "📦 В шкатулке хранятся секреты и воспоминания.",
        "🔐 Открой шкатулку — и найдёшь немного магии.",
        "🎶 Музыка из шкатулки заставляет сердце биться чаще.",
        "🗝️ В каждом замке — своя история.",
        "📿 Шкатулка таит тайны давно забытых времен."
    ],
    "письмо": [
        "✉️ Письмо — как послание из другого мира.",
        "🖋️ Каждое слово пропитано чувствами.",
        "📜 Письмо раскрывает души сокровенные уголки.",
        "📬 Отправь письмо — и пусть судьба ответит.",
        "🕊️ Письмо летит, как голубь надежды."
    ],
    "камин": [
        "🔥 Камин дарит тепло не только телу, но и душе.",
        "🌙 В свете камина вечер становится волшебным.",
        "🌿 Запах дров напоминает о домах детства.",
        "🪵 Камин шепчет истории прошедших зим.",
        "✨ Пламя в камине — маленькое чудо уюта."
    ],
    "филин": [
        "🦉 Филин — ночной страж и мудрый советчик.",
        "🌌 Его глаза — зеркало звёздного неба.",
        "🕯️ Филин охраняет тайны тёмных лесов.",
        "🌙 В его крике слышна древняя песня ночи.",
        "🪶 Филин ведёт туда, где свет встречается с тьмой."
    ],
    "сундучок": [
        "🎁 Сундучок хранит сокровища и загадки.",
        "🗝️ Открой сундучок — и найдёшь частичку счастья.",
        "📦 В сундучке спит тайна, ждёт своего часа.",
        "🕰️ Время не властно над тем, что хранит сундучок.",
        "🔮 Сундучок — портал в мир воспоминаний."
    ],
    "кисть": [
        "🎨 Кисть — инструмент для создания чудес.",
        "🖌️ С кистью мир становится ярче и добрее.",
        "✨ Каждое движение кисти — как заклинание цвета.",
        "🖼️ Кисть творит миры, невидимые глазу.",
        "🌈 С кистью в руках оживают мечты."
    ],
    "перо": [
        "🪶 Перо — ключ к мыслям и словам.",
        "✒️ С пером в руках рождаются истории и магия.",
        "📜 Перо — инструмент для души и сердца.",
        "🖋️ Каждый штрих пера — отпечаток судьбы.",
        "🕊️ Перо несёт лёгкость и свободу слова."
    ],
    "пыльца": [
        "🌸 Пыльца — крошечные волшебники цветочного мира.",
        "🍃 Пыльца летит, создавая жизнь и чудеса.",
        "🌼 В пыльце — обещание нового начала.",
        "✨ Пыльца сверкает в лучах солнца, как звёзды.",
        "🐝 Пыльца — подарок природы, наполненный силой."
    ],
    "свисток": [
        "🎶 Свисток зовёт на приключения и веселье.",
        "📯 Свисток — сигнал к началу волшебства.",
        "🦜 Свисток умеет разговаривать с ветром.",
        "🎵 Свисток звучит, когда в воздухе магия.",
        "🕰️ Свисток напоминает о времени и ритме жизни."
    ]
}

async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id not in chat_members:
        chat_members[chat_id] = {}

    chat_members[chat_id][user.id] = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
    }
    chat_ids.add(chat_id)

    text = update.message.text.lower()

    for keyword, responses in keyword_reactions.items():
        if keyword in text:
            response = random.choice(responses)
            await update.message.reply_text(response)
            break  # реагировать только на первое найденное слово


chat_members = {}
chat_ids = set()
last_horoscope_usage = {}
last_ritual_usage = {}
auto_posting_enabled = {}


user_added_truths = []
user_added_dares = []

async def add_truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Пример: /addtruth Какая у тебя любимая магия?")
        return

    truth = " ".join(context.args)
    truth_questions.append(truth)
    user_added_truths.append(truth)

    await update.message.reply_text("✅ Твоя *Правда* добавлена!", parse_mode=ParseMode.MARKDOWN)

async def add_dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Пример: /adddare Сними видео с волшебным танцем!")
        return

    dare = " ".join(context.args)
    dare_challenges.append(dare)
    user_added_dares.append(dare)

    await update.message.reply_text("✅ Твоё *Действие* добавлено!", parse_mode=ParseMode.MARKDOWN)


async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id not in chat_members:
        chat_members[chat_id] = {}

    chat_members[chat_id][user.id] = {
        "id": user.id,
        "username": f"@{user.username}" if user.username else user.full_name,
        "first_name": user.first_name,
    }
    chat_ids.add(chat_id)

    text = update.message.text.lower()

    for keyword, responses in keyword_reactions.items():
        if keyword in text:
            response = random.choice(responses)
            await update.message.reply_text(response)
            break  # реагировать только на первое найденное слово

    

async def meme_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not meme_urls:
        await update.message.reply_text("Мемов нет, но духи говорят, что ты прекрасен 💫")
        return

    meme_url = random.choice(meme_urls)
    await update.message.reply_photo(photo=meme_url, caption="🔮 Мемное-предсказание от Бабы Мани")

async def mus_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not vibe:  # если список пустой
        await update.message.reply_text("Музыки нет, но духи говорят, что ты прекрасен(а) 💫")
        return

    song_url = random.choice(vibe)
    caption_text = random.choice(caption)

    await update.message.reply_text(f"{caption_text}\n{song_url}")
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Меня зовут Баба Маня. Напиши /prediction или /lovestory, чтобы узнать судьбу! TKACH MAX - developer. Обновление 11.06: 1.Гороскоп теперь не доступен, теперь он будет приходить 1 раз в день в чат! 2.Добавлена игра Правда или действие, с вожностью добавлять свои вопросы и действия! 3.Добавлена возможность включать и отключать автопредсказания! 4.Добавлены мемы в мемные-предсказания - списибо Викусе за помощь!")
    
    
async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, predictions)
    
async def predictionToday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, predictionsToday)

async def predictionTomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, predictionsTomorrow)

async def Recomendation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, recom)
    
async def love_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, love_predictions)

async def love_ball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, love)
async def ball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_prediction(update, context, Ball)
from telegram.constants import ParseMode

async def ritual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.datetime.now()
    last_used = last_ritual_usage.get(user_id)

    if last_used and (now - last_used).total_seconds() < 86400:
        await update.message.reply_text("🔒 Ты уже проводил обряд за последние 24 часа. Приходи позже.")
        return

    if not context.args:
        await update.message.reply_text("👤 Укажи пользователя после команды. Пример:\n/ritual @username")
        return

    target_username = context.args[0]
    if not target_username.startswith("@"):
        await update.message.reply_text("⚠️ Укажи корректный @username.")
        return

    last_ritual_usage[user_id] = now

    await update.message.reply_text("🔮 Баба Маня начала обряд... Медленно варит зелье...")

    await asyncio.sleep(2)  # эффект обряда

    character = random.choice(character_traits)
    love = random.choice(love_traits)
    career = random.choice(career_traits)
    work = random.choice(Work)
    future = random.choice(future_predictions)
    attract = random.choice(attractiveness)
    score = random.randint(1, 10)
    a1 = random.randint(1, 10)
    a2 = random.randint(1, 10)
    a3 = random.randint(1, 10)
    a4 = random.randint(1, 10)
    a5 = random.randint(1, 10)

    response = f"""🔮 *Магический анализ для {target_username}*:

🧠 *Характер*: {character}
❤️ *Любовь*: {love}
💼 *Карьера*: {career}
✍️ *Возможная Работа*: {work}
🔮 *Будущее*: {future}
🖕 *Степень уверенности в себе(/10)*: {a1}
✊ *Стрессоустойчивость(/10)*: {a2}
💋 *Уровень эмпатии(/10)*: {a3}
💢 *Уровень мотивации(/10)*: {a4}
🤪 *Чувство юмора(/10)*: {a5}
✨ *Привлекательность*: {attract}
 

🏅 *Общая оценка*: *{score}/10*

_Обряд завершён. Баба Маня уходит в туман..._"""

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

async def send_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE, source):
    chat_id = update.effective_chat.id
    members_dict = chat_members.get(chat_id, {})
    members_list = list(members_dict.values())

    if len(members_list) == 0:
        await update.message.reply_text(
            "Я пока никого не вижу в чате. Напиши что-нибудь, чтобы я тебя запомнила 🔮"
        )
        return

    if len(members_list) == 1:
        user1 = members_list[0]
        template = random.choice(solo_predictions)
        text = template.format(
            user1=user1["username"],
            user1_first_name=user1["first_name"]
        )
    else:
        user1, user2 = random.sample(members_list, 2)
        template = random.choice(source)
        text = template.format(
            user1=user1["username"],
            user2=user2["username"],
            user1_first_name=user1["first_name"],
            user2_first_name=user2["first_name"]
        )

    await update.message.reply_text(text)
last_horoscope_sent = {}

async def daily_horoscope_post(app):
    while True:
        now = datetime.datetime.now()
        if now.hour == 9:  # В 9 утра
            for chat_id in chat_ids:
                last_sent = last_horoscope_sent.get(chat_id)
                if not last_sent or (now - last_sent).days >= 1:
                    message = "🌟 Гороскоп на сегодня:\n\n"
                    for sign, dates in zodiac_signs.items():
                        prediction = random.choice(horoscope_texts)
                        message += f"▶️ {sign} ({dates}): {prediction}\n"
                    try:
                        await app.bot.send_message(chat_id=chat_id, text=message)
                        last_horoscope_sent[chat_id] = now
                    except Exception as e:
                        print(f"Ошибка при отправке гороскопа в чат {chat_id}: {e}")
        await asyncio.sleep(3600)  # Проверка каждый час
async def after_startup(app):
    asyncio.create_task(auto_post(app))
    asyncio.create_task(daily_horoscope_post(app))

async def tyan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tyan_images:
        await update.message.reply_text("🧙‍♀️ закончились аниме-девочки!")
        return
    
    user = update.effective_user
    user_display = f"@{user.username}" if user.username else user.full_name
    
    photo_url = random.choice(tyan_images)
    await update.message.reply_photo(photo=photo_url, caption=f"✨ Баба Маня превратила {user_display} в аниме-девочку!")

async def auto_post(app):
    await asyncio.sleep(10)
    while True:
        for chat_id in chat_ids:
            if not auto_posting_enabled.get(chat_id, True):
                continue  # Автопостинг отключён

            members = list(chat_members.get(chat_id, {}).values())
            if len(members) >= 2:
                user1, user2 = random.sample(members, 2)
                try:
                    text = random.choice(autopred).format(
                        user1=user1["username"],
                        user2=user2["username"],
                        user1_first_name=user1["first_name"],
                        user2_first_name=user2["first_name"]
                    )
                    await app.bot.send_message(chat_id=chat_id, text=f"🔮 Предсказание: {text}")
                except Exception as e:
                    print(f"Ошибка при отправке в чат {chat_id}: {e}")
        await asyncio.sleep(21600)  # Раз в час
async def disable_autopost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    auto_posting_enabled[chat_id] = False
    await update.message.reply_text("🔕 Автопредсказания отключены в этом чате.")

async def enable_autopost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    auto_posting_enabled[chat_id] = True
    await update.message.reply_text("🔔 Автопредсказания включены в этом чате.")

async def truth_or_dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_display = f"@{user.username}" if user.username else user.first_name

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔍 Правда", callback_data=f"truth|{user_display}"),
            InlineKeyboardButton("⚡️ Действие", callback_data=f"dare|{user_display}")
        ]
    ])

    await update.message.reply_text(
        f"🎲 *{user_display}*, выбери свою судьбу:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )

async def truth_or_dare_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    choice, user = data.split("|")

    if choice == "truth":
        result = random.choice(truth_questions)
        prefix = "🔍 *Правда*"
    else:
        result = random.choice(dare_challenges)
        prefix = "⚡️ *Действие*"

    await query.edit_message_text(
        text=f"{prefix} для {user}:\n\n{result}",
        parse_mode=ParseMode.MARKDOWN
    )



def main():
    Thread(target=run_flask).start()

    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prediction", prediction))
    app.add_handler(CommandHandler("predictiontoday", predictionToday))
    app.add_handler(CommandHandler("predictiontomorrow", predictionTomorrow))
    app.add_handler(CommandHandler("lovestory", love_story))
    app.add_handler(CommandHandler("loveball", love_ball))
    app.add_handler(CommandHandler("Ball", ball))
    app.add_handler(CommandHandler("memeprediction", meme_prediction))
    app.add_handler(CommandHandler("musicprediction", mus_prediction))
    app.add_handler(CommandHandler("ritual", ritual))
    app.add_handler(CommandHandler("tyan", tyan))
    app.add_handler(CommandHandler("disable_autopost", disable_autopost))
    app.add_handler(CommandHandler("enable_autopost", enable_autopost))
    app.add_handler(CommandHandler("truthordare", truth_or_dare))
    app.add_handler(CommandHandler("addtruth", add_truth))
    app.add_handler(CommandHandler("adddare", add_dare))
    app.add_handler(CommandHandler("recomendation", Recomendation))
    app.add_handler(CallbackQueryHandler(truth_or_dare_callback, pattern="^(truth|dare)\|"))
    add_meme_handler = ConversationHandler(entry_points=[CommandHandler("addmeme", add_meme_start)],
    states={ADD_MEME: [MessageHandler(filters.PHOTO, handle_meme_photo)]},
    fallbacks=[CommandHandler("cancel", cancel_add_meme)],)

app.add_handler(add_meme_handler)

app.add_handler(add_meme_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_user))
    




    async def after_startup(app):
        asyncio.create_task(auto_post(app))

    app.post_init = after_startup

    print("🤖 Баба Маня запущена!")
    app.run_polling()

if __name__ == "__main__":
    main()
