"""
Good Day Полоцк — Telegram-бот феста
Создано: PolotAI (@yanchqqq1)
Локальная версия (для запуска на Mac).
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from openai import OpenAI

# ============================================================
#  НАСТРОЙКИ — ЗАПОЛНИ ПЕРЕД ЗАПУСКОМ
# ============================================================

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

MAP_IMAGE = "map.png"
PROGRAM_IMAGE = "program.png"

# ============================================================
#  КОНТЕНТ ФЕСТА
# ============================================================

WELCOME_TEXT = (
    "🎉 <b>Добро пожаловать на GOOD DAY ПОЛОЦК!</b>\n\n"
    "Я — твой личный ассистент и навигатор по фесту.\n"
    "Здесь 40+ локаций, море активностей и горы призов!\n\n"
    "🗺 <b>Как это работает?</b>\n"
    "Проходи испытания на локациях.\n"
    "Получай Good Tokens.\n"
    "Обменивай токены на крутые призы в Центре выдачи призов "
    "(работает до 19:00)\n\n"
    "👇 <b>Выбери следующий шаг:</b>"
)

# Картинка-афиша для приветствия
WELCOME_IMAGE = "welcome.png"

PROGRAM_CAPTION = (
    "📋 <b>ПРОГРАММА GOOD DAY ПОЛОЦК</b>\n"
    "Вся подробная программа — на афише выше 👆"
)

PROGRAM_FULL = (
    "📋 <b>ПРОГРАММА GOOD DAY ПОЛОЦК</b>\n\n"
    "⭐️ <b>Главное по площадкам:</b>\n\n"
    "🎪 <b>Площадка GOOD DAY</b> — 12:00–00:00\n"
    "<blockquote>"
    "🎈 Детская программа — 12:20–15:10\n"
    "🎩 Иллюзионист Глеб Сафонов — 16:00\n"
    "🌈 Holi Kids Party — 16:20\n"
    "🕺 Just Dance — 16:50\n"
    "🤸 Jumping с Be Fit — 17:00\n"
    "🧠 Квиз-шоу «Точка сбора» — 18:00\n"
    "🎤 MIXLOTO и караоке — 19:30\n"
    "🎁 Итоги «Фестиваля подарков» — 23:00"
    "</blockquote>\n"
    "⚔️ <b>Фэнтези-бал «Игра престолов»</b> — 12:00–21:00\n"
    "<blockquote>"
    "🏰 Фотозоны и интерактивные площадки\n"
    "⚔️ Фехтование и танцы\n"
    "🧩 Тематический квест\n"
    "👑 Конкурс костюмов"
    "</blockquote>\n"
    "🧘 <b>Energy-зона</b>\n"
    "<blockquote>"
    "Массовая практика йоги — 12:30\n"
    "Dog-шоу — 14:30\n"
    "Джампинг — 15:30\n"
    "Bachata Open Air — 16:30"
    "</blockquote>\n"
    "🎨 <b>Мастер-классы и активности</b> — 12:00–21:00\n"
    "<blockquote>"
    "🎨 Творческие мастер-классы\n"
    "🧪 Эксперименты и квесты\n"
    "💻 Программирование от KLiK\n"
    "🎭 Театральный пикник\n"
    "🌺 Цветущий сад\n"
    "✨ Аквагрим и блеск-тату"
    "</blockquote>\n"
    "ℹ️ Инфоцентр — 11:00–23:00\n" "🎁 Центр выдачи призов — 12:00–19:00\n"
    "🧩 Палатка с заданиями — 12:00–18:00\n"
    "🏃 Спортивная зона — 12:00–18:00\n"
    "🍔 Фудкорт и развлечения — 12:00–00:00"
)

PRIZES_CAPTION = (
    "🎁 <b>АКТУАЛЬНЫЙ СПИСОК ПРИЗОВ</b>\n\n"
    "Здесь находится актуальный список призов, доступных для обмена "
    "на Good Token.\n\n"
    "Список обновляется в течение дня по мере выдачи подарков, поэтому "
    "ты всегда можешь проверить, какие призы ещё доступны прямо сейчас 👀\n\n"
    "Нажми кнопку ниже, чтобы открыть список призов.\n\n"
    '<a href="https://docs.google.com/document/d/13784rV3ld77L2L6TKVlU7aUNmAdaZS6W/edit">🔘 Открыть список призов</a>'
)

# Имя файла со списком призов
PRIZES_PDF = "prizes.pdf"

TASKS_TEXT = (
    "📋 <b>СПИСОК ЗАДАНИЙ</b>\n\n"
    "Good Token уже ждут тебя! 💙\n"
    "Выполняй задания на площадках, участвуй в активностях и собирай "
    "токены, которые можно обменять на призы в Центре выдачи "
    "(локация №9).\n\n"
    '<a href="https://docs.google.com/document/d/1lxeNaHUH2hTne-TpQnVE3ltMSgiE1ud7/edit">⬇️ Открыть список заданий</a>'
)

QUEST_TEXT = (
    "🎯 <b>Добро пожаловать в GOOD DAY QUEST!</b>\n\n"
    "Поздравляем, ты в игре.\n"
    "С этого момента каждая активность может принести тебе GoodToken.\n\n"
    "Проходи задания, участвуй в конкурсах, посещай площадки "
    "партнёров и собирай валюту феста.\n\n"
    "Чем больше токенов соберёшь — тем больше подарков сможешь забрать.\n\n"
    "🔥 Выполняй задания и зарабатывай свои первые GoodToken."
)

ACTIVITIES_TEXT = (
    "🏃 <b>СПИСОК АКТИВНОСТЕЙ</b>\n\n"
    "Выполняй активности на площадках, зарабатывай GoodToken "
    "и обменивай их на призы.\n\n"
    "💡 <i>Подходи к волонтёру на площадке — он начислит токены!</i>"
)

SECRET_TASK_TEXT = (
    "🤫 <b>СЕКРЕТНОЕ ЗАДАНИЕ</b>\n\n"
    "1️⃣ Сфотографируй свой браслет Good Day Quest\n"
    "2️⃣ Выложи фото в Stories с текстом «Good Day Quest»\n"
    "3️⃣ Покажи сторис волонтёру в Палатке с заданиями (локация №9)\n\n"
    "🎁 <b>Награда: +2 Good Tokens!</b>\n\n"
    "⏰ <i>Палатка с заданиями работает 12:00–18:00</i>"
)

# --- Браслет (главный экран) ---
QUEST_BRACELET_TEXT = (
    "🟡 <b>Браслет QUEST</b>\n"
    "Для активных и любознательных 💙\n\n"
    "<b>Что входит:</b>\n\n"
    "🧩 <b>Good Day Quest</b>\n"
    "Участвуй в квесте, получай GoodToken и обменивай их на призы.\n\n"
    "⚡️ <b>Вне очереди</b>\n"
    "Внеочередное обслуживание на активностях квеста перед теми,  кто без браслета.\n\n"
    "🤖 <b>Онлайн-ассистент феста</b>\n"
    "Вся информация всегда под рукой.\n\n"
    "📱 <b>Подписка Good Day на 1 месяц</b>\n"
    "Дополнительные скидки и предложения от партнёров.\n\n"
    "💡 Знай, что в любой момент феста ты можешь улучшить свой "
    "браслет и получить ещё больше возможностей!"
)

# --- Улучшить браслет (общий экран) ---
UPGRADE_TEXT = (
    "🚀 <b>Хочешь получить больше возможностей на фесте?</b>\n\n"
    "Ты можешь обменять свой браслет на более высокий уровень "
    "прямо во время феста.\n\n"
    "Доступны:\n"
    "🟢 VIP\n"
    "🟡 VIP DELUXE\n\n"
    "Каждый следующий уровень открывает дополнительные бонусы, "
    "подарки и привилегии.\n\n"
    "📍 Обратитесь на Инфо-центр возле фонтана.\n\n"
    "Стоимость улучшения рассчитывается по формуле:\n"
    "<i>Цена нового браслета − стоимость текущего браслета + 5 BYN</i>"
)

# --- STANDART ---
STANDART_TEXT = (
    "🔵 <b>STANDART</b>\n"
    "Отлично подойдёт для каждого 💙\n\n"
    "<b>В подарок к браслету вы получаете:</b>\n"
    "✅ Участие в Good Day Quest\n"
    "✅ Получение и обмен Good Token на призы\n"
    "✅ Внеочередное обслуживание на активностях квеста перед теми, "
    "кто без браслета\n"
    "✅ Онлайн-ассистент феста\n\n"
    "🎁 <b>Дополнительные бонусы:</b>\n"
    "🌈 Пакетик красок Holi\n"
    "📸 Доступ к фотоальбому феста\n"
    "🎁 Онлайн-доступ к актуальному списку призов\n"
    "🏰 Бесплатное посещение квеста и фотозон Фэнтези-бала\n"
    "⭐️ VIP-зона Good Day с 12:00 до 19:00 + 📷 работа фотографа в VIP-зоне\n"
    "🪙 5 Good Token в подарок\n"
    "📱 Подписка на Good Day на 3 месяца\n\n"
    "💡 Знай, что в любой момент феста ты можешь улучшить свой браслет "
    "и получить ещё больше возможностей!"
)

# --- VIP ---
VIP_TEXT = (
    "🟢 <b>VIP</b>\n"
    "Отличный баланс возможностей 💙\n\n"
    "<b>В подарок к браслету ты получаешь:</b>\n"
    "✅ Участие в Good Day Quest\n"
    "✅ Получение и обмен Good Token на призы\n"
    "✅ Внеочередное обслуживание на активностях квеста перед теми,  кто без браслета\n"
    "✅ Онлайн-ассистент феста\n"
    "✅ Пакетик красок Holi\n"
    "✅ Доступ к фотоальбому феста\n"
    "✅ Онлайн-доступ к актуальному списку призов\n"
    "✅ Бесплатное посещение квеста и фотозон Фэнтези-бала\n\n"
    "🎁 <b>Дополнительные бонусы:</b>\n"
    "✨ Бесплатные селфи-зеркало, аквагрим и видеоспиннер\n"
    "⭐️ VIP-зона Good Day с 12:00 до 00:00 + 📷 работа фотографа\n"
    "🎟 Бесплатное участие в MixLoto\n"
    "🪙 10 Good Token в подарок\n"
    "📱 Подписка Good Day на 6 месяцев"
)

# --- VIP DELUXE ---
DELUXE_TEXT = (
    "🟠 <b>VIP DELUXE</b>\n"
    "Лучший выбор для яркого дня! 🔥\n\n"
    "<b>В подарок к браслету ты получаешь:</b>\n"
    "✅ Участие в Good Day Quest\n"
    "✅ Получение и обмен Good Token на призы\n"
    "✅ Внеочередное обслуживание на активностях квеста перед теми,  кто без браслета\n"
    "✅ Онлайн-ассистент феста\n"
    "✅ Пакетик красок Holi\n"
    "✅ Доступ к фотоальбому феста\n"
    "✅ Онлайн-доступ к актуальному списку призов\n"
    "✅ Бесплатное посещение квеста и фотозон Фэнтези-бала\n"
    "✅ Бесплатные селфи-зеркало, аквагрим и видеоспиннер\n"
    "✅ VIP-зона Good Day с 12:00 до 00:00 + 📷 работа фотографа\n"
    "✅ Бесплатное участие в MixLoto\n\n"
    "🎁 <b>Дополнительные бонусы:</b>\n"
    "🎡 Одно бесплатное посещение всех аттракционов\n"
    "🎨 Одно бесплатное посещение всех мастер-классов\n"
    "🪙 20 Good Token в подарок\n"
    "📱 Подписка Good Day на 12 месяцев\n\n"
    "Это максимальный пакет возможностей на фесте и самый "
    "выгодный вариант для тех, кто хочет попробовать всё 💙"
)

# --- Где улучшить браслет ---

RAFFLE_TEXT = (
    "🎁 <b>Не упусти шанс принять участие в большом "
    "розыгрыше Good Day!</b>\n\n"
    "Среди главных призов:\n\n"
    "✨ 12 моющих пылесосов Dreame G10\n"
    "📺 Телевизор Roome 65\"\n\n"
    "Участвовать можно двумя способами:\n\n"
    "📍 Лично — в палатке «Рекламная игра от Good Day» на фесте\n"
    "📱 Онлайн\n\n"
    "⏰ Приём заявок открыт до 23:00 \n\n"
    "🎤 А уже сегодня в 23:00 на площадке GOOD DAY ПОЛОЦК (на сцене) состоится "
    "подведение итогов и розыгрыш всех главных призов!\n\n"
    "💙 Не откладывай на потом — возможно, именно сейчас удача улыбается тебе."
)


MAP_TEXT = (
    "🗺 <b>КАРТА ФЕСТА</b>\n\n"
    "Все локации отмечены номерами на карте 👆\n\n"
    "📍 <b>№5 — Фэнтези-бал «Игра престолов»</b>\n"
    "⚔️ Квесты, фотозоны, фехтование, конкурс костюмов\n\n"
    "📍 <b>№7 — Мастер-классы и активности</b>\n"
    "🎨 Творчество, квесты, аквагрим и многое другое\n\n"
    "📍 <b>№8 — Тематическая площадка GOOD DAY ПОЛОЦК</b>\n"
    "🎁 Розыгрыши, детская программа, Holi Party, MIXLOTO и главные активности\n\n"
    "📍 <b>№9 — Инфоцентр, Центр выдачи призов и Палатка с заданиями</b>\n"
    "🧩 Здесь начинается Good Day Quest\n\n"
    "📍 <b>№10 — Energy-зона</b>\n"
    "🧘 Йога, джампинг, танцы и активный отдых\n\n"
    "📍 <b>№11 — Аттракционы</b>\n"
    "🎡 Развлечения для детей и взрослых\n\n"
    "📍 <b>№12 — Фуд-зона</b>\n"
    "🍔 Еда, напитки и место для отдыха\n\n"
    "Не можешь найти нужную площадку? Просто напиши мне 👇"
)

PHOTOS_TEXT = (
    "📸 <b>ФОТОАЛЬБОМ ФЕСТА</b>\n\n"
    "Все фотографии с GOOD DAY ПОЛОЦК будут загружаться в этот альбом "
    "после мероприятия.\n"
    "📷 Фото будут доступны в течение 10 дней после завершения события.\n\n"
    '<a href="https://drive.google.com/drive/folders/1ypCYZdJKXU9fwwCSt0SX3B2rlZhWkfaf?usp=sharing">📸 Открыть фотоальбом</a>'
)

SOCIALS_TEXT = (
    "🌐 <b>НАШИ СОЦ. СЕТИ</b>\n\n"
    "Подписывайся, чтобы не пропустить обновления!"
)

INSTAGRAM_LINK = "https://instagram.com/good_day_open_air"

FESTIVAL_KNOWLEDGE = """
Ты — дружелюбный ИИ-ассистент феста «Good Day Полоцк» / «Летний Драйв: День Молодежи и Студенчества».
Дата: 27 июня 2026 года, город Полоцк, Беларусь. Площадь Ф. Скорины (Фонтан) и прилегающая территория.

ЛОКАЦИИ НА КАРТЕ (по номерам):
1 — Концертная зона
2 — Зона ремесленников
3 — Тематическая площадка «Молодёжное крыло»
4 — Тематическая площадка «Зона безопасности: профессионалы рядом»
5 — Фэнтези-бал «Игра Престолов»
6 — Спортивная зона
7 — Мастер-классы
8 — Тематическая площадка «Good Day Полоцк» (главная сцена)
9 — Инфоцентр, Центр выдачи призов, Палатка с заданиями
10 — Зона Energy
11 — Аттракционы
12 — Фуд-зона
Также на карте: остановочные пункты, кинотеатр «Родина», памятник «Географический центр Европы», гостиница «Двина».

РЕЖИМ РАБОТЫ ЗОН:
- Инфоцентр: 11:00–23:00
- Спортивная зона + Выбор ЗОЖ: 12:00–18:00
- Палатка с заданиями: 12:00–18:00
- Центр выдачи призов: 12:00–19:00
- Фуд-корт, развлечения: 12:00–00:00

ПРОГРАММА ГЛАВНОЙ СЦЕНЫ «GOOD DAY ПОЛОЦК»:
- 12:00 Открытие площадки
- 12:05 Розыгрыш от Good Day
- 12:15 Танец от студии Star City
- Детская программа: 12:20 анимация, 13:05 ростовая кукла Зайка Лапочка, 13:15 Сикс Севен Тренд Пати, 14:00 Медведь Тедди, 14:10 Frog-зарядка, 14:30 мини-диско + шоу мыльных пузырей, 15:10 химическое шоу
- 16:00 Иллюзионист Глеб Сафонов
- 16:20 Holi Kids Party (вечеринка красок), ростовая кукла Артур Пирожков
- 16:50 Just Dance
- 17:00 Jumping с Be Fit Полоцк
- 17:10 Fit Frog FM
- 18:00 Квиз-шоу «Точка сбора»
- 19:30 Mixloto — микс лото и караоке
- 21:30 Выступление Мари Краймбрери
- 23:00 Итоги розыгрыша «Фестиваль подарков от Good Day» (12 моющих пылесосов и ТВ 65 дюймов)

ФЭНТЕЗИ-БАЛ «ИГРА ПРЕСТОЛОВ»:
- 12:00 Открытие бала с приветственным танцем и парадом домов в костюмах
- 12:00–18:00 Интерактивные зоны, мастер-классы по танцам, по фехтованию, плетение волос
- 12:00–21:00 Лавка чудес, тематические фотозоны
- 14:00–17:00 Квест по мотивам «Песни Льда и Пламени»
- 16:00 Конкурс костюмов

ENERGY ЗОНА:
- 12:30 Масштабная практика йоги Energy of Yoga
- 14:30 Dog-шоу Алёны Ващенко
- 15:30 Мастер-класс по джампингу (фитнес на мини-батутах)
- 16:30 Мастер-класс и танцы под открытым небом (Bachata Open Air)

МАСТЕР-КЛАССЫ И АКТИВНОСТИ:
- 12:00–16:00 от «Радуги»: рисование на гипсовых фигурах, изготовление слаймов, рисование на шопперах
- от «Оранжевого настроения»: роспись печенья, роспись мини-шопперов, изготовление значков
- 12:00–18:00: строительство, программирование от «Klik», наклейки, пиратский квест, ароматный квест, музыкальный мастер-класс «Саунд код», собирай-ка, театральный пикник
- 12:00–20:00: цветущий сад (ходулисты, фонарик, цветок-веер), аквагрим, блеск-тату, арт-макияж
- 16:00–20:00 от «Радуги»: изготовление свечей, духов, слаймов
- 12:00–21:00: интерактивная зона «Доктор Драйв», кукла-шоу, Твой Porsche от VIP.AUTO

БРАСЛЕТЫ (уровни и бонусы):
- QUEST (базовый): участие в квесте, GoodToken, обмен на призы, вне очереди, онлайн-ассистент, подписка Good Day 1 месяц
- STANDART (для родителей с детьми): всё из Quest + пакетик красок Holi, фотоальбом, список призов онлайн, фотозоны Фэнтези-бала, VIP-зона 12:00-19:00, 5 Good Token, подписка 3 месяца
- VIP: всё из Standart + селфи-зеркало/аквагрим/видеоспиннер, VIP-зона 12:00-00:00, бесплатное участие в MixLoto, 10 Good Token, подписка 6 месяцев
- VIP DELUXE: всё из VIP + одно бесплатное посещение всех аттракционов и всех мастер-классов, 20 Good Token, подписка 12 месяцев
- Улучшить браслет можно на Инфо-центре возле фонтана (локация 9). Формула: цена нового − цена текущего + 5 BYN

КВЕСТ GOOD TOKENS:
- Проходи задания на площадках, получай Good Tokens
- Обменивай токены на призы в Центре выдачи (локация 9, до 19:00)
- Более 500 призов: сертификаты, развлечения, цветы, спорт, красота, еда, техника

БОЛЬШОЙ РОЗЫГРЫШ:
- 12 моющих пылесосов Dreame G10 и телевизор Roome 65"
- Участие до 23:00: лично в палатке «Рекламная игра от Good Day» или онлайн
- Итоги в 23:00 на главной сцене

ПРАВИЛА:
- Отвечай коротко и по делу, максимум 3-4 предложения
- Если не знаешь ответа — скажи «Уточни в Инфоцентре (локация 9) или напиши организаторам https://instagram.com/good_day_open_air»
- Отвечай на русском языке
- Будь дружелюбным и энергичным, используй эмодзи умеренно
- НЕ ВЫДУМЫВАЙ информацию, которой нет выше

Бот создан PolotAI — автоматизация и ИИ для бизнеса (@yanchqqq1).
"""

# ============================================================
#  КОД БОТА
# ============================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)


def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Программа феста", callback_data="program")],
        [InlineKeyboardButton("🗺 Карта феста", callback_data="map")],
        [InlineKeyboardButton("🎁 Актуальные призы", callback_data="prizes")],
        [InlineKeyboardButton("🎯 Начать квест", callback_data="quest")],
        [InlineKeyboardButton("🎫 Что может мой браслет", callback_data="b_quest")],
        [InlineKeyboardButton("💎 VIP Браслеты", callback_data="bracelet")],
        [InlineKeyboardButton("🏆 Большой розыгрыш", callback_data="raffle")],
        [InlineKeyboardButton("🌐 Наши соц. сети", callback_data="socials")],
        [InlineKeyboardButton("📸 Фотоальбом феста", callback_data="photos")],
    ])


def back_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        with open(WELCOME_IMAGE, "rb") as photo:
            await context.bot.send_photo(
                chat_id=chat_id, photo=photo,
                caption=WELCOME_TEXT, parse_mode="HTML",
                reply_markup=main_menu_keyboard()
            )
    except FileNotFoundError:
        await update.message.reply_text(
            WELCOME_TEXT, parse_mode="HTML", reply_markup=main_menu_keyboard()
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat_id

    # --- Главное меню (без афиши, только текст) ---
    if data == "menu":
        await query.message.reply_text(
            WELCOME_TEXT, parse_mode="HTML", reply_markup=main_menu_keyboard()
        )
        return

    # --- #1 Программа (фото + подпись) ---
    if data == "program":
        # Сначала текст программы
        await context.bot.send_message(
            chat_id=chat_id, text=PROGRAM_FULL, parse_mode="HTML"
        )
        # Затем фото-афиша программы
        try:
            with open(PROGRAM_IMAGE, "rb") as photo:
                await context.bot.send_photo(
                    chat_id=chat_id, photo=photo,
                    caption="📋 Полная программа здесь 👆",
                    reply_markup=back_button()
                )
        except FileNotFoundError:
            await context.bot.send_message(
                chat_id=chat_id, text="📋 Это вся программа!",
                reply_markup=back_button()
            )

    # --- #2 Карта (фото) ---
    elif data == "map":
        # Сначала текст
        await context.bot.send_message(
            chat_id=chat_id, text=MAP_TEXT, parse_mode="HTML"
        )
        # Затем фото-карта
        try:
            with open(MAP_IMAGE, "rb") as photo:
                await context.bot.send_photo(
                    chat_id=chat_id, photo=photo,
                    caption="🗺 Карта феста 👆",
                    reply_markup=back_button()
                )
        except FileNotFoundError:
            await context.bot.send_message(
                chat_id=chat_id, text="🗺 Карта!", reply_markup=back_button()
            )

    # --- #3 Призы ---
    elif data == "prizes":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Назад в меню", callback_data="menu")],
        ])
        await query.message.reply_text(
            PRIZES_CAPTION, parse_mode="HTML",
            reply_markup=keyboard, disable_web_page_preview=True
        )

    # --- Квест ---
    elif data == "quest":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 Список заданий", callback_data="tasks")],
            [InlineKeyboardButton("🎁 Посмотреть актуальный список призов", callback_data="prizes")],
            [InlineKeyboardButton("🤫 Секретное задание", callback_data="secret")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.message.reply_text(QUEST_TEXT, parse_mode="HTML", reply_markup=keyboard)

    # --- Список заданий ---
    elif data == "tasks":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.message.reply_text(
            TASKS_TEXT, parse_mode="HTML",
            reply_markup=keyboard, disable_web_page_preview=True
        )

    # --- Секретное задание ---
    elif data == "secret":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎁 Актуальные призы", callback_data="prizes")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.message.reply_text(SECRET_TASK_TEXT, parse_mode="HTML", reply_markup=keyboard)

    # --- VIP Браслеты (главный экран выбора) ---
    elif data == "bracelet":
        # Показываем возможности VIP и VIP DELUXE, потом кнопку "Улучшить браслет"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬆️ Улучшить браслет", callback_data="upgrade")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await context.bot.send_message(chat_id=chat_id, text=VIP_TEXT, parse_mode="HTML")
        await context.bot.send_message(
            chat_id=chat_id, text=DELUXE_TEXT, parse_mode="HTML",
            reply_markup=keyboard
        )

    elif data == "upgrade":
        # По кнопке "Улучшить браслет" — текст-приглашение с формулой
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🟢 Возможности браслета VIP", callback_data="vip")],
            [InlineKeyboardButton("🟡 Возможности браслета VIP DELUXE", callback_data="deluxe")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.message.reply_text(UPGRADE_TEXT, parse_mode="HTML", reply_markup=keyboard)

    # --- Браслет QUEST ---
    elif data == "b_quest":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬆️ Улучшить браслет", callback_data="upgrade")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.message.reply_text(STANDART_TEXT, parse_mode="HTML", reply_markup=keyboard)

    # --- VIP ---
    elif data == "vip":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🟡 VIP DELUXE", callback_data="deluxe")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.message.reply_text(VIP_TEXT, parse_mode="HTML", reply_markup=keyboard)

    # --- VIP DELUXE ---
    elif data == "deluxe":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🟢 VIP", callback_data="vip")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.message.reply_text(DELUXE_TEXT, parse_mode="HTML", reply_markup=keyboard)

    # --- #6 Розыгрыш ---
    elif data == "raffle":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎟 Принять участие онлайн", url="https://www.instagram.com/p/DZy-sSxDf8J/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==")],
            [InlineKeyboardButton("ℹ️ Узнать подробнее", url="https://www.instagram.com/reel/DZy--P-NFgT/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.message.reply_text(RAFFLE_TEXT, parse_mode="HTML", reply_markup=keyboard)

    # --- Фотоальбом ---
    elif data == "photos":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.message.reply_text(
            PHOTOS_TEXT, parse_mode="HTML",
            reply_markup=keyboard, disable_web_page_preview=True
        )

    # --- #7 Соц. сети ---
    elif data == "socials":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_LINK)],
            [InlineKeyboardButton("🎵 TikTok", url="https://www.tiktok.com/@good_day_news")],
            [InlineKeyboardButton("📱 Скачать приложение Good Day", url="http://partners.good-day.by/download")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="menu")],
        ])
        await query.message.reply_text(SOCIALS_TEXT, parse_mode="HTML", reply_markup=keyboard)


async def ai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": FESTIVAL_KNOWLEDGE},
                {"role": "user", "content": user_text},
            ],
            max_tokens=300,
            temperature=0.7,
        )
        answer = response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        answer = (
            "😅 Не смог найти ответ. Попробуй переформулировать вопрос "
            "или уточни в Инфоцентре (локация 9)!"
        )
    await update.message.reply_text(answer, reply_markup=back_button())


def main():
    if not BOT_TOKEN:
        raise SystemExit("ОШИБКА: не задан BOT_TOKEN в переменных окружения!")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_response))
    logger.info("🚀 Бот Good Day Полоцк запущен!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
