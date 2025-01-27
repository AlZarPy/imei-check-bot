import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_TOKEN, is_user_allowed
from api import check_imei

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()  # Вывод в консоль
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Декоратор для проверки прав пользователя
def user_permission_required(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        username = update.effective_user.username
        if not is_user_allowed(username):
            await update.message.reply_text(f"{username}, у вас нет доступа к этому боту.")
            logger.warning(f"{username} не смог получить доступ к боту")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

# Обработчик команды /start
@user_permission_required
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    await update.message.reply_text(f"Добро пожаловать, {username}! Отправьте IMEI, чтобы проверить его статус.")
    logger.info(f"{username} начал использовать бота")

# Обработчик сообщения для проверки IMEI
@user_permission_required
async def check_imei_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    imei = update.message.text.strip()

    logger.info(f"{username} отправил: {imei}")

    # Проверка длины и формата IMEI
    if len(imei) != 15 or not imei.isdigit():
        await update.message.reply_text("Неверный формат IMEI. Пожалуйста, введите 15 цифр.")
        return

    try:
        result = await check_imei(imei)
        logger.info(f"Результат проверки IMEI: {result}")

        if "error" in result:
            await update.message.reply_text(f"Ошибка: {result['error']}")
        else:
            await update.message.reply_text(
                f"Статус IMEI {imei}:\n" + "\n".join([f"{key}: {value}" for key, value in result.items()]))
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при проверке IMEI: {e}")
        logger.error(f"Ошибка при проверке IMEI: {e}")

# Функция запуска бота
def run_bot() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрация хэдлеров
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_imei_message))

    # Запуск бота
    logger.info("Бот запущен. Нажмите Ctrl+C для остановки.")
    application.run_polling()




