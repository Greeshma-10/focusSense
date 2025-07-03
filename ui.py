import tkinter as tk
from tkinter import messagebox

class FocusUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FocusSense")
        self.label = tk.Label(self.root, text="Focus Score: 100", font=("Helvetica", 24))
        self.label.pack(pady=30)

    def update_score(self, score):
        self.label.config(text=f"Focus Score: {score}")
        self.root.update_idletasks()

    def alert_user(self):
        messagebox.showwarning("Distraction Detected", "You've lost focus. Please refocus!")

    def run(self):
        self.root.mainloop()
