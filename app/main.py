import logging
from bot import run_bot

# Настройка логирования
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def main():
    try:
        run_bot()
    except Exception as e:
        logger.error(f"Произошла ошибка при запуске бота: {e}")

if __name__ == "__main__":
    main()
