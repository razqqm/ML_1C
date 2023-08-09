import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class Task:
    def __init__(self, name, duration, start_date=None):
        self.name = name
        self.duration = duration
        self.start_date = start_date if start_date else datetime.now().date()

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Календарь задач")
        
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        
        # Navigation
        self.nav_frame = ttk.Frame(self.root)
        self.nav_frame.pack(pady=5)

        self.prev_button = ttk.Button(self.nav_frame, text="<", command=self.prev_month)
        self.prev_button.grid(row=0, column=0)

        self.month_label = ttk.Label(self.nav_frame, text=f"{self.current_month}-{self.current_year}")
        self.month_label.grid(row=0, column=1)

        self.next_button = ttk.Button(self.nav_frame, text=">", command=self.next_month)
        self.next_button.grid(row=0, column=2)

        self.draw_calendar()

    def draw_calendar(self):
        # Destroy previous calendar if exists
        if hasattr(self, "calendar_frame"):
            self.calendar_frame.destroy()

        self.calendar_frame = ttk.Frame(self.root)
        self.calendar_frame.pack(padx=10, pady=10)

        # Days headers
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for idx, day in enumerate(days):
            label = ttk.Label(self.calendar_frame, text=day)
            label.grid(row=0, column=idx)

        # Calculate days in the month
        month_days = [i for i in range(1, (self.days_in_month(self.current_month, self.current_year) + 1))]
        first_day_weekday = datetime(self.current_year, self.current_month, 1).weekday()

        # Create empty buttons for spacing before the first day
        for _ in range(first_day_weekday):
            ttk.Button(self.calendar_frame, text=" ", state=tk.DISABLED).grid(row=1, column=_)

        # Place buttons
        week_row = 1
        for index, day in enumerate(month_days, start=first_day_weekday):
            col_idx = index % 7
            if col_idx == 0 and index != 0:
                week_row += 1
            btn = ttk.Button(self.calendar_frame, text=day)
            btn.grid(row=week_row, column=col_idx)

        # Update month label
        self.month_label.config(text=f"{self.current_month}-{self.current_year}")

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.draw_calendar()

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.draw_calendar()

    @staticmethod
    def days_in_month(month, year):
        if month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            return 28
        if month in [4, 6, 9, 11]:
            return 30
        return 31

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
