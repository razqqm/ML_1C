import tkinter as tk
from tkinter import ttk, simpledialog
from tkcalendar import Calendar
from datetime import datetime, timedelta
import json
import os

class TaskDialog(simpledialog.Dialog):
    def body(self, master):
        self.task_name = tk.StringVar()
        self.duration_hours = tk.IntVar()
        self.duration_minutes = tk.IntVar(value=15)
        self.user_id = tk.IntVar(value=1000)
        
        tk.Label(master, text="Имя задачи:").grid(row=0)
        tk.Entry(master, textvariable=self.task_name).grid(row=0, column=1)
        tk.Label(master, text="Часы:").grid(row=1)
        tk.Spinbox(master, from_=0, to=100, textvariable=self.duration_hours).grid(row=1, column=1)
        tk.Label(master, text="Минуты (кратно 15):").grid(row=2)
        tk.Spinbox(master, from_=0, to=59, increment=15, textvariable=self.duration_minutes).grid(row=2, column=1)
        tk.Label(master, text="ID пользователя:").grid(row=3)
        tk.Entry(master, textvariable=self.user_id).grid(row=3, column=1)

        return tk.Entry(master, textvariable=self.task_name)  # initial focus

    def apply(self):
        task = {
            "name": self.task_name.get(),
            "hours": self.duration_hours.get(),
            "minutes": self.duration_minutes.get(),
            "user_id": self.user_id.get()
        }
        self.result = task

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.tasks_filename = "tasks.json"
        self.tasks = []
        self.load_tasks()

        self.cal = Calendar(self.root, selectmode="day", year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)
        self.cal.pack(fill="both", expand=True)

        self.create_task_list()
        self.highlight_workdays()
        self.cal.bind("<<CalendarMonthChanged>>", lambda e: self.highlight_workdays())

    def highlight_workdays(self, event=None):
        self.cal.calevent_remove('all')  # Очищаем все события
        date = datetime.strptime(self.cal.get_date(), "%d.%m.%Y")

        # Определяем первый и последний день месяца
        start_date = datetime(date.year, date.month, 1)
        if date.month == 12:
            end_date = datetime(date.year+1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(date.year, date.month+1, 1) - timedelta(days=1)

        # Выделяем рабочие дни
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:  # Понедельник - Пятница
                self.cal.calevent_create(current_date, 'Рабочий день', 'workday')
            current_date += timedelta(days=1)
        self.cal.tag_config('workday', background='light green')

    def on_month_changed(self, event):
        self.highlight_workdays()

    def create_task_list(self):
        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack(padx=10,pady=10)

        self.task_listbox = tk.Listbox(self.task_frame, selectmode=tk.SINGLE, height=10, width=80)
        self.task_listbox.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        for task in self.tasks:
            task_text = f"{task['name']} ({task['hours']} часов {task['minutes']} минут), ID пользователя: {task['user_id']}"
            self.task_listbox.insert(tk.END, task_text)

        task_control_frame = tk.Frame(self.task_frame)
        task_control_frame.pack(side=tk.TOP)

        ttk.Button(task_control_frame, text="Добавить", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(task_control_frame, text="Удалить", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(task_control_frame, text="Редактировать", command=self.edit_task).pack(side=tk.LEFT, padx=5)

    def add_task(self):
        dialog = TaskDialog(self.root)
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
# E