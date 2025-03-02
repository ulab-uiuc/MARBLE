# team_sync_pro.py
# This is the main implementation of TeamSyncPro

import datetime
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
import random

class TeamSyncPro:
    def __init__(self, root):
        self.root = root
        self.root.title("TeamSyncPro")
        self.root.geometry("800x600")
        self.users = {}
        self.tasks = {}
        self.projects = {}
        self.reminders = {}

        # Create frames for different sections
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        self.schedule_frame = tk.Frame(self.root)
        self.schedule_frame.pack(pady=20)

        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack(pady=20)

        self.project_frame = tk.Frame(self.root)
        self.project_frame.pack(pady=20)

        self.reminder_frame = tk.Frame(self.root)
        self.reminder_frame.pack(pady=20)

        # Create login section
        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.pack(side=tk.LEFT)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack(side=tk.LEFT)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.pack(side=tk.LEFT)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack(side=tk.LEFT)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(side=tk.LEFT)

        # Create schedule section
        self.schedule_label = tk.Label(self.schedule_frame, text="Schedule:")
        self.schedule_label.pack()
        self.schedule_text = tk.Text(self.schedule_frame, width=50, height=10)
        self.schedule_text.pack()

        # Create task section
        self.task_label = tk.Label(self.task_frame, text="Task:")
        self.task_label.pack()
        self.task_name_entry = tk.Entry(self.task_frame)
        self.task_name_entry.pack()
        self.task_priority_entry = tk.Entry(self.task_frame)
        self.task_priority_entry.pack()
        self.task_deadline_entry = tk.Entry(self.task_frame)
        self.task_deadline_entry.pack()
        self.task_button = tk.Button(self.task_frame, text="Add Task", command=self.add_task)
        self.task_button.pack()

        # Create project section
        self.project_label = tk.Label(self.project_frame, text="Project:")
        self.project_label.pack()
        self.project_name_entry = tk.Entry(self.project_frame)
        self.project_name_entry.pack()
        self.project_button = tk.Button(self.project_frame, text="Add Project", command=self.add_project)
        self.project_button.pack()

        # Create reminder section
        self.reminder_label = tk.Label(self.reminder_frame, text="Reminder:")
        self.reminder_label.pack()
        self.reminder_time_entry = tk.Entry(self.reminder_frame)
        self.reminder_time_entry.pack()
        self.reminder_button = tk.Button(self.reminder_frame, text="Set Reminder", command=self.set_reminder)
        self.reminder_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username] == password:
            self.login_frame.pack_forget()
            self.schedule_frame.pack()
            self.task_frame.pack()
            self.project_frame.pack()
            self.reminder_frame.pack()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def add_task(self):
        task_name = self.task_name_entry.get()
        task_priority = self.task_priority_entry.get()
        task_deadline = self.task_deadline_entry.get()
        self.tasks[task_name] = {"priority": task_priority, "deadline": task_deadline}
        self.schedule_text.insert(tk.END, f"Task: {task_name}, Priority: {task_priority}, Deadline: {task_deadline}\n")

    def add_project(self):
        project_name = self.project_name_entry.get()
        self.projects[project_name] = {}
        self.schedule_text.insert(tk.END, f"Project: {project_name}\n")

    def set_reminder(self):
        reminder_time = self.reminder_time_entry.get()
        self.reminders[reminder_time] = {}
        threading.Thread(target=self.remind, args=(reminder_time,)).start()

    def remind(self, reminder_time):
        time.sleep(int(reminder_time))
        messagebox.showinfo("Reminder", f"Reminder: {reminder_time}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    team_sync_pro = TeamSyncPro(root)
    team_sync_pro.run()