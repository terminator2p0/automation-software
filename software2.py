import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import schedule
import time
from datetime import datetime

class AutomationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Automation Software")
        self.geometry("600x400")

        self.run_button = tk.Button(self, text="Run Automation Now", command=self.run_scripts)
        self.run_button.pack(pady=10)

        self.start_schedule_button = tk.Button(self, text="Start Scheduled Automation (1:45 PM)", command=self.start_scheduler)
        self.start_schedule_button.pack(pady=10)

        self.log_area = ScrolledText(self, height=15)
        self.log_area.pack(fill='both', expand=True, padx=10, pady=10)

        self.scheduling_active = False
        self.scheduler_thread = None

    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.see(tk.END)

    def run_scripts(self):
        def target():
            self.log("Starting automation...")
            process = subprocess.Popen(
                ["python", "weather2.py"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            # Read stdout line by line
            for line in process.stdout:
                self.log(line.rstrip())

            # Read any errors and log them
            stderr = process.stderr.read()
            if stderr:
                self.log(f"Error: {stderr.strip()}")

            process.stdout.close()
            process.stderr.close()
            process.wait()
            self.log("Automation finished.")

        threading.Thread(target=target, daemon=True).start()

    def scheduled_job(self):
        self.log("Scheduled automation started.")
        self.run_scripts()

    def scheduler_loop(self):
        self.log("Scheduler thread started, waiting for scheduled time daily at 13:45...")
        while self.scheduling_active:
            schedule.run_pending()
            time.sleep(10)  # check every 10 seconds

    def start_scheduler(self):
        if self.scheduling_active:
            self.log("Scheduler is already running.")
            return

        schedule.clear()  # Clear any existing schedules
        schedule.every().day.at("13:45").do(self.scheduled_job)

        self.scheduling_active = True
        self.scheduler_thread = threading.Thread(target=self.scheduler_loop, daemon=True)
        self.scheduler_thread.start()

        self.log("Scheduler started: Automation will run daily at 13:45 (1:45 PM).")


if __name__ == "__main__":
    app = AutomationApp()
    app.mainloop()
