import asyncio
from math import lgamma

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import psycopg2
from aiogram.filters import Command
from settings import BOT_TOKEN
from cache import cache

DB_CONFIG = {
    'dbname': 'joyreactor_data',
    'user': 'saitama',
    'password': 'hungry',
    'host': 'postgres',
    'port': '5432'
}

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👍 Хорошие"),
            KeyboardButton(text="🔥 Топ")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    return keyboard

def get_good_pictures():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT img_url, rating
            FROM pictures
            ORDER BY rating DESC        
            """)

        results = cursor.fetchall()
        cursor.close()
        conn.close()

        pictures = []
        for result in results:
            pictures.append(
                {"img_url" : result[0],
                 "rating" : result[1]}
            )
        return pictures
    except Exception as e:
        print(f"Ошибка базы данных: {e}")

def get_best_pictures():
    try:
        cached_data = cache.get("best_pictures")
        if cached_data:
            return cached_data

        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT img_url, rating
            FROM pictures
            WHERE rating > 100
            """)
        results =  cursor.fetchall()
        cursor.close()
        conn.close()

        pictures = []
        for result in results:
            pictures.append({
                "img_url" : result[0],
                "rating" : result[1]
            })
        cache.set("best_pictures", pictures)
        return pictures
    except Exception as e:
        print(f"Ошибка базы данных {e}")
        return []
@dp.message(Command("start"))
async def handle_start(message: types.Message):
    welcome_text = """
    📊 Доступные действия:
    • 👍 Хорошие - картинки с высоким рейтингом
    • 🔥 Топ - только самые популярные (рейтинг > 100)
    """
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@dp.message(Command("menu"))
async def handle_menu(message: types.Message):
    await message.answer("📋 Главное меню:", reply_markup=get_main_keyboard())

@dp.message(lambda message: message.text == "👍 Хорошие")
async def handle_good(message: types.Message):
    pictures = get_good_pictures()

    if not pictures:
        await message.answer("В базе нет картинки")
        return

    for i in range(min(5, len(pictures))):
        await message.answer_photo(photo=pictures[i]["img_url"],reply_markup=get_main_keyboard())
    await asyncio.sleep(0.3)

@dp.message(lambda message: message.text == "🔥 Топ")
async def handle_best(message: types.Message):
    pictures = get_best_pictures()

    if not pictures:
        await message.answer("😔 Нет картинок с рейтингом > 100")
        return

    for i in range(1, len(pictures)):
        await message.answer_photo(photo=pictures[i]["img_url"], reply_markup=get_main_keyboard())
    await asyncio.sleep(0.1)

@dp.message(lambda message: message.text == "Обновить кэш")
async def refresh_cash(message: types.Message):
    cache.delete("best_pictures")
    await message.answer("Кэш обновлён", reply_markup=get_main_keyboard())

@dp.message(Command("help"))
async def handle_help(message: types.Message):
    help_text = """
    🤖 Помощь по боту:
    /start - начать
    /menu - показать клавиатуру
    /help - помощь
    
    Или используй кнопки:
    • 👍 Хорошие - все картинки по рейтингу
    • 🔥 Топ - только лучшие (рейтинг > 100)
    """
    await message.answer(help_text, reply_markup=get_main_keyboard())

@dp.message()
async def handle_other_messages(message: types.Message):
    if message.text not in ["👍 Хорошие", "🔥 Топ"]:
        await message.answer(
            "🤔 Используй кнопки меню или команды:\n"
            "/start - начать\n"
            "/menu - показать кнопки\n"
            "/help - помощь",
            reply_markup=get_main_keyboard()
        )

async def main():
    print("🤖 Бот запущен! Ожидаю сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())