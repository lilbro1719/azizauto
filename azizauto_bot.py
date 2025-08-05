import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token - uses environment variable for production, fallback for local testing
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8133311727:AAHLsIyxz6cnUbSxYmUxXpfShd6OA9QMi1o')

# Car inventory (prices converted to RUB)
CARS = {
    'suvs': [
        {'name': 'Toyota RAV4', 'price': '2,800,000 ₽', 'year': '2023'},
        {'name': 'Honda CR-V', 'price': '3,200,000 ₽', 'year': '2023'},
        {'name': 'Mazda CX-5', 'price': '3,000,000 ₽', 'year': '2022'}
    ],
    'sedans': [
        {'name': 'Toyota Camry', 'price': '2,500,000 ₽', 'year': '2023'},
        {'name': 'Honda Accord', 'price': '2,700,000 ₽', 'year': '2023'},
        {'name': 'Nissan Altima', 'price': '2,400,000 ₽', 'year': '2022'}
    ],
    'sports': [
        {'name': 'BMW M3', 'price': '6,500,000 ₽', 'year': '2023'},
        {'name': 'Audi RS5', 'price': '7,500,000 ₽', 'year': '2023'}
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send main menu when /start command is issued."""
    keyboard = [
        [InlineKeyboardButton("🔍 Просмотр автомобилей", callback_data='browse')],
        [InlineKeyboardButton("💰 Получить расчет", callback_data='quote')],
        [InlineKeyboardButton("📞 Связаться с нами", callback_data='contact')],
        [InlineKeyboardButton("ℹ️ О нас", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🚗 *Добро пожаловать в AzizAuto!*\n\n"
        "Ваш надежный автодилер. У нас широкий выбор качественных автомобилей.\n"
        "Что бы вы хотели сделать сегодня?"
    )
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'browse':
        await show_categories(query)
    elif query.data == 'quote':
        await show_quote_options(query)
    elif query.data == 'contact':
        await show_contact(query)
    elif query.data == 'about':
        await show_about(query)
    elif query.data == 'back_main':
        await show_main_menu(query)
    elif query.data in ['suvs', 'sedans', 'sports']:
        await show_cars(query, query.data)
    elif query.data.startswith('car_'):
        await show_car_details(query)
    elif query.data.startswith('budget_'):
        await handle_budget(query)

async def show_categories(query) -> None:
    """Show car categories."""
    keyboard = [
        [InlineKeyboardButton("🚙 Внедорожники (3 доступно)", callback_data='suvs')],
        [InlineKeyboardButton("🚗 Седаны (3 доступно)", callback_data='sedans')],
        [InlineKeyboardButton("🏎️ Спорткары (2 доступно)", callback_data='sports')],
        [InlineKeyboardButton("🔙 Назад в главное меню", callback_data='back_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🔍 *Просмотр наших автомобилей*\n\nВыберите категорию для просмотра доступных машин:"
    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)

async def show_cars(query, category) -> None:
    """Show cars in selected category."""
    category_names = {'suvs': 'Внедорожники', 'sedans': 'Седаны', 'sports': 'Спорткары'}
    cars = CARS[category]
    
    keyboard = []
    for i, car in enumerate(cars):
        button_text = f"{car['name']} - {car['price']}"
        callback_data = f"car_{category}_{i}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад к категориям", callback_data='browse')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"🚗 *{category_names[category]}*\n\nВыберите автомобиль для подробной информации:"
    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)

async def show_car_details(query) -> None:
    """Show detailed car information."""
    # Parse callback data: car_category_index
    _, category, index = query.data.split('_')
    car = CARS[category][int(index)]
    
    keyboard = [
        [InlineKeyboardButton("📋 Полные характеристики", callback_data=f"specs_{category}_{index}")],
        [InlineKeyboardButton("📅 Записаться на тест-драйв", callback_data=f"testdrive_{category}_{index}")],
        [InlineKeyboardButton("💬 Связаться с отделом продаж", callback_data='contact')],
        [InlineKeyboardButton("🔙 Назад к автомобилям", callback_data=category)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        f"🚗 *{car['name']}*\n\n"
        f"💰 Цена: {car['price']}\n"
        f"📅 Год: {car['year']}\n"
        f"✅ Доступен сейчас\n\n"
        f"Отличный выбор! Это одна из наших самых популярных моделей."
    )
    
    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)

async def show_quote_options(query) -> None:
    """Show budget options for quote."""
    keyboard = [
        [InlineKeyboardButton("💵 До 2 млн ₽", callback_data='budget_under20')],
        [InlineKeyboardButton("💰 2-4 млн ₽", callback_data='budget_20to40')],
        [InlineKeyboardButton("💎 Свыше 4 млн ₽", callback_data='budget_above40')],
        [InlineKeyboardButton("🔙 Назад в главное меню", callback_data='back_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "💰 *Получить персональный расчет*\n\nКакой у вас бюджет?"
    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_budget(query) -> None:
    """Handle budget selection."""
    budget_responses = {
        'budget_under20': "Отлично! У нас есть несколько качественных подержанных автомобилей до 2 млн ₽. Наш отдел продаж свяжется с вами с лучшими вариантами в течение 24 часов.",
        'budget_20to40': "Превосходный диапазон! Это покрывает большинство наших популярных седанов и внедорожников. Вы получите наш премиальный список в ближайшее время.",
        'budget_above40': "Отлично! У вас будет доступ к нашей коллекции люксовых и спортивных автомобилей. Специалист свяжется с вами для обсуждения эксклюзивных вариантов."
    }
    
    keyboard = [
        [InlineKeyboardButton("📞 Позвонить мне сейчас", callback_data='contact')],
        [InlineKeyboardButton("🔙 Назад в главное меню", callback_data='back_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(budget_responses[query.data], reply_markup=reply_markup)

async def show_contact(query) -> None:
    """Show contact information."""
    keyboard = [[InlineKeyboardButton("🔙 Назад в главное меню", callback_data='back_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "📞 *Связаться с AzizAuto*\n\n"
        "📱 Телефон: +7 (xxx) xxx-xx-xx\n"
        "📧 Email: sales@azizauto.com\n"
        "📍 Адрес: ул. Автомобильная, 123, г. Автоград\n"
        "🕒 Часы работы: Пн-Сб 9:00-19:00\n\n"
        "Наш отдел продаж готов помочь вам найти идеальный автомобиль!"
    )
    
    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)

async def show_about(query) -> None:
    """Show about information."""
    keyboard = [[InlineKeyboardButton("🔙 Назад в главное меню", callback_data='back_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "ℹ️ *О компании AzizAuto*\n\n"
        "🏆 Надежный автодилер с 2010 года\n"
        "✅ Более 1000+ довольных клиентов\n"
        "🔧 Полное обслуживание и гарантия\n"
        "💯 Гарантированно качественные автомобили\n\n"
        "Мы стремимся помочь вам найти идеальный автомобиль по лучшей цене!"
    )
    
    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)

async def show_main_menu(query) -> None:
    """Return to main menu."""
    keyboard = [
        [InlineKeyboardButton("🔍 Просмотр автомобилей", callback_data='browse')],
        [InlineKeyboardButton("💰 Получить расчет", callback_data='quote')],
        [InlineKeyboardButton("📞 Связаться с нами", callback_data='contact')],
        [InlineKeyboardButton("ℹ️ О нас", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🚗 *Добро пожаловать в AzizAuto!*\n\n"
        "Ваш надежный автодилер. У нас широкий выбор качественных автомобилей.\n"
        "Что бы вы хотели сделать сегодня?"
    )
    
    await query.edit_message_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot
    print("Bot is starting...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
