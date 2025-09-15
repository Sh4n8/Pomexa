import customtkinter as ctk
import time
import threading
import winsound

class PomodoroTimer:
    def __init__(self, label):
        self.label = label
        self.running = False
        self.work_time = 25 * 60
        self.break_time = 5 * 60
        self.time_left = self.work_time
        self.on_break = False
        self.thread = None
        self._lock = threading.Lock()  

    def start(self):
        with self._lock:
            if not self.running:
                self.running = True
                if not self.thread or not self.thread.is_alive():
                    self.thread = threading.Thread(target=self.countdown)
                    self.thread.start()

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.on_break = False
        self.time_left = self.work_time
        self.update_label()

    def skip(self):
        """Skip current session safely"""
        self.running = False
        self.on_break = not self.on_break
        self.time_left = self.break_time if self.on_break else self.work_time
        self.update_label()
        self.start()  

    def countdown(self):
        while self.time_left > 0:
            if not self.running:
                break
            mins, secs = divmod(self.time_left, 60)
            self.label.configure(text=f"{mins:02d}:{secs:02d}")
            time.sleep(1)
            self.time_left -= 1

        if self.time_left == 0:
            self.running = False
            self.play_sound()
            self.on_break = not self.on_break
            self.time_left = self.break_time if self.on_break else self.work_time
            self.start()  

    def update_label(self):
        mins, secs = divmod(self.time_left, 60)
        self.label.configure(text=f"{mins:02d}:{secs:02d}")

    def play_sound(self):
        winsound.Beep(2000, 1500)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Pomexa Timer")
app.geometry("350x220")

timer_label = ctk.CTkLabel(app, text="25:00", font=("Helvetica", 40))
timer_label.pack(pady=20)

pomodoro = PomodoroTimer(timer_label)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

start_btn = ctk.CTkButton(button_frame, text="Start", command=pomodoro.start)
start_btn.grid(row=0, column=0, padx=5)

pause_btn = ctk.CTkButton(button_frame, text="Pause", command=pomodoro.pause)
pause_btn.grid(row=0, column=1, padx=5)

reset_btn = ctk.CTkButton(button_frame, text="Reset", command=pomodoro.reset)
reset_btn.grid(row=0, column=2, padx=5)

skip_btn = ctk.CTkButton(button_frame, text="Skip", command=pomodoro.skip)
skip_btn.grid(row=0, column=3, padx=5)

app.mainloop()
