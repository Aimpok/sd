from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

# Получаем токен из переменной окружения
TOKEN = os.environ.get('BOT_TOKEN') # Теперь токен будет браться из переменной окружения BOT_TOKEN

if not TOKEN:
    print("Ошибка: Токен бота не установлен. Убедитесь, что переменная окружения BOT_TOKEN задана.")
    exit()

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Укажите имя файла изображения, который должен находиться в той же папке, что и ваш скрипт Python
IMAGE_FILENAME = 'Welcome.png' 

@dp.message_handler(commands=['start'])
async def send_welcome_with_photo(message: types.Message):
    if not os.path.exists(IMAGE_FILENAME):
        await message.reply(f"Ошибка: Файл изображения '{IMAGE_FILENAME}' не найден в той же директории, что и скрипт бота.")
        return

    markup = types.InlineKeyboardMarkup()
    open_bitly_button = types.InlineKeyboardButton("Open Bitly", url="https://t.me/telegram/telegram_apps_platform") 
    markup.add(open_bitly_button)
    bitly_news_button = types.InlineKeyboardButton("Bitly News", url="https://t.me/telegram") 
    markup.add(bitly_news_button)
    
    welcome_caption = """
<b>Welcome to Bitly! 🎯</b>

Trade. Exchange. Grow.
Everything for fast deals and earning points in one place. Your go-to tool for asset operations right here, right now.

Don't waste time. Start farming Blyx and trading while others are just waking up.
Let’s go! 🧤
    """
    
    with open(IMAGE_FILENAME, 'rb') as photo_file:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_file,
            caption=welcome_caption,
            reply_markup=markup,
            parse_mode=types.ParseMode.HTML 
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)