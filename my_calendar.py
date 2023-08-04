import calendar
import tkinter as tk
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.year = datetime.today().year
        self.month = datetime.today().month
        self.root = root
        self.selected_buttons = []

        self.label = tk.Label(root, text="", font="Helvetica 16 bold")
        self.label.pack(pady=10)

        tk.Button(self.root, text="Предыдущий месяц", command=self.previous_month, font="Helvetica 12").pack(side=tk.LEFT)
        tk.Button(self.root, text="Следующий месяц", command=self.next_month, font="Helvetica 12").pack(side=tk.RIGHT)

        self.create_calendar()
        self.create_task_list()
        self.selected_day_label = tk.Label(root, text="", font="Helvetica 12")
        self.selected_day_label.pack(pady=10)

    def create_calendar(self):
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack(pady=10, side=tk.LEFT)

        self.show_calendar()

    def create_task_list(self):
        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack(pady=10, side=tk.RIGHT)

        self.task_listbox = tk.Listbox(self.task_frame, selectmode=tk.MULTIPLE, height=10, width=30, font="Helvetica 12")
        self.task_listbox.pack(side=tk.TOP)

        for task in ["Задача 1", "Задача 2", "Задача 3", "Задача 4"]:
            self.task_listbox.insert(tk.END, task)

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

                color = "red" if col >= 5 else "black"
                state = tk.DISABLED if col >= 5 else tk.NORMAL

                if day == datetime.today().day and self.year == datetime.today().year and self.month == datetime.today().month:
                    color = "blue"

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

root = tk.Tk()
root.title("Графический Календарь")
app = CalendarApp(root)
root.mainloop()
