import sys
import os



# ================================= SCRIPT INFO =================================

APP_NAME = "SobesHelper"
SHORT_DESCRIPTION = "Помощник для проведения собеседований"
AUTHOR = "Satoshi White"
AUTHOR_CONTACTS = {"discord": "devmalware", "telegram": "@coder_kiddo"}
VERSION = "1.1.0"



# ================================= FILE PATHS =================================

def get_base_dir() -> str:
    if sys.platform == "win32":
        root = os.environ.get("APPDATA") or os.path.expanduser("~")
    elif sys.platform == "darwin":
        root = os.path.expanduser("~/Library/Application Support")
    else:
        root = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    return os.path.join(root, APP_NAME)

def get_app_dir() -> str:
    if getattr(sys, "frozen", False) or "compiled" in globals():
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_dir()
HISTORY_PATH = os.path.join(BASE_PATH, "journal")
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
os.makedirs(HISTORY_PATH, exist_ok=True)



# ================================= GAME INFO =================================

JOBS = [
    {
        "name": "Шеф ЛСПД",
        "skl": "Шефа ЛСПД",
        "tag": "LSPD [10]"
    },
    {
        "name": "Шеф ЛВПД",
        "skl": "Шефа ЛВПД",
        "tag": "LVPD [10]"
    },
    {
        "name": "Шеф СФПД",
        "skl": "Шефа СФПД",
        "tag": "SFPD [10]"
    },
    {
        "name": "Директор ФБР",
        "skl": "Директора ФБР",
        "tag": "FBI [10]"
    },
    {
        "name": "Начальник ТСР",
        "skl": "Начальника ТСР",
        "tag": "MSP [10]"
    },
    {
        "name": "Адмирал СФа",
        "skl": "Адмирала СФа",
        "tag": "SFa [10]"
    },
    {
        "name": "Генерал Армии ЛС",
        "skl": "Генерала Армии ЛС",
        "tag": "LSa [10]"
    },
    {
        "name": "Глава Пожарного Департамента",
        "skl": "Главу Пожарного Департамента",
        "tag": "DES [10]"
    },
    {
        "name": "Ректор Академии Здравоохранения",
        "skl": "Ректора Академии Здравоохранения",
        "tag": "AMH [10]"
    },
    {
        "name": "Главный Врач Больницы ЛС",
        "skl": "Главного Врача Больницы ЛС",
        "tag": "LSMC [10]"
    },
    {
        "name": "Судья",
        "skl": "Судьи",
        "tag": "Judge"
    },
    {
        "name": "Директор ГЦЛ",
        "skl": "Директора ГЦЛ",
        "tag": "LC [10]"
    },
    {
        "name": "Шеф ЛСПД",
        "skl": "Шефа ЛСПД",
        "tag": "LSPD [10]"
    },
    {
        "name": "Директор Радиоцентра ЛС",
        "skl": "Директора Радиоцентра ЛС",
        "tag": "CNN LS [10]"
    },
    {
        "name": "Глава Грув Стрит",
        "skl": "Главы Грув Стрит",
        "tag": "Groove [10]"
    },
    {
        "name": "Глава Баллас",
        "skl": "Главы Баллас",
        "tag": "Ballas [10]"
    },
    {
        "name": "Глава Рифа",
        "skl": "Главы Рифы",
        "tag": "Rifa [10]"
    },
    {
        "name": "Глава Вагос",
        "skl": "Главы Вагос",
        "tag": "Vagos [10]"
    },
    {
        "name": "Глава Русской Мафии",
        "skl": "Главы Русской Мафии",
        "tag": "RM [10]"
    },
    {
        "name": "Глава Варлок",
        "skl": "Главы Варлок",
        "tag": "WMC [10]"
    }
]

SERVER = "Brainburg" # если переделываете скрипт, можете указать свой сервер



# ================================= COLORS =================================

APP_BACKGROUND = "#F3F4F6" # [NOTE] Добавить смену темы

BLUE = "#3B82F6"
BLUE_HOVER = "#2563EB"

GREEN = "#22C55E"
GREEN_HOVER = "#16A34A"

YELLOW = "#EAB308"
YELLOW_HOVER = "#CA8A04"

RED = "#EF4444"
RED_HOVER = "#DC2626"

GRAY = "#6B7280"
GRAY_HOVER = "#4B5563"



# ================================= PHRASES =================================
# Nothing here yet