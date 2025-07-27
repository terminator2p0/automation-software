import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading

class AutomationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Automation Software")
        self.geometry("600x400")

        self.run_button = tk.Button(self, text="Run Automation", command=self.run_scripts)
        self.run_button.pack(pady=10)

        self.log_area = ScrolledText(self, height=15)
        self.log_area.pack(fill='both', expand=True, padx=10, pady=10)

    def run_scripts(self):
        def target():
            self.log_area.insert(tk.END, "Starting automation...\n")
            # Example: call your main script using subprocess
            process = subprocess.Popen(["python", "weather.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in process.stdout:
                self.log_area.insert(tk.END, line)
                self.log_area.see(tk.END)
            self.log_area.insert(tk.END, "Automation finished.\n")

        threading.Thread(target=target).start()

if __name__ == "__main__":
    app = AutomationApp()
    app.mainloop()
