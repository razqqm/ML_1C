import calendar
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
import json
import os

class TaskDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("300x300")
        self.title("Добавить задачу (метод add_task)")

        self.task_name = tk.StringVar()
        self.duration_hours = tk.IntVar()
        self.duration_minutes = tk.IntVar(value=15)
        self.user_id = tk.IntVar(value=1000)

        tk.Label(self, text="Имя задачи (метод add_task):").pack(pady=5)
        tk.Entry(self, textvariable=self.task_name).pack(pady=5)

        tk.Label(self, text="Часы (метод add_task):").pack(pady=5)
        tk.Spinbox(self, from_=0, to=100, textvariable=self.duration_hours).pack(pady=5)

        tk.Label(self, text="Минуты (кратно 15, метод add_task):").pack(pady=5)
        tk.Spinbox(self, from_=0, to=59, increment=15, textvariable=self.duration_minutes).pack(pady=5)

        tk.Label(self, text="ID пользователя (метод add_task):").pack(pady=5)
        tk.Entry(self, textvariable=self.user_id).pack(pady=5)

        ttk.Button(self, text="Сохранить", command=self.add_task, style="Main.TButton").pack(pady=10)

        self.result = None

    def add_task(self):
        task = {
            "name": self.task_name.get(),
            "hours": self.duration_hours.get(),
            "minutes": self.duration_minutes.get(),
            "user_id": self.user_id.get()
        }
        self.result = task
        self.destroy()

class CalendarApp:
    def __init__(self, root):
        self.year = datetime.today().year
        self.month = datetime.today().month
        self.root = root
        self.selected_buttons = []
        self.tasks_filename = "tasks.json"
        self.tasks = []
        self.working_days = tk.IntVar(self.root)
        self.working_days.set(5)
        self.load_tasks()

        self.label = tk.Label(root, text="", font="Helvetica 16 bold")
        self.label.pack(pady=10)

        self.create_calendar()
        self.create_task_list()
        self.create_working_days_schedule()

        self.selected_day_label = tk.Label(root, text="", font="Helvetica 12")
        self.selected_day_label.pack(pady=10)

        navigation_frame = tk.Frame(root)
        navigation_frame.pack(pady=10)
        ttk.Button(navigation_frame, text="Предыдущий месяц", command=self.previous_month, style="Main.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(navigation_frame, text="Следующий месяц", command=self.next_month, style="Main.TButton").pack(side=tk.RIGHT, padx=5)

        # Применение стилей
        self.root.option_add("*TCombobox*Listbox*Font", "Helvetica 12")
        self.root.option_add("*TCombobox*Listbox*Background", "white")
        self.root.option_add("*TCombobox*Listbox*Foreground", "black")
        self.root.option_add("*TCombobox*Listbox*selectBackground", "#4e88bf")
        self.root.option_add("*TCombobox*Listbox*selectForeground", "white")

        self.root.option_add("*TCombobox*Font", "Helvetica 12")
        self.root.option_add("*TCombobox*Background", "white")
        self.root.option_add("*TCombobox*Foreground", "black")
        self.root.option_add("*TCombobox*selectBackground", "#4e88bf")
        self.root.option_add("*TCombobox*selectForeground", "white")

        # Оформление стиля кнопок
        style = ttk.Style()
        style.configure("Main.TButton", font="Helvetica 12")

# основной код
    def create_calendar(self):
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack(pady=10)

        self.show_calendar()

    def create_task_list(self):
        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack(padx=10,pady=10)

        self.task_listbox = tk.Listbox(self.task_frame, selectmode=tk.SINGLE, height=10, width=80, font="Helvetica 12")
        self.task_listbox.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        for task in self.tasks:
            task_text = f"{task['name']} ({task['hours']} часов {task['minutes']} минут), ID пользователя: {task['user_id']}"
            self.task_listbox.insert(tk.END, task_text)

        task_control_frame = tk.Frame(self.task_frame)
        task_control_frame.pack(side=tk.TOP)

        ttk.Button(task_control_frame, text="Добавить", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(task_control_frame, text="Удалить", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(task_control_frame, text="Редактировать", command=self.edit_task).pack(side=tk.LEFT, padx=5)

    def create_working_days_schedule(self):
        self.working_days = tk.IntVar(self.root)
        self.working_days.set(5)
        
        tk.Radiobutton(self.root, text="5 дней", variable=self.working_days, value=5, command=self.show_calendar).pack(side=tk.LEFT)
        tk.Radiobutton(self.root, text="6 дней", variable=self.working_days, value=6, command=self.show_calendar).pack(side=tk.LEFT)
        tk.Radiobutton(self.root, text="7 дней", variable=self.working_days, value=7, command=self.show_calendar).pack(side=tk.LEFT)

    def show_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.selected_buttons.clear()

        self.cal = calendar.monthcalendar(self.year, self.month)

        weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for day in weekdays:
            tk.Label(self.calendar_frame, text=day, font="Helvetica 16 bold").grid(row=0, column=weekdays.index(day))

        for row, week in enumerate(self.cal):
            for col, day in enumerate(week):
                if day == 0:
                    continue

                state = tk.DISABLED
                color = "red" if col >= 5 else "black"
                if col < self.working_days.get() or (col == 5 and self.working_days.get() == 6):
                    state = tk.NORMAL

                button = tk.Button(self.calendar_frame, text=day, fg=color, font="Helvetica 16", width=5, height=2, state=state)
                button.grid(row=row+1, column=col, padx=5, pady=5)

                if state != tk.DISABLED:
                    button.bind("<Button-1>", lambda e, button=button, day=day: self.select_day(button, day))

        self.label.config(text=f"{calendar.month_name[self.month]} {self.year}")

    def select_day(self, button, day):
        if button in self.selected_buttons:
            button.config(relief=tk.FLAT)
            self.selected_buttons.remove(button)
        else:
            button.config(relief=tk.SOLID)
            self.selected_buttons.append(button)

        selected_days = [int(b.cget("text")) for b in self.selected_buttons]
        self.selected_day_label.config(text=f"Выбранные дни: {', '.join(map(str, selected_days))} {calendar.month_name[self.month]} {self.year}")

    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.show_calendar()

    def previous_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.show_calendar()

    def add_task(self):
        dialog = TaskDialog(self.root)
        self.root.wait_window(dialog)
        task = dialog.result
        if task:
            self.tasks.append(task)
            task_text = f"{task['name']} ({task['hours']} часов {task['minutes']} минут), ID пользователя: {task['user_id']}"
            self.task_listbox.insert(tk.END, task_text)
            self.save_tasks()

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            del self.tasks[selected_index[0]]
            self.task_listbox.delete(selected_index)
            self.save_tasks()

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task = self.tasks[selected_index[0]]
            dialog = TaskDialog(self.root)
            dialog.task_name.set(task['name'])
            dialog.duration_hours.set(task['hours'])
            dialog.duration_minutes.set(task['minutes'])
            dialog.user_id.set(task['user_id'])
            self.root.wait_window(dialog)

            new_task = dialog.result
            if new_task:
                self.tasks[selected_index[0]] = new_task
                task_text = f"{new_task['name']} ({new_task['hours']} часов {new_task['minutes']} минут), ID пользователя: {new_task['user_id']}"
                self.task_listbox.delete(selected_index)
                self.task_listbox.insert(selected_index, task_text)
                self.save_tasks()

    def load_tasks(self):
        try:
            if os.path.exists(self.tasks_filename):
                with open(self.tasks_filename, 'r', encoding='utf-8') as file:
                    self.tasks = json.load(file)
            else:
                self.tasks = []
        except json.JSONDecodeError:
            print("Файл задач поврежден или имеет неверный формат. Создание нового файла.")
            self.tasks = []

    def save_tasks(self):
        with open(self.tasks_filename, 'w', encoding='utf-8') as file:
            json.dump(self.tasks, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Графический Календарь")
    app = CalendarApp(root)
    root.mainloop()
