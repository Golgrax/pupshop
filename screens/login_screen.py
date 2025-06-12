import tkinter as tk
from tkinter import messagebox
from utils.helpers import (
    check_password, load_image, PUP_RED, PUP_GOLD, BUTTON_BLUE_LIGHT, BUTTON_BLUE_DARK, # <-- Added check_password
    LIGHT_BG, WHITE_BG, GRAY_TEXT, HEADER_FONT, TITLE_FONT, GLOBAL_FONT, BUTTON_FONT,
    PUP_LOGO_PATH, create_styled_button, create_rounded_entry_field
)

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=LIGHT_BG)
        self.controller = controller
        self.db = self.controller.get_db()

        # --- Variables ---
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # --- PUP Logo ---
        self.pup_logo_label = tk.Label(self, image=self.controller.pup_logo, bg=LIGHT_BG)
        self.pup_logo_label.pack(pady=(40, 20))

        self.header_text = tk.Label(self, text="Welcome Back!",
                                    font=HEADER_FONT, fg=PUP_RED, bg=LIGHT_BG)
        self.header_text.pack(pady=20)

        # Input fields using custom rounded entry
        self.email_entry = create_rounded_entry_field(self, "Email Address :", self.email_var)
        self.password_entry = create_rounded_entry_field(self, "Password:", self.password_var, is_password=True)

        # Buttons using custom styled buttons
        button_frame = tk.Frame(self, bg=LIGHT_BG)
        button_frame.pack(pady=20)

        self.login_button_canvas = create_styled_button(button_frame, "LOGIN", self.login_user, PUP_RED, PUP_GOLD)
        self.login_button_canvas.pack(pady=5)

        self.register_button_canvas = create_styled_button(button_frame, "Register Here", self.go_to_register, BUTTON_BLUE_DARK, BUTTON_BLUE_LIGHT)
        self.register_button_canvas.pack(pady=5)

    def login_user(self):
        email = self.email_var.get().strip()
        password = self.password_var.get()

        if not email or not password:
            messagebox.showerror("Login Error", "Email and Password are required.")
            return

        user_data = self.db.fetch_one("SELECT id, name, password FROM users WHERE email = ?", (email,))

        if user_data:
            user_id, name, hashed_password = user_data
            if check_password(password, hashed_password):
                messagebox.showinfo("Login Success", f"Welcome, {name}!")
                self.controller.set_current_user(user_id)
                self.controller.show_frame("HomeScreen") # Transition to home screen
                self.clear_fields()
            else:
                messagebox.showerror("Login Error", "Invalid email or password.")
        else:
            messagebox.showerror("Login Error", "Invalid email or password.")

    def go_to_register(self):
        self.controller.show_frame("RegisterScreen")

    def clear_fields(self):
        self.email_var.set("")
        self.password_var.set("")

