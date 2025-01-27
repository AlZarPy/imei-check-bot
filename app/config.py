import json

# Токены
TELEGRAM_TOKEN = "7008186343:AAECtYr3TsVTxxDrrLUk_wqBL4fTB3gsOZE" # Для работы введи свой токен бота от BotFather
API_TOKEN = "e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b" #  Указан тестовый токен SandBox
WHITELIST_FILE = "whitelist.json"  # Путь к файлу белого списка

def load_whitelist() -> list[str]:

    # Загружает белый список пользователей из JSON-файла.

    try:
        with open(WHITELIST_FILE, 'r') as file:
            return json.load(file).get('whitelist', [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки белого списка: {e}")
        return []

def is_user_allowed(username: str) -> bool:

    # Проверяет, разрешён ли доступ для указанного username.

    whitelist = load_whitelist()
    return username in whitelist
