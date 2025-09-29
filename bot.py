import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from postgres_db.postgresdb import repository
from config import config
from aiogram.filters import Command
from cache import cache
from collections import defaultdict

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()

user_positions = defaultdict(lambda: defaultdict(int))

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👍 Хорошие"),
             KeyboardButton(text="🔥 Топ")],
            [KeyboardButton(text="🔄 Обновить кэш"),
             KeyboardButton(text="Сброс")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_good_pictures():
    try:
        return repository.get_good_pictures()
    except Exception as e:
        print(f"❌ Ошибка получения хороших картинок: {e}")
        return []

def get_best_pictures():
    try:
        cached_data = cache.get("best_pictures")
        if cached_data:
            print("📦 Данные из кэша лучшие")
            return cached_data

        pictures = repository.get_best_pictures()
        cache.set("best_pictures", pictures, 200)
        print("💾 Сохранено в кэш")
        return pictures
    except Exception as e:
        print(f"❌ Ошибка получения лучших картинок: {e}")
        return []

@dp.message(Command("start"))
async def handle_start(message: types.Message):
    welcome_text = """
    📊 Доступные действия:
    • 👍 Хорошие - картинки с высоким рейтингом
    • 🔥 Топ - только самые популярные (рейтинг > 100)
    • Сброс - начать просмотр сначала
    """
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@dp.message(Command("menu"))
async def handle_menu(message: types.Message):
    await message.answer("📋 Главное меню:", reply_markup=get_main_keyboard())

@dp.message(lambda message: message.text == "👍 Хорошие")
async def handle_good(message: types.Message):
    user_id = message.from_user.id
    pictures = get_good_pictures()

    if not pictures:
        await message.answer("В базе нет картинки")
        return

    current_position = user_positions[user_id]["good"]
    start_idx = current_position
    end_idx = start_idx + 5

    if start_idx >= len(pictures):
        user_positions[user_id]["good"] = 0
        start_idx = 0
        end_idx = 5

    sent_count = 0
    for i in range(start_idx, min(end_idx, len(pictures))):
        try:
            reply_markup = get_main_keyboard() if i == min(end_idx, len(pictures)) - 1 else None
            await message.answer_photo(
                photo=pictures[i]["img_url"],
                caption=f"⭐ Рейтинг: {pictures[i]['rating']}\n📊 {i+1}/{len(pictures)}",
                reply_markup=reply_markup
            )
            sent_count += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"❌ Ошибка отправки картинки: {e}")
            continue

    user_positions[user_id]["good"] = end_idx
    if sent_count == 0:
        await message.answer("❌ Не удалось отправить картинки")

@dp.message(lambda message: message.text == "🔥 Топ")
async def handle_best(message: types.Message):
    user_id = message.from_user.id
    pictures = get_best_pictures()

    if not pictures:
        await message.answer("😔 Нет картинок с рейтингом > 100")
        return

    current_position = user_positions[user_id]["best"]
    start_idx = current_position
    end_idx = start_idx + 5

    if start_idx >= len(pictures):
        user_positions[user_id]["best"] = 0
        start_idx = 0
        end_idx = 5

    sent_count = 0
    for i in range(start_idx, min(end_idx, len(pictures))):
        try:
            reply_markup = get_main_keyboard() if i == min(end_idx, len(pictures)) - 1 else None
            await message.answer_photo(
                photo=pictures[i]["img_url"],
                caption=f"🔥 Топ! Рейтинг: {pictures[i]['rating']}",
                reply_markup=reply_markup
            )
            sent_count += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"❌ Ошибка отправки картинки: {e}")
            continue

    user_positions[user_id]["best"] = end_idx
    if sent_count == 0:
        await message.answer("❌ Не удалось отправить картинки")


@dp.message(lambda message: message.text == "🔄 Обновить кэш")
async def refresh_cash(message: types.Message):
    try:
        cache.delete("best_pictures")

        user_id = message.from_user.id
        user_positions[user_id]["good"] = 0
        user_positions[user_id]["best"] = 0
        await message.answer("✅ Кэш обновлён и позиции сброшены!", reply_markup=get_main_keyboard())

    except Exception as e:
        print(f"❌ Ошибка обновления кэша: {e}")
        await message.answer("❌ Ошибка при обновлении кэша", reply_markup=get_main_keyboard())


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

@dp.message(lambda message: message.text == "Сброс")
async def handle_reset(message: types.Message):
    user_id = message.from_user.id
    user_positions[user_id]["good"] = 0
    user_positions[user_id]["best"] = 0
    await message.answer("Позиции просмотра сброшены! Теперь вы начнёте с первых картинок.", reply_markup=get_main_keyboard())


@dp.message()
async def handle_other_messages(message: types.Message):
    if message.text not in ["👍 Хорошие", "🔥 Топ", "🔄 Обновить кэш", "Сброс"]:
        await message.answer(
            "🤔 Используй кнопки меню или команды:",
            reply_markup=get_main_keyboard()
        )

async def main():
    print("🤖 Бот запущен! Ожидаю сообщения...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())