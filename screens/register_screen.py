import tkinter as tk
from tkinter import messagebox
from utils.helpers import (
    hash_password, load_image, PUP_RED, PUP_GOLD, BUTTON_BLUE_LIGHT, BUTTON_BLUE_DARK,
    LIGHT_BG, WHITE_BG, GRAY_TEXT, HEADER_FONT, TITLE_FONT, GLOBAL_FONT, BUTTON_FONT,
    PUP_LOGO_PATH, create_styled_button, create_rounded_entry_field
)

class RegisterScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=WHITE_BG) # Make screen background uniformly white
        self.controller = controller
        self.db = self.controller.get_db()

        # --- Variables ---
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        # --- PUP Logo ---
        self.pup_logo_label = tk.Label(self, image=self.controller.pup_logo, bg=WHITE_BG) # Changed to WHITE_BG
        self.pup_logo_label.pack(pady=(20, 10))

        # --- Header Text ---
        self.header_text = tk.Label(self, text="Mula sayo para\nsa bayan",
                                    font=HEADER_FONT, fg=PUP_RED, bg=WHITE_BG, # Changed to WHITE_BG
                                    justify="center")
        self.header_text.pack(pady=10)

        # --- Input Fields using custom rounded entry function ---
        self.name_entry = create_rounded_entry_field(self, "Name:", self.name_var, width=280)
        self.email_entry = create_rounded_entry_field(self, "Email Address :", self.email_var, width=280)
        self.password_entry = create_rounded_entry_field(self, "Password:", self.password_var, is_password=True, width=280)
        self.confirm_password_entry = create_rounded_entry_field(self, "Confirm Password :", self.confirm_password_var, is_password=True, width=280)

        # --- Buttons using custom styled button function ---
        button_frame = tk.Frame(self, bg=WHITE_BG) # Changed to WHITE_BG
        button_frame.pack(pady=10)

        self.back_to_login_button_canvas = create_styled_button(button_frame, "Back to LOGIN", self.go_to_login, BUTTON_BLUE_DARK, BUTTON_BLUE_LIGHT, width=120, height=30)
        self.back_to_login_button_canvas.pack(pady=5)

        self.register_button_canvas = create_styled_button(button_frame, "REGISTER", self.register_user, PUP_RED, PUP_GOLD, width=120, height=30)
        self.register_button_canvas.pack(pady=5)

    def go_to_login(self):
        self.controller.show_frame("LoginScreen")

    def register_user(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()

        if not name or not email or not password or not confirm_password:
            messagebox.showerror("Registration Error", "All fields are required.")
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Registration Error", "Please enter a valid email address.")
            return

        if password != confirm_password:
            messagebox.showerror("Registration Error", "Passwords do not match.")
            return

        if len(password) < 6:
            messagebox.showerror("Registration Error", "Password must be at least 6 characters long.")
            return

        hashed_password = hash_password(password)

        if self.db.fetch_one("SELECT id FROM users WHERE email = ?", (email,)):
            messagebox.showerror("Registration Error", "Email already registered. Please log in or use a different email.")
            return

        success = self.db.execute_query(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password)
        )

        if success:
            messagebox.showinfo("Registration Success", "Account created successfully! You can now log in.")
            self.clear_fields()
            self.controller.show_frame("LoginScreen")
        else:
            messagebox.showerror("Registration Error", "Failed to register. Please try again.")

    def clear_fields(self):
        self.name_var.set("")
        self.email_var.set("")
        self.password_var.set("")
        self.confirm_password_var.set("")