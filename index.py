import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiohttp import web

# Настройка логирования
logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get('BOT_TOKEN')
# URL вашего приложения на Vercel (вы получите его после первого деплоя)
# Например: https://my-bot-name.vercel.app
WEBHOOK_HOST = os.environ.get('WEBHOOK_HOST') 
WEBHOOK_PATH = f'/api/index.py'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

IMAGE_FILENAME = 'Welcome.png' 
WEB_APP_URL = "https://aimpok.github.io/bitly-webapp/" 

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome_with_photo(message: types.Message):
    # В Vercel файлы лежат в корне проекта
    image_path = os.path.join(os.getcwd(), IMAGE_FILENAME)
    
    if not os.path.exists(image_path):
        await message.reply(f"Ошибка: Файл {IMAGE_FILENAME} не найден.")
        return

    markup = types.InlineKeyboardMarkup()
    # Обратите внимание: URL в web_app должен быть актуальным
    markup.add(types.InlineKeyboardButton("Open Bitly App", web_app=types.WebAppInfo(url="https://aimpok.github.io/bitly/")))
    markup.add(types.InlineKeyboardButton("Bitly News", url="https://t.me/telegram"))
    
    welcome_caption = """
<b>Welcome to Bitly! 🎯</b>

Trade. Exchange. Grow.
Everything for fast deals and earning points in one place. Your go-to tool for asset operations right here, right now.

Don't waste time. Start farming Blyx and trading while others are just waking up.
Let’s go! 🧤
    """
    
    with open(image_path, 'rb') as photo_file:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_file,
            caption=welcome_caption,
            reply_markup=markup,
            parse_mode=types.ParseMode.HTML 
        )

# Обработчик для Vercel (Serverless функция)
async def handler(request):
    if request.method == 'POST':
        # Получаем обновление от Telegram
        data = await request.json()
        update = Update.to_object(data)
        
        # Устанавливаем текущий контекст бота (важно для aiogram 2.x)
        Bot.set_current(bot)
        Dispatcher.set_current(dp)
        
        await dp.process_update(update)
        return web.Response(text='ok')
    else:
        # При GET запросе (например, открытие в браузере) пробуем установить вебхук
        if WEBHOOK_HOST:
            await bot.set_webhook(WEBHOOK_URL)
            return web.Response(text=f"Webhook set to {WEBHOOK_URL}")
        else:
            return web.Response(text="WEBHOOK_HOST not set")

# Vercel требует, чтобы приложение экспортировало асинхронную функцию
app = web.Application()
app.router.add_post('/api/index.py', handler)
app.router.add_get('/api/index.py', handler)
