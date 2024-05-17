import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

#ΑΡΧΙΚΑ ΧΡΩΜΑΤΑ
BG_COLOR = "#292A2A"  
TEXT_COLOR = "#ADADAD"  
BUTTON_COLOR = "#107FE7"
BUTTON_TEXT_COLOR = "white"  

tasks = {}
points = 0

#ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΦΟΡΤΩΣΗ ΔΕΔΟΜΕΝΩΝ ΧΡΗΣΤΗ ΣΤΗΝ ΕΚΚΙΝΗΣΗ ΕΦΑΡΜΟΓΗΣ
def load_user_data():
    global points
    try:
        with open("user_data.txt", "r") as file:
            data = file.readline().strip()
            if data:
                points = int(data)
                update_points_rank_label()
    except FileNotFoundError:
        pass

    global tasks
    tasks = {}
    try:
        with open("tasks_data.txt", "r") as file:
            for line in file:
                date, task, difficulty = line.strip().split(",")
                if date not in tasks:
                    tasks[date] = [(task, difficulty)]
                else:
                    tasks[date].append((task, difficulty))
    except FileNotFoundError:
        pass

#ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΑΠΟΘΗΚΕΥΣΗ ΔΕΔΟΜΕΝΩΝ ΧΡΗΣΤΗ ΜΕ ΤΟ ΚΛΕΙΣΙΜΟ ΤΗΣ ΕΦΑΡΜΟΓΗΣ
def save_user_data():
    with open("user_data.txt", "w") as file:
        file.write(str(points))
    with open("tasks_data.txt", "w") as file:
        for date, task_list in tasks.items():
            for task, difficulty in task_list:
                file.write(f"{date},{task},{difficulty}\n")

#ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΠΡΟΣΘΗΚΗ ΣΤΟΧΟΥ
def add_task():
    date = cal.get_date()
    task = entry_task.get()
    difficulty = difficulty_var.get()

    if task:
        if date not in tasks:
            tasks[date] = [(task, difficulty)]
        else:
            tasks[date].append((task, difficulty))
        update_task_list()
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

#ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΕΝΗΜΕΡΩΣΗ ΤΟΥ LISTBOX ΓΙΑ ΣΩΣΤΗ ΠΑΡΟΥΣΙΑΣΗ ΤΩΝ ΣΤΟΧΩΝ
def update_task_list(event=None):
    listbox_tasks.delete(0, tk.END)
    date = cal.get_date()
    if date in tasks:
        for task, difficulty in tasks[date]:
            listbox_tasks.insert(tk.END, f"{task} ({difficulty})")

#ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΔΙΑΓΡΑΦΗ ΣΤΟΧΟΥ
def delete_task():
    try:
        task_index = listbox_tasks.curselection()[0]
        date = cal.get_date()
        tasks[date].pop(task_index)
        update_task_list()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete.")

#ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΟΛΟΚΛΗΡΩΣΗ ΣΤΟΧΟΥ ΚΑΙ ΠΡΟΣΘΗΚΗ ΠΟΝΤΩΝ
def complete_task():
    global points
    try:
        task_index = listbox_tasks.curselection()[0]
        date = cal.get_date()
        task, difficulty = tasks[date][task_index]
        tasks[date].pop(task_index)
        update_task_list()

        if difficulty == "Easy":
            points += 5
        elif difficulty == "Medium":
            points += 10
        elif difficulty == "Hard":
            points += 20

        update_points_rank_label()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to complete.")

#ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΕΝΗΜΕΡΩΣΗ ΠΟΝΤΩΝ KAI RANK
def update_points_rank_label():
    points_label.config(text=f"Points: {points}")
    rank = calculate_rank(points)
    rank_label.config(text=f"Rank: {rank}")

#ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΥΠΟΛΟΓΙΣΜΟ ΤΟΥ RANK
def calculate_rank(points):
    ranks = {
        10: "Iron",
        50: "Bronze",
        200: "Silver",
        300: "Gold",
        500: "Platinum",
        700: "Diamond",
        1000: "Master",
        2000: "Grandmaster"
    }

    closest_rank = None
    for points_needed, rank in ranks.items():
        if points >= points_needed:
            closest_rank = rank
        else:
            break
    return closest_rank

#ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΤΟ ΚΟΥΜΠΙ SHOW RANK INFO ΜΕ ΠΛΗΡΟΦΟΡΙΕΣ ΓΙΑ ΚΑΘΕ RANK
def show_rank_info():
    ranks = {
        10: "Iron",
        50: "Bronze",
        200: "Silver",
        300: "Gold",
        500: "Platinum",
        700: "Diamond",
        1000: "Master",
        2000: "Grandmaster"
    }

    rank_info = ""
    for points_needed, rank in ranks.items():
        if points >= points_needed:
            rank_info += f"{rank}: Completed\n"
        else:
            progress = points_needed - points
            rank_info += f"{rank}: {progress} points needed\n"

    messagebox.showinfo("Rank Information", rank_info)

#ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΤΟ ΟΡΘΟ ΚΛΕΙΣΙΜΟ ΤΗΣ ΕΦΑΡΜΟΓΗΣ
def handle_closing():
    save_user_data()
    root.destroy()

#ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΤΗ ΔΗΜΙΟΥΡΓΙΑ ΤΟΥ GUI 
def create_task_manager_gui():

    #ΑΡΧΙΚΟ ΠΑΡΑΘΥΡΟ
    global root
    root = tk.Tk()
    root.title("Task Manager")
    root.geometry("700x600")
    root.resizable(False, False)
    root.config(bg=BG_COLOR)

    root.columnconfigure(0, weight = 1)
    root.columnconfigure(1,weight=2)
    root.columnconfigure(2,weight=1)
    root.rowconfigure(0,weight=1)
    root.rowconfigure(1,weight=3)
    root.rowconfigure(2,weight=3)
    root.rowconfigure(3,weight=1)
    root.rowconfigure(4,weight=2)

    #ΤΙΤΛΟΣ
    title_label = tk.Label(root, text="TASK MANAGER", font=("Eras Bold ITC", 24, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
    title_label.grid(row=0, column=1, padx=10, pady=10)

    #ΠΕΔΙΟ ΕΙΣΑΓΩΓΗΣ ΣΤΟΧΩΝ
    global entry_task
    entry_task = tk.Entry(root, width=50)
    entry_task.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    #ΚΟΥΜΠΙ ΠΡΟΣΘΗΚΗΣ ΣΤΟΧΟΥ
    btn_add = tk.Button(root, text="Add Task", width=10, command=add_task, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    btn_add.grid(row=1, column=1, padx=10, pady=10, sticky="e")

    #Η ΛΙΣΤΑ ΜΕ ΤΟΥΣ ΣΤΟΧΟΥΣ
    global listbox_tasks
    listbox_tasks = tk.Listbox(root, width=50)
    listbox_tasks.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    #ΚΟΥΜΠΙ ΔΙΑΓΡΑΦΗΣ ΣΤΟΧΟΥ
    btn_delete = tk.Button(root, text="Delete Task", width=15, command=delete_task, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    btn_delete.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    #ΚΟΥΜΠΙ ΟΛΟΚΛΗΡΩΣΗΣ ΣΤΟΧΟΥ
    btn_complete = tk.Button(root, text="Complete Task", width=15, command=complete_task, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    btn_complete.grid(row=3, column=1, padx=10, pady=5, sticky="e")

    #ΚΟΥΜΠΙΑ ΕΠΙΛΟΓΗΣ ΔΥΣΚΟΛΙΑΣ ΣΤΟΧΟΥ
    global difficulty_var
    difficulty_var = tk.StringVar()
    difficulty_var.set("Easy")

    difficulty_frame = tk.Frame(root, bg=BG_COLOR)
    difficulty_frame.grid(row=2, column=1, padx=10, pady=10,sticky="e")

    tk.Radiobutton(difficulty_frame, text="Easy", variable=difficulty_var, value="Easy", bg=BG_COLOR).pack(anchor="w")
    tk.Radiobutton(difficulty_frame, text="Medium", variable=difficulty_var, value="Medium", bg=BG_COLOR).pack(anchor="w")
    tk.Radiobutton(difficulty_frame, text="Hard", variable=difficulty_var, value="Hard", bg=BG_COLOR).pack(anchor="w")

    #ΗΜΕΡΟΛΟΓΙΟ
    global cal
    cal = Calendar(root, selectmode="day")
    cal.grid(row=4, column=1,  padx=10, pady=10, sticky="w")
    cal.bind("<<CalendarSelected>>", update_task_list)

    #ΠΟΝΤΟΙ
    global points_label
    points_label = tk.Label(root, text="Points: 0", bg=BG_COLOR, fg=TEXT_COLOR)
    points_label.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

    #RANK
    global rank_label
    rank_label = tk.Label(root, text="Rank: Iron", bg=BG_COLOR, fg=TEXT_COLOR)
    rank_label.grid(row=0, column=2, padx=10, pady=30, sticky="ne")

    #ΚΟΥΜΠΙ ΠΛΗΡΟΦΟΡΙΩΝ ΓΙΑ ΤΟ RANK
    btn_rank_info = tk.Button(root, text="Rank Info", width=10, command=show_rank_info, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    btn_rank_info.grid(row=0, column=2, padx=10, pady=50, sticky="ne")

    load_user_data()

    root.protocol("WM_DELETE_WINDOW", handle_closing)

    root.mainloop()

create_task_manager_gui()