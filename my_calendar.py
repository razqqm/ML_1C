import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import calendar
import datetime

class TaskDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Add task")

        self.task_name = tk.StringVar()
        self.duration_hours = tk.IntVar()
        self.duration_minutes = tk.IntVar()
        self.user_id = tk.IntVar()
        self.priority = tk.IntVar()

        tk.Label(self, text="Task name:").pack(pady=5)
        tk.Entry(self, textvariable=self.task_name).pack(pady=5)
        
        tk.Label(self, text="Duration (hours):").pack(pady=5)
        tk.Entry(self, textvariable=self.duration_hours).pack(pady=5)
        
        tk.Label(self, text="Duration (minutes):").pack(pady=5)
        tk.Entry(self, textvariable=self.duration_minutes).pack(pady=5)

        tk.Label(self, text="User ID:").pack(pady=5)
        tk.Entry(self, textvariable=self.user_id).pack(pady=5)

        tk.Label(self, text="Priority:").pack(pady=5)
        tk.Entry(self, textvariable=self.priority).pack(pady=5)

        ttk.Button(self, text="OK", command=self.add_task).pack(pady=10)

    def add_task(self):
        task = {
            "name": self.task_name.get(),
            "duration": self.duration_hours.get() * 60 + self.duration_minutes.get(),
            "user_id": self.user_id.get(),
            "priority": self.priority.get()
        }
        self.master.tasks.append(task)
        self.destroy()

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar")
        self.root.geometry("800x600")
        
        self.tasks = []
        self.time_boxes = [[None for _ in range(32)] for _ in range(7)]
        
        self.year = tk.IntVar(value=datetime.datetime.now().year)
        self.month = tk.IntVar(value=datetime.datetime.now().month)
        self.working_days = tk.IntVar(value=5)

        self.create_ui()

    def create_ui(self):
        controls_frame = ttk.Frame(self.root)
        controls_frame.pack(pady=5)
        
        ttk.Label(controls_frame, text="Year:").pack(side=tk.LEFT)
        ttk.Entry(controls_frame, textvariable=self.year).pack(side=tk.LEFT)

        ttk.Label(controls_frame, text="Month:").pack(side=tk.LEFT)
        ttk.Entry(controls_frame, textvariable=self.month).pack(side=tk.LEFT)
        
        ttk.Label(controls_frame, text="Working days:").pack(side=tk.LEFT)
        ttk.Entry(controls_frame, textvariable=self.working_days).pack(side=tk.LEFT)

        ttk.Button(controls_frame, text="Show calendar", command=self.show_calendar).pack(side=tk.LEFT, padx=5)
        
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        task_controls_frame = ttk.Frame(self.root)
        task_controls_frame.pack(pady=5)

        ttk.Button(task_controls_frame, text="Add task", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(task_controls_frame, text="Simulate", command=self.simulate).pack(side=tk.LEFT, padx=5)

    def add_task(self):
        TaskDialog(self)

    def show_calendar(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.time_boxes = [[None for _ in range(32)] for _ in range(7)]
        
        cal = calendar.monthcalendar(self.year.get(), self.month.get())
        for i in range(len(cal)):
            for j in range(7):
                if cal[i][j] != 0:
                    cell_text = str(cal[i][j])
                    label = tk.Label(self.table_frame, text=cell_text, borderwidth=2, relief="solid", width=5, height=2)
                    label.grid(row=i, column=j)
                    self.time_boxes[j][cal[i][j]] = label

        self.update_calendar()

    def update_calendar(self):
        for i in range(len(self.time_boxes)):
            for j in range(len(self.time_boxes[i])):
                if self.time_boxes[i][j] is not None:
                    self.time_boxes[i][j]["text"] = str(j) + "\n"

    def simulate(self):
        self.tasks.sort(key=lambda x: x["priority"], reverse=True)

        day_time = 480 # 8 hours in minutes
        day_limit = self.working_days.get()
        month_days = calendar.monthrange(self.year.get(), self.month.get())[1]

        day = 1
        weekday = datetime.datetime(self.year.get(), self.month.get(), day).weekday()

        for task in self.tasks:
            while task["duration"] > 0 and day <= month_days:
                if weekday < day_limit: # working day
                    if task["duration"] >= day_time: # task lasts whole day
                        self.time_boxes[weekday][day]["text"] += task["name"] + "\n"
                        task["duration"] -= day_time
                    else: # task lasts part of the day
                        self.time_boxes[weekday][day]["text"] += task["name"] + " (" + str(task["duration"]) + "m)\n"
                        task["duration"] = 0

                day += 1
                weekday = datetime.datetime(self.year.get(), self.month.get(), day).weekday() if day <= month_days else 7

root = tk.Tk()
app = CalendarApp(root)
root.mainloop()
