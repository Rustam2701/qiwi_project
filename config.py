import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env в окружение
load_dotenv()

class Config:
    BASE_URL = os.getenv("QIWI_BASE_URL", "https://qiwi.com")
    AGENT_ID = os.getenv("QIWI_AGENT_ID")
    POINT_ID = os.getenv("QIWI_POINT_ID")
    TOKEN = os.getenv("QIWI_TOKEN")

    # Простая проверка, что критически важные данные были загружены
    if not all([AGENT_ID, POINT_ID, TOKEN]):
        raise ValueError("Ошибка: Проверьте, что QIWI_AGENT_ID, QIWI_POINT_ID и QIWI_TOKEN заполнены в файле .env")
