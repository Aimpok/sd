from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

# Получаем токен из переменной окружения
TOKEN = os.environ.get('BOT_TOKEN') 

if not TOKEN:
    print("Ошибка: Токен бота не установлен. Убедитесь, что переменная окружения BOT_TOKEN задана.")
    exit()

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Укажите имя файла изображения
IMAGE_FILENAME = 'Welcome.png' 

# *** ВАЖНО: Замените этот URL на URL вашего Mini App, который вы получили с GitHub Pages ***
# Например: "https://your_github_username.github.io/bitly-webapp/"
WEB_APP_URL = "https://aimpok.github.io/bitly-webapp/" 

@dp.message_handler(commands=['start'])
async def send_welcome_with_photo(message: types.Message):
    if not os.path.exists(IMAGE_FILENAME):
        await message.reply(f"Ошибка: Файл изображения '{IMAGE_FILENAME}' не найден в той же директории, что и скрипт бота.")
        return

    # Создаем инлайн-кнопки
    markup = types.InlineKeyboardMarkup()
    
    # Кнопка "Open Bitly" - теперь это Web App кнопка!
    open_bitly_button = types.InlineKeyboardButton("Open Bitly App", web_app=types.WebAppInfo(url="https://aimpok.github.io/bitly/"))
    markup.add(open_bitly_button)
    
    # Кнопка "Bitly News" - остается обычной ссылкой
    bitly_news_button = types.InlineKeyboardButton("Bitly News", url="https://t.me/telegram") 
    markup.add(bitly_news_button)
    
    # Текст сообщения с жирным заголовком
    welcome_caption = """
<b>Welcome to Bitly! 🎯</b>

Trade. Exchange. Grow.
Everything for fast deals and earning points in one place. Your go-to tool for asset operations right here, right now.

Don't waste time. Start farming Blyx and trading while others are just waking up.
Let’s go! 🧤
    """
    
    # Открываем файл изображения в бинарном режиме для отправки
    with open(IMAGE_FILENAME, 'rb') as photo_file:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_file, # Передаем файловый объект
            caption=welcome_caption,
            reply_markup=markup,
            parse_mode=types.ParseMode.HTML 
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
