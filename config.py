import sys
import os


# ================================= SCRIPT INFO =================================

APP_NAME = "SobesHelper"
SHORT_DESCRIPTION = "Помощник для проведения собеседований"
AUTHOR = "Satoshi White"
AUTHOR_CONTACTS = {"discord": "devmalware", "telegram": "@coder_kiddo"}
VERSION = "1.2.0"
GITHUB_LINK = "https://github.com/treizd/arizona-sobes-helper"
PACKAGES = ["matplotlib"]



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
CONFIG_PATH = os.path.join(BASE_PATH, "config.json")
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

APP_BACKGROUND_LIGHT = "#F3F4F6" 
APP_BACKGROUND_DARK = "#707070"

TEXT_COLOR_LIGHT = "#000000"
TEXT_COLOR_DARK = "#FFFFFF"

BLUE = "#6E87FF"
BLUE_HOVER = "#4A65E0"

GREEN = "#57E67B"
GREEN_HOVER = "#42AD57"

YELLOW = "#E6DE45"
YELLOW_HOVER = "#CCC343"

RED = "#CC4543"
RED_HOVER = "#A13635"

GRAY = "#A8A8A8"
GRAY_HOVER = "#9C9C9C"



# ================================= OTHER =================================

JSON_BASE = {"theme": "light", "font": "Arial"}

LICENSE = f"""MIT License

Copyright (c) 2026 treizd

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

SBORKA = f"python -m nuitka --standalone --onefile --enable-plugin=tk-inter --enable-plugin=matplotlib --windows-icon-from-ico=icon.ico --windows-product-name=\"Sobes Helper\" --windows-company-name=\"Satoshi White\" --windows-file-version=\"{VERSION}.0\" --windows-product-version=\"{VERSION}.0\" --windows-file-description=\"Помощник для проведения собеседований Arizona RP\" --windows-console-mode=disable --include-module=backend --include-module=config --include-package=matplotlib --include-package=matplotlib.font_manager --include-package=numpy --include-package=kiwisolver --include-package=pyparsing --include-package=cycler frontend.py --output-filename=SobesHelper.exe"