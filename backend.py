import os
import pip
import json
import random
import string
import datetime
import matplotlib.font_manager as fm
import importlib.util as iu

from config import HISTORY_PATH, JOBS, CONFIG_PATH, JSON_BASE, PACKAGES



# ================================= QUESTIONS =================================

def load_questions(
        path: str
        ) -> list | None:
    if not path or not os.path.exists(path) or not path.endswith(".txt"):
        return

    with open(path, "r", encoding="utf-8") as file:
        return [question.rstrip("\n") for question in file.readlines()]


def distribute_questions(
        file_path: str
        ) -> bool | None:
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    questions = load_questions(data["questions_file"])
    tq = []

    for person in data["participants"]:
        if data["same_questions"]:
            if len(tq) == 0:
                tq = random.sample(questions, k=min(len(questions), data["questions_to_ask_count"]))
            person_questions = tq.copy()
        else:
            person_questions = random.sample(questions, k=min(len(questions), data["questions_to_ask_count"]))

        if data["shuffle_questions"]:
            random.shuffle(person_questions)

        data["answers"].append({
            "name": person,
            "points": {},
            "questions": person_questions,
            "is_checked": False,
            "question_state": 0
        })

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)



# ================================= FILES =================================

def create_sobes(
        custom_name: str, 
        questions_to_ask_count: int, 
        same_questions: bool, 
        shuffle_questions: bool, 
        question_file: str, 
        nicknames: list, 
        time_per_question: int, 
        job: str
        ) -> str:
    os.makedirs(HISTORY_PATH, exist_ok=True)

    file_name = "".join([random.choice(string.ascii_letters + string.digits) for _ in range(8)]) + ".json"
    job_data = get_job(job)

    dump_data = {
        "short_name": custom_name,
        "date": datetime.datetime.now().strftime("%d.%m.%Y"),
        "time": datetime.datetime.now().strftime("%H:%M"),
        "job": job_data["tag"],
        "job_name": job_data["name"],
        "job_skl": job_data["skl"],
        "participants": nicknames,
        "questions_file": question_file,
        "questions_to_ask_count": questions_to_ask_count,
        "same_questions": same_questions,
        "shuffle_questions": shuffle_questions,
        "time_per_question": time_per_question,
        "answers": [],
        "marked_ended": False
    }

    file_path = os.path.join(HISTORY_PATH, file_name)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(dump_data, file, ensure_ascii=False, indent=4)

    return file_path


def get_history_files() -> list:
    os.makedirs(HISTORY_PATH, exist_ok=True)

    files = []

    for file_name in os.listdir(HISTORY_PATH):
        file_path = os.path.join(HISTORY_PATH, file_name)

        if os.path.isfile(file_path) and file_name.endswith(".json"):
            files.append(file_path)

    return sorted(files, key=os.path.getmtime, reverse=True)


def load_data(
        file_path: str
        ) -> dict | bool:
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for participant in data.get("answers", []):
        if not isinstance(participant.get("points"), dict):
            participant["points"] = {}

    return data


def save_data(
        file_path: str, 
        data: dict
        ) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        print("Could not find config.json")
        with open(CONFIG_PATH, "w", encoding="utf-8") as file:
            json.dump(JSON_BASE, file)

        return JSON_BASE

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = json.load(file)

    return config



# ================================= OTHER =================================

def get_job(
        job: str
        ) -> dict:
    for job_data in JOBS:
        if job_data["name"] == job or job_data["tag"] == job:
            return job_data

    return {
        "name": job,
        "skl": job,
        "tag": job
    }


def get_total_points(
        participant: dict
        ) -> float:
    return sum([float(points) for points in participant.get("points", {}).values()])


def get_sorted_participants(
        data: dict
        ) -> list:
    return sorted(
        data["answers"],
        key=lambda participant: (
            not participant.get("is_checked", False),
            -get_total_points(participant),
            participant.get("name", "").lower()
        )
    )


def change_theme(
        new_theme: str
        ) -> None:
    config = load_config()
    config["theme"] = new_theme

    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file)

def change_font(
        target_font: str
        ) -> None:
    config = load_config()
    config["font"] = target_font

    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file)


def get_available_fonts() -> list:
    font_names = fm.get_font_names() # пути к шрифтам: font_paths = fm.findSystemFonts()
    return sorted(font_names)