import calendar
import tkinter as tk

def show_calendar():
    year = int(entry_year.get())
    month = int(entry_month.get())
    
    cal = calendar.month(year, month)
    
    text.delete(0.0, tk.END)
    text.insert(tk.INSERT, cal)

root = tk.Tk()
root.title("Простой Календарь")

label_year = tk.Label(root, text="Введите год:")
label_year.pack()

entry_year = tk.Entry(root)
entry_year.pack()

label_month = tk.Label(root, text="Введите месяц:")
label_month.pack()

entry_month = tk.Entry(root)
entry_month.pack()

button = tk.Button(root, text="Показать календарь", command=show_calendar)
button.pack()

text = tk.Text(root, width=25, height=10)
text.pack()

root.mainloop()
