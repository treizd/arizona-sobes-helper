# Frontend: treizd and his anonymous partner (GUI styling: AI)
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from config import APP_BACKGROUND, BLUE, BLUE_HOVER, GRAY, GRAY_HOVER, GREEN, GREEN_HOVER, RED, RED_HOVER, YELLOW, YELLOW_HOVER, DESKTOP_PATH, SERVER, JOBS, AUTHOR, AUTHOR_CONTACTS, VERSION, APP_NAME, SHORT_DESCRIPTION
from backend import load_questions, distribute_questions, create_sobes, load_data, save_data, get_sorted_participants, get_total_points, get_job, get_history_files



# ================================= [AI] CUSTOM BUTTON CLASS =================================

class RoundedButton(tk.Canvas):
    def __init__(
        self,
        parent,
        text,
        command=None,
        color=BLUE,
        hover_color=BLUE_HOVER,
        text_color="white",
        radius=12,
        height=42,
        width=180,
        button_font=("Arial", 11, "bold")
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            background=APP_BACKGROUND,
            highlightthickness=0,
            borderwidth=0,
            relief="flat",
            cursor="hand2"
        )

        self.command = command
        self.button_text = text
        self.normal_color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.radius = radius
        self.button_font = button_font

        self.button_state = "normal"
        self.hovered = False

        self.bind("<Configure>", self._redraw)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

        self._draw()

    def _rounded_rectangle(
        self,
        x1,
        y1,
        x2,
        y2,
        radius,
        **kwargs
    ):
        radius = min(
            radius,
            (x2 - x1) / 2,
            (y2 - y1) / 2
        )

        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]

        self.create_polygon(
            points,
            smooth=True,
            splinesteps=36,
            **kwargs
        )

    def _draw(self):
        self.delete("all")

        width = max(self.winfo_width(), 2)
        height = max(self.winfo_height(), 2)

        if self.button_state == "disabled":
            background = "#D1D5DB"
            foreground = "#9CA3AF"
        else:
            background = (
                self.hover_color
                if self.hovered
                else self.normal_color
            )
            foreground = self.text_color

        self._rounded_rectangle(
            1,
            1,
            width - 1,
            height - 1,
            self.radius,
            fill=background,
            outline=""
        )

        self.create_text(
            width / 2,
            height / 2,
            text=self.button_text,
            fill=foreground,
            font=self.button_font
        )

    def _redraw(self, _event=None):
        self._draw()

    def _on_enter(self, _event=None):
        if self.button_state != "disabled":
            self.hovered = True
            self._draw()

    def _on_leave(self, _event=None):
        self.hovered = False
        self._draw()

    def _on_click(self, _event=None):
        if self.button_state != "disabled" and self.command:
            self.command()

    def set_state(self, state):
        self.button_state = state

        if state == "disabled":
            self.configure(cursor="arrow")
        else:
            self.configure(cursor="hand2")

        self._draw()

    def set_text(self, text):
        self.button_text = text
        self._draw()


def create_title(
        parent,
        text=APP_NAME
        ):
    label = ttk.Label(
        parent,
        text=text,
        style="Title.TLabel"
    )
    label.pack(pady=(10, 15))
    return label


def create_back_button(
        parent, 
        text, 
        command
        ):
    button = RoundedButton(
        parent,
        text=text,
        command=command,
        color=GRAY,
        hover_color=GRAY_HOVER,
        width=170,
        height=36,
        radius=10,
        button_font=("Arial", 10, "bold")
    )
    button.pack(anchor="nw", padx=10, pady=10)
    return button

# [NOTE] Стилизация от ИИ
def start():
    global root, timer_after

    root = tk.Tk()
    root.title(f"{APP_NAME} [v{VERSION}]")
    root.resizable(False, False)
    root.configure(background=APP_BACKGROUND)

    timer_after = None

    width = 700
    height = 600

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    root.geometry(f"{width}x{height}+{x}+{y}")

    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        "TFrame",
        background=APP_BACKGROUND
    )

    style.configure(
        "TLabel",
        background=APP_BACKGROUND,
        foreground="#111827",
        font=("Arial", 10)
    )

    style.configure(
        "Title.TLabel",
        background=APP_BACKGROUND,
        foreground="#111827",
        font=("Arial", 24, "bold")
    )

    style.configure(
        "Subtitle.TLabel",
        background=APP_BACKGROUND,
        foreground="#111827",
        font=("Arial", 14, "bold")
    )

    style.configure(
        "TEntry",
        fieldbackground="white",
        foreground="#111827",
        padding=7,
        borderwidth=1,
        relief="flat"
    )

    style.configure(
        "TCombobox",
        fieldbackground="white",
        foreground="#111827",
        padding=6
    )

    style.configure(
        "TSpinbox",
        fieldbackground="white",
        foreground="#111827",
        padding=5
    )


def clear_page():
    global timer_after

    if timer_after is not None:
        try:
            root.after_cancel(timer_after)
        except Exception:
            pass

        timer_after = None

    for widget in root.winfo_children():
        widget.destroy()

# [NOTE] .txt только пока что, в планах добавить .json
def select_file():
    global question_file

    file_path = filedialog.askopenfilename(
        title="Выберите файл",
        initialdir=DESKTOP_PATH,
        filetypes=[
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
    )

    if not file_path:
        question_file = None
        chosen_label.config(text="❌ Файл не выбран")
        return None

    questions = load_questions(file_path)

    if questions is None:
        question_file = None
        chosen_label.config(text="❌ Не удалось загрузить файл")
        return None

    question_file = file_path

    chosen_label.config(
        text=f"✅ Выбран файл: {file_path}\nВопросов: {len(questions)}"
    )

    return file_path


def main_page():
    clear_page()

    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    create_title(frame)

    subtitle = ttk.Label(
        frame,
        text=SHORT_DESCRIPTION,
        font=("Arial", 11),
        foreground="#6B7280"
    )
    subtitle.pack(pady=(0, 25))

    create_button = RoundedButton(
        frame,
        text="▶ Создать собеседование",
        command=sobes_creation_page,
        color=BLUE,
        hover_color=BLUE_HOVER,
        width=280,
        height=48,
        radius=14
    )
    create_button.pack(pady=7)

    history_button = RoundedButton(
        frame,
        text="🕒 История собеседований",
        command=history_page,
        color=GRAY,
        hover_color=GRAY_HOVER,
        width=280,
        height=48,
        radius=14
    )
    history_button.pack(pady=7)

    debug_button = RoundedButton(
            frame,
            text="🐞 Баги/предложения",
            command=bugs_and_adv,
            color=YELLOW,
            hover_color=YELLOW_HOVER,
            width=280,
            height=48,
            radius=14
        )
    debug_button.pack(pady=7)

    author_label = ttk.Label(
        frame,
        text=f"© {AUTHOR}", # ток попробуйте поменять автора в конфиге!
        font=("Arial", 10),
        foreground="#6B7280"
    )
    author_label.pack(side="bottom", pady=20)


def sobes_creation_page():
    global chosen_label
    global custom_entry
    global job_box
    global nicks_entry
    global count_box
    global same_box
    global shuffle_box
    global time_box
    global question_file

    clear_page()
    question_file = None

    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    create_back_button(
        frame,
        "◀ Домой",
        main_page
    )

    title = ttk.Label(
        frame,
        text="Новое собеседование",
        style="Title.TLabel"
    )
    title.pack(pady=(0, 12))

    form = ttk.Frame(frame)
    form.pack(fill="both", expand=True, padx=45)

    ttk.Label(
        form,
        text="Название собеседования:"
    ).pack(anchor="w", pady=(0, 3))

    custom_entry = ttk.Entry(form)
    custom_entry.pack(fill="x", pady=(0, 8))

    ttk.Label(
        form,
        text="Собеседование на должность:"
    ).pack(anchor="w", pady=(0, 3))

    job_box = ttk.Combobox(
        form,
        values=[job["name"] for job in JOBS],
        state="readonly"
    )
    job_box.pack(fill="x", pady=(0, 8))

    ttk.Label(
        form,
        text="Ники участников (каждый с новой строки):"
    ).pack(anchor="w", pady=(0, 3))

    nicks_entry = scrolledtext.ScrolledText(
        form,
        wrap=tk.WORD,
        width=50,
        height=5,
        font=("Arial", 10),
        relief="flat",
        borderwidth=1,
        highlightthickness=1,
        highlightbackground="#D1D5DB",
        highlightcolor=BLUE
    )
    nicks_entry.pack(fill="x", pady=(0, 8))

    file_row = ttk.Frame(form)
    file_row.pack(fill="x", pady=3)

    file_button = RoundedButton(
        file_row,
        text="Выбрать файл вопросов",
        command=select_file,
        color=GRAY,
        hover_color=GRAY_HOVER,
        width=220,
        height=36,
        radius=10,
        button_font=("Arial", 10, "bold")
    )
    file_button.pack(side="left")

    chosen_label = ttk.Label(
        form,
        text="❌ Файл не выбран",
        foreground="#6B7280",
        wraplength=590
    )
    chosen_label.pack(anchor="w", pady=(3, 8))

    options_frame = ttk.Frame(form)
    options_frame.pack(fill="x", pady=2)

    ttk.Label(
        options_frame,
        text="Вопросов:"
    ).grid(row=0, column=0, padx=(0, 5), sticky="w")

    count_box = ttk.Spinbox(
        options_frame,
        from_=1,
        to=1000,
        width=6
    )
    count_box.set(1)
    count_box.grid(row=0, column=1, padx=(0, 18))

    ttk.Label(
        options_frame,
        text="Одинаковые:"
    ).grid(row=0, column=2, padx=(0, 5))

    same_box = ttk.Combobox(
        options_frame,
        values=["Да", "Нет"],
        state="readonly",
        width=7
    )
    same_box.set("Да")
    same_box.grid(row=0, column=3, padx=(0, 18))

    ttk.Label(
        options_frame,
        text="Перемешивать:"
    ).grid(row=0, column=4, padx=(0, 5))

    shuffle_box = ttk.Combobox(
        options_frame,
        values=["Да", "Нет"],
        state="readonly",
        width=7
    )
    shuffle_box.set("Нет")
    shuffle_box.grid(row=0, column=5)

    time_frame = ttk.Frame(form)
    time_frame.pack(fill="x", pady=(8, 4))

    ttk.Label(
        time_frame,
        text="Секунд на вопрос (0 – без таймера):"
    ).pack(side="left")

    time_box = ttk.Spinbox(
        time_frame,
        from_=0,
        to=3600,
        width=7
    )
    time_box.set(0)
    time_box.pack(side="left", padx=8)

    start_button = RoundedButton(
        form,
        text="▶ Начать собеседование",
        command=create_sobes_from_form,
        color=GREEN,
        hover_color=GREEN_HOVER,
        width=270,
        height=44,
        radius=13
    )
    start_button.pack(pady=12)

# [NOTE] Валидатор данных тут
def create_sobes_from_form():
    nicknames = [
        nickname.strip()
        for nickname in nicks_entry.get("1.0", "end").splitlines()
        if nickname.strip()
    ]

    if not custom_entry.get().strip():
        messagebox.showerror(
            "Ошибка",
            "Введите название собеседования"
        )
        return

    if not job_box.get():
        messagebox.showerror(
            "Ошибка",
            "Выберите должность"
        )
        return

    if not nicknames:
        messagebox.showerror(
            "Ошибка",
            "Введите хотя бы одного кандидата"
        )
        return

    if not question_file:
        messagebox.showerror(
            "Ошибка",
            "Выберите файл с вопросами"
        )
        return

    questions = load_questions(question_file)

    if not questions:
        messagebox.showerror(
            "Ошибка",
            "В файле нет вопросов"
        )
        return

    try:
        questions_count = int(count_box.get())
        time_per_question = int(time_box.get())
    except ValueError:
        messagebox.showerror(
            "Ошибка",
            "Введите корректные числовые значения"
        )
        return

    if questions_count > len(questions):
        messagebox.showerror(
            "Ошибка",
            "Количество вопросов больше количества строк в файле"
        )
        return

    sobes_file = create_sobes(
        custom_entry.get().strip(),
        questions_count,
        same_box.get() == "Да",
        shuffle_box.get() == "Да",
        question_file,
        nicknames,
        time_per_question,
        job_box.get()
    )

    distribute_questions(sobes_file)
    candidates_page(sobes_file, False)


def candidates_page(file_path, from_history=False):
    clear_page()

    data = load_data(file_path)

    if not data:
        messagebox.showerror(
            "Ошибка",
            "Файл собеседования не найден"
        )
        main_page()
        return

    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    back_command = history_page if from_history else main_page

    create_back_button(
        frame,
        "◀ Назад",
        back_command
    )

    create_title(frame)

    sobes_label = ttk.Label(
        frame,
        text=f"{data.get('short_name', '')} | {data.get('job', '')}",
        style="Subtitle.TLabel"
    )
    sobes_label.pack(pady=(0, 10))

    candidates_label = ttk.Label(
        frame,
        text="Кандидаты:",
        font=("Arial", 11, "bold")
    )
    candidates_label.pack(pady=5)

    candidates_frame = ttk.Frame(frame)
    candidates_frame.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=5
    )

    for participant in get_sorted_participants(data):
        state = participant.get("question_state", 0)
        is_checked = participant.get("is_checked", False)
        total_points = get_total_points(participant)

        if state == -1 and is_checked:
            status = "Завершен"
            color = GREEN
            hover_color = GREEN_HOVER

        elif state > 0:
            status = f"Вопрос №{state}"
            color = YELLOW
            hover_color = YELLOW_HOVER

        else:
            status = "Не начато"
            color = RED
            hover_color = RED_HOVER

        if state == 0 and not is_checked:
            open_command = (
                lambda participant_name=participant.get("name"):
                candidate_intro_page(
                    file_path,
                    participant_name,
                    from_history
                )
            )
        else:
            open_command = (
                lambda participant_name=participant.get("name"):
                question_page(
                    file_path,
                    participant_name,
                    None,
                    from_history
                )
            )

        candidate_button = RoundedButton(
            candidates_frame,
            text=f"{participant.get('name')}  •  {status}  •  {total_points:g} баллов",
            command=open_command,
            color=color,
            hover_color=hover_color,
            width=600,
            height=44,
            radius=13
        )
        candidate_button.pack(fill="x", pady=4)


def candidate_intro_page(
    file_path,
    participant_name,
    from_history=False
):
    clear_page()

    data = load_data(file_path)

    if not data:
        candidates_page(file_path, from_history)
        return

    participant = next(
        (
            answer
            for answer in data["answers"]
            if answer["name"] == participant_name
        ),
        None
    )

    if participant is None:
        candidates_page(file_path, from_history)
        return

    if (
        participant.get("is_checked", False)
        or participant.get("question_state", 0) == -1
    ):
        question_page(
            file_path,
            participant_name,
            None,
            from_history
        )
        return

    job_skl = data.get("job_skl")

    if not job_skl:
        job_skl = get_job(data.get("job", ""))["skl"]

    questions_count = len(participant.get("questions", []))
    time_per_question = int(data.get("time_per_question", 0))

    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    create_back_button(
        frame,
        "◀ К кандидатам",
        lambda: candidates_page(file_path, from_history)
    )

    create_title(frame)

    candidate_label = ttk.Label(
        frame,
        text=f"Кандидат: {participant_name}",
        style="Subtitle.TLabel"
    )
    candidate_label.pack(pady=5)

    greeting_text = f"Приветствую, кандидат. Вы попали на обзвон на должность {job_skl} штата {SERVER}. Представьтесь, расскажите о себе."

    greeting_label = ttk.Label(
        frame,
        text=greeting_text,
        font=("Arial", 13),
        wraplength=620,
        justify="center"
    )
    greeting_label.pack(padx=30, pady=(20, 8))

    wait_label = ttk.Label(
        frame,
        text="ОЖИДАЙТЕ ПРЕДСТАВЛЕНИЯ",
        font=("Arial", 13, "bold"),
        foreground=RED
    )
    wait_label.pack(pady=12)

    if time_per_question == 0:
        time_text = "без ограничения времени"
    else:
        time_text = f"не более {time_per_question} секунд"

    questions_text = f"Сейчас вам будут заданы тестовые вопросы в количестве {questions_count} штук. На каждый ответ дается {time_text}.\n\nОценивание: 1 балл – верный ответ, 0.5 – частично верный, 0 – неверный. Вы готовы?"


    questions_label = ttk.Label(
        frame,
        text=questions_text,
        font=("Arial", 12),
        wraplength=620,
        justify="center"
    )
    questions_label.pack(padx=30, pady=15)

    start_button = RoundedButton(
        frame,
        text="Приступить к вопросам",
        command=lambda: question_page(
            file_path,
            participant_name,
            1,
            from_history
        ),
        color=GREEN,
        hover_color=GREEN_HOVER,
        width=260,
        height=46,
        radius=14
    )
    start_button.pack(pady=15)


def question_page(
    file_path,
    participant_name,
    shown_question=None,
    from_history=False
):
    clear_page()

    data = load_data(file_path)

    if not data:
        candidates_page(file_path, from_history)
        return

    participant = next(
        (
            answer
            for answer in data["answers"]
            if answer["name"] == participant_name
        ),
        None
    )

    if participant is None or not participant.get("questions"):
        candidates_page(file_path, from_history)
        return

    if participant.get("question_state", 0) == 0:
        participant["question_state"] = 1
        save_data(file_path, data)

    if shown_question is None:
        if participant.get("question_state") == -1:
            shown_question = len(participant["questions"])
        else:
            shown_question = participant["question_state"]

    shown_question = max(
        1,
        min(
            shown_question,
            len(participant["questions"])
        )
    )

    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    top_frame = ttk.Frame(frame)
    top_frame.pack(fill="x", padx=10, pady=10)

    back_button = RoundedButton(
        top_frame,
        text="◀ К кандидатам",
        command=lambda: candidates_page(
            file_path,
            from_history
        ),
        color=GRAY,
        hover_color=GRAY_HOVER,
        width=170,
        height=36,
        radius=10,
        button_font=("Arial", 10, "bold")
    )
    back_button.pack(side="left")

    if (
        shown_question == 1
        and not participant.get("is_checked", False)
        and participant.get("question_state") != -1
    ):
        intro_button = RoundedButton(
            top_frame,
            text="◀ К памятке",
            command=lambda: candidate_intro_page(
                file_path,
                participant_name,
                from_history
            ),
            color=BLUE,
            hover_color=BLUE_HOVER,
            width=150,
            height=36,
            radius=10,
            button_font=("Arial", 10, "bold")
        )
        intro_button.pack(side="left", padx=8)

    create_title(frame)

    job_skl = data.get("job_skl")

    if not job_skl:
        job_skl = get_job(data.get("job", ""))["skl"]

    job_label = ttk.Label(
        frame,
        text=f"Собеседование на {job_skl}",
        style="Subtitle.TLabel"
    )
    job_label.pack(pady=3)

    total_points = get_total_points(participant)

    candidate_label = ttk.Label(
        frame,
        text=f"Кандидат: {participant_name}  •  Баллы: {total_points:g}",
        font=("Arial", 12)
    )
    candidate_label.pack(pady=5)

    navigation_frame = ttk.Frame(frame)
    navigation_frame.pack(pady=12)

    previous_button = RoundedButton(
        navigation_frame,
        text="◀",
        command=lambda: question_page(
            file_path,
            participant_name,
            shown_question - 1,
            from_history
        ),
        color=GRAY,
        hover_color=GRAY_HOVER,
        width=55,
        height=38,
        radius=10
    )
    previous_button.grid(row=0, column=0, padx=10)

    question_number_label = ttk.Label(
        navigation_frame,
        text=f"Вопрос {shown_question} из {len(participant['questions'])}",
        font=("Arial", 14, "bold")
    )
    question_number_label.grid(row=0, column=1, padx=15)

    next_button = RoundedButton(
        navigation_frame,
        text="▶",
        command=lambda: question_page(
            file_path,
            participant_name,
            shown_question + 1,
            from_history
        ),
        color=GRAY,
        hover_color=GRAY_HOVER,
        width=55,
        height=38,
        radius=10
    )
    next_button.grid(row=0, column=2, padx=10)

    if shown_question == 1:
        previous_button.set_state("disabled")

    if shown_question == len(participant["questions"]):
        next_button.set_state("disabled")

    question_text = participant["questions"][shown_question - 1]

    question_label = ttk.Label(
        frame,
        text=question_text,
        font=("Arial", 15, "bold"),
        wraplength=620,
        justify="center"
    )
    question_label.pack(padx=30, pady=25)

    timer_label = ttk.Label(
        frame,
        text="",
        font=("Arial", 13, "bold"),
        foreground=RED
    )
    timer_label.pack(pady=8)

    question_points = participant.get("points", {})
    question_key = str(shown_question)
    current_state = participant.get("question_state", 0)

    if question_key in question_points:
        result_label = ttk.Label(
            frame,
            text=f"Кандидат получил: {float(question_points[question_key]):g}",
            font=("Arial", 14, "bold"),
            foreground=GREEN
        )
        result_label.pack(pady=10)

    elif participant.get("is_checked") or current_state == -1:
        result_label = ttk.Label(
            frame,
            text="Вопрос не оценен",
            font=("Arial", 13),
            foreground="#6B7280"
        )
        result_label.pack(pady=10)

    elif shown_question != current_state:
        result_label = ttk.Label(
            frame,
            text="Этот вопрос еще не оценен",
            font=("Arial", 13),
            foreground="#6B7280"
        )
        result_label.pack(pady=10)

    else:
        time_per_question = int(
            data.get("time_per_question", 0)
        )

        if time_per_question == 0:
            timer_label.config(
                text="Без ограничения времени",
                foreground="#6B7280"
            )
        else:
            start_question_timer(
                timer_label,
                time_per_question
            )

        points_frame = ttk.Frame(frame)
        points_frame.pack(pady=18)

        zero_button = RoundedButton(
            points_frame,
            text="+0",
            command=lambda: set_question_points(
                file_path,
                participant_name,
                shown_question,
                0,
                from_history
            ),
            color=RED,
            hover_color=RED_HOVER,
            width=100,
            height=45,
            radius=13
        )
        zero_button.grid(row=0, column=0, padx=7)

        half_button = RoundedButton(
            points_frame,
            text="+0.5",
            command=lambda: set_question_points(
                file_path,
                participant_name,
                shown_question,
                0.5,
                from_history
            ),
            color=YELLOW,
            hover_color=YELLOW_HOVER,
            width=100,
            height=45,
            radius=13
        )
        half_button.grid(row=0, column=1, padx=7)

        one_button = RoundedButton(
            points_frame,
            text="+1",
            command=lambda: set_question_points(
                file_path,
                participant_name,
                shown_question,
                1,
                from_history
            ),
            color=GREEN,
            hover_color=GREEN_HOVER,
            width=100,
            height=45,
            radius=13
        )
        one_button.grid(row=0, column=2, padx=7)


def start_question_timer(timer_label, seconds_left):
    global timer_after

    if not timer_label.winfo_exists():
        return

    if seconds_left <= 0:
        timer_label.config(
            text="Время вышло!",
            foreground=RED
        )
        timer_after = None
        return

    timer_label.config(
        text=f"Осталось: {seconds_left} сек.",
        foreground=RED if seconds_left <= 5 else "#111827"
    )

    timer_after = root.after(
        1000,
        lambda: start_question_timer(
            timer_label,
            seconds_left - 1
        )
    )


def set_question_points(
    file_path,
    participant_name,
    question_number,
    points,
    from_history=False
):
    data = load_data(file_path)

    if not data:
        return

    participant = next(
        (
            answer
            for answer in data["answers"]
            if answer["name"] == participant_name
        ),
        None
    )

    if participant is None:
        return

    if participant.get("question_state") != question_number:
        question_page(
            file_path,
            participant_name,
            question_number,
            from_history
        )
        return

    participant.setdefault("points", {})
    participant["points"][str(question_number)] = points

    if question_number >= len(participant["questions"]):
        participant["question_state"] = -1
        participant["is_checked"] = True

        if all(
            answer.get("is_checked", False)
            for answer in data["answers"]
        ):
            data["marked_ended"] = True

        save_data(file_path, data)
        candidates_page(file_path, from_history)

    else:
        participant["question_state"] = question_number + 1

        save_data(file_path, data)

        question_page(
            file_path,
            participant_name,
            question_number + 1,
            from_history
        )


def history_page():
    clear_page()

    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    create_back_button(
        frame,
        "◀ Домой",
        main_page
    )

    create_title(
        frame,
        "История собеседований"
    )

    history_frame = ttk.Frame(frame)
    history_frame.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=10
    )

    history_files = get_history_files()

    if not history_files:
        empty_label = ttk.Label(
            history_frame,
            text="История пуста",
            font=("Arial", 13),
            foreground="#6B7280"
        )
        empty_label.pack(pady=40)
        return

    for file_path in history_files:
        data = load_data(file_path)

        if not data:
            continue

        answers = data.get("answers", [])

        checked_count = len([
            answer
            for answer in answers
            if answer.get("is_checked", False)
        ])

        all_count = len(answers)

        is_ended = (
            data.get("marked_ended", False)
            or (
                all_count > 0
                and checked_count == all_count
            )
        )

        if is_ended:
            ended_text = "Завершено"
            color = GREEN
            hover_color = GREEN_HOVER
        else:
            ended_text = "Не завершено"
            color = RED
            hover_color = RED_HOVER

        history_button = RoundedButton(
            history_frame,
            text=f"{data.get('short_name', '')}  •  {data.get('job', '')}  •  {ended_text} ({checked_count}/{all_count})",
            command=(
                lambda selected_file=file_path:
                candidates_page(selected_file, True)
            ),
            color=color,
            hover_color=hover_color,
            width=600,
            height=46,
            radius=13
        )
        history_button.pack(fill="x", pady=5)


def bugs_and_adv():
    tk.messagebox.showinfo("Баги и предложения", f"Если вы нашли баг или у вас есть предложение по улучшению, пожалуйста, свяжитесь с автором:\n{', '.join([i + ': ' + AUTHOR_CONTACTS[i] for i in AUTHOR_CONTACTS])}\n\nВерсия программы: {VERSION}")

start()
main_page()
root.mainloop()