import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from postgres_db.postgresdb import repository
from config import config
from aiogram.filters import Command
from cache import cache

config.DB_CONFIG()

bot = Bot(config.BOT_TOKEN)

dp = Dispatcher()

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👍 Хорошие"),
             KeyboardButton(text="🔥 Топ")],
            [KeyboardButton(text="🔄 Обновить кэш")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_good_pictures():
        repository.get_good_pictures()


def get_best_pictures():
        cached_data = cache.get("best_pictures")
        if cached_data:
            return cached_data
        repository.get_best_pictures()
        cache.set("best_pictures", repository.get_best_pictures())

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
        reply_markup = get_main_keyboard() if i == 4 else None
        await message.answer_photo(
            photo=pictures[i]["img_url"],
            caption=f"⭐ Рейтинг: {pictures[i]['rating']}",
            reply_markup=reply_markup
        )
    await asyncio.sleep(0.3)

@dp.message(lambda message: message.text == "🔥 Топ")
async def handle_best(message: types.Message):
    pictures = get_best_pictures()

    if not pictures:
        await message.answer("😔 Нет картинок с рейтингом > 100")
        return

    for i in range(min(5, len(pictures))):

        reply_markup = get_main_keyboard() if i == 4 else None
        await message.answer_photo(
            photo=pictures[i]["img_url"],
            caption=f"🔥 Топ! Рейтинг: {pictures[i]['rating']}",
            reply_markup=reply_markup
        )
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
    if message.text not in ["👍 Хорошие", "🔥 Топ", "🔄 Обновить кэш"]:
        await message.answer(
            "🤔 Используй кнопки меню или команды:",
            reply_markup=get_main_keyboard()
        )

async def main():
    print("🤖 Бот запущен! Ожидаю сообщения...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())