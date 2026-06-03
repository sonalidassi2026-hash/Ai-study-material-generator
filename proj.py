import customtkinter as ctk
from tkinter import filedialog
import threading
import requests
import time
import os

# ==========================
# TELEGRAM CONFIG
# ==========================
BOT_TOKEN = "8872838119:AAG3bPHZHT3_LXiD3hLlBDUD4ynvS4OD6bQ"
CHAT_ID = "2101113698"


class TelegramSchedulerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Telegram Image Scheduler")
        self.geometry("1100x700")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.files = []
        self.running = False

        self.create_ui()

    def create_ui(self):

        # ==========================
        # TOP BAR
        # ==========================
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=10, pady=10)

        title = ctk.CTkLabel(
            top_frame,
            text="📤 Telegram Image Scheduler",
            font=("Segoe UI", 24, "bold")
        )
        title.pack(side="left", padx=15)

        self.theme_menu = ctk.CTkOptionMenu(
            top_frame,
            values=["System", "Dark", "Light"],
            command=self.change_theme
        )
        self.theme_menu.pack(side="right", padx=15)

        # ==========================
        # MAIN CONTENT
        # ==========================
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT PANEL
        left = ctk.CTkFrame(main)
        left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # RIGHT PANEL
        right = ctk.CTkFrame(main, width=300)
        right.pack(side="right", fill="y", padx=5, pady=5)

        # ==========================
        # FILE SELECTION
        # ==========================
        files_frame = ctk.CTkFrame(left)
        files_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            files_frame,
            text="📁 Select Image Files",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.file_label = ctk.CTkLabel(
            files_frame,
            text="No files selected"
        )
        self.file_label.pack(anchor="w", padx=10)

        ctk.CTkButton(
            files_frame,
            text="Browse Images",
            command=self.select_files
        ).pack(padx=10, pady=10)

        # ==========================
        # INTERVAL SETTINGS
        # ==========================
        interval_frame = ctk.CTkFrame(left)
        interval_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            interval_frame,
            text="⏱ Upload Interval",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=10, pady=10)

        self.interval_entry = ctk.CTkEntry(
            interval_frame,
            placeholder_text="Seconds"
        )
        self.interval_entry.insert(0, "10")
        self.interval_entry.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # ==========================
        # STATUS
        # ==========================
        status_frame = ctk.CTkFrame(left)
        status_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            status_frame,
            text="📊 Progress & Status",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=10, pady=10)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready"
        )
        self.status_label.pack(anchor="w", padx=10)

        self.progress_bar = ctk.CTkProgressBar(status_frame)
        self.progress_bar.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.progress_bar.set(0)

        # ==========================
        # CONTROL BUTTONS
        # ==========================
        controls = ctk.CTkFrame(left)
        controls.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(
            controls,
            text="▶ Start",
            command=self.start_upload
        ).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            controls,
            text="⏹ Stop",
            fg_color="red",
            command=self.stop_upload
        ).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            controls,
            text="🗑 Clear",
            command=self.clear_all
        ).pack(side="left", padx=10, pady=10)

        # ==========================
        # LOGS
        # ==========================
        log_frame = ctk.CTkFrame(left)
        log_frame.pack(fill="both", expand=True,
                       padx=10, pady=10)

        ctk.CTkLabel(
            log_frame,
            text="📝 Logs",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=10, pady=10)

        self.log_box = ctk.CTkTextbox(log_frame)
        self.log_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # ==========================
        # RIGHT PANEL INFO
        # ==========================
        ctk.CTkLabel(
            right,
            text="⚙ Telegram Configuration",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        self.bot_token = ctk.CTkEntry(
            right,
            placeholder_text="Bot Token"
        )
        self.bot_token.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.chat_id = ctk.CTkEntry(
            right,
            placeholder_text="Chat ID"
        )
        self.chat_id.pack(
            fill="x",
            padx=15,
            pady=10
        )

    # ==========================
    # FUNCTIONS
    # ==========================

    def change_theme(self, mode):
        ctk.set_appearance_mode(mode)

    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def select_files(self):

        files = filedialog.askopenfilenames(
            filetypes=[
                ("Images",
                 "*.png *.jpg *.jpeg *.webp")
            ]
        )

        self.files = list(files)

        self.file_label.configure(
            text=f"{len(self.files)} image(s) selected"
        )

        self.log(
            f"Loaded {len(self.files)} image(s)"
        )

    def send_photo(self, filepath):

        token = self.bot_token.get()
        chat_id = self.chat_id.get()

        url = (
            f"https://api.telegram.org/bot"
            f"{token}/sendPhoto"
        )

        with open(filepath, "rb") as img:

            response = requests.post(
                url,
                data={
                    "chat_id": chat_id
                },
                files={
                    "photo": img
                }
            )

        return response.status_code == 200

    def worker(self):

        total = len(self.files)

        for index, image in enumerate(self.files):

            if not self.running:
                self.log("Upload stopped.")
                return

            filename = os.path.basename(image)

            self.status_label.configure(
                text=f"Sending: {filename}"
            )

            self.log(
                f"Sending {filename}"
            )

            try:
                success = self.send_photo(image)

                if success:
                    self.log(
                        f"✓ Sent {filename}"
                    )
                else:
                    self.log(
                        f"✗ Failed {filename}"
                    )

            except Exception as e:
                self.log(
                    f"Error: {e}"
                )

            progress = (index + 1) / total
            self.progress_bar.set(progress)

            if index < total - 1:
                time.sleep(
                    int(
                        self.interval_entry.get()
                    )
                )

        self.status_label.configure(
            text="Completed"
        )

        self.log("All uploads completed.")

        self.running = False

    def start_upload(self):

        if not self.files:
            self.log("No files selected.")
            return

        if self.running:
            return

        self.running = True

        threading.Thread(
            target=self.worker,
            daemon=True
        ).start()

    def stop_upload(self):
        self.running = False

    def clear_all(self):

        self.running = False
        self.files = []

        self.progress_bar.set(0)

        self.file_label.configure(
            text="No files selected"
        )

        self.status_label.configure(
            text="Ready"
        )

        self.log_box.delete(
            "1.0",
            "end"
        )


if __name__ == "__main__":
    app = TelegramSchedulerApp()
    app.mainloop()