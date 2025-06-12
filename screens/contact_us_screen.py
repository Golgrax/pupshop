import tkinter as tk
from tkinter import messagebox
import datetime
from utils.helpers import (
    load_image, PUP_RED, PUP_GOLD, LIGHT_BG, WHITE_BG, GLOBAL_FONT, GLOBAL_FONT_BOLD,
    TITLE_FONT, HEADER_FONT, BORDER_COLOR, CART_ICON_PATH, USER_ICON_PATH, GRAY_TEXT,
    create_rounded_entry_field, create_styled_button, create_rounded_rectangle
)

class ContactUsScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=WHITE_BG) # Make screen background uniformly white
        self.controller = controller
        self.db = self.controller.get_db()

        # --- Variables ---
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.message_var = tk.StringVar()

        # --- Top Bar (Icons) ---
        top_bar_frame = tk.Frame(self, bg=WHITE_BG) # <--- Changed to WHITE_BG
        top_bar_frame.pack(fill="x", pady=5, padx=10)

        # Cart Icon
        self.cart_icon_image = self.controller.cart_icon
        self.cart_button = tk.Button(top_bar_frame, image=self.cart_icon_image, bd=0, bg=WHITE_BG, # <--- Changed to WHITE_BG
                                     activebackground=WHITE_BG, command=lambda: self.controller.show_frame("ShoppingCartScreen"))
        self.cart_button.pack(side="right", padx=5)

        # User Profile Icon
        self.user_icon_image = self.controller.user_icon
        self.profile_button = tk.Button(top_bar_frame, image=self.user_icon_image, bd=0, bg=WHITE_BG, # <--- Changed to WHITE_BG
                                        activebackground=WHITE_BG, command=lambda: self.controller.show_frame("ProfileScreen"))
        self.profile_button.pack(side="right", padx=5)

        # Back Button
        back_button = tk.Button(top_bar_frame, text="< Back to Shop", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=WHITE_BG, bd=0, # <--- Changed to WHITE_BG
                                activebackground=WHITE_BG, activeforeground=PUP_GOLD,
                                command=lambda: self.controller.show_frame("HomeScreen"))
        back_button.pack(side="left", padx=5)

        # --- Contact Us Title ---
        tk.Label(self, text="Contact Us", font=HEADER_FONT, fg=PUP_RED, bg=WHITE_BG).pack(pady=(20, 10)) # <--- Changed to WHITE_BG

        # --- Input Fields ---
        self.name_entry = create_rounded_entry_field(self, "Name:", self.name_var, width=280)
        self.email_entry = create_rounded_entry_field(self, "Email Address :", self.email_var, width=280)

        tk.Label(self, text="Message ?", font=GLOBAL_FONT, fg=PUP_RED, bg=WHITE_BG).pack(anchor="w", padx=15, pady=(5, 0)) # <--- Changed to WHITE_BG
        
        # Custom drawing for Text widget border
        message_frame = tk.Frame(self, bg=WHITE_BG) # <--- Changed to WHITE_BG
        message_frame.pack(padx=15, pady=(0, 5))

        message_canvas = tk.Canvas(message_frame, width=280, height=120, bd=0, highlightthickness=0, bg=WHITE_BG) # <--- Changed to WHITE_BG
        message_canvas.pack()
        
        # Draw the rounded rectangle border for the message box
        create_rounded_rectangle(message_canvas, 1, 1, 279, 119, radius=15, fill="white", outline=PUP_GOLD, width=2)

        self.message_text = tk.Text(message_canvas, font=GLOBAL_FONT, relief="flat", bd=0,
                                    bg="white", fg="gray", insertbackground=PUP_RED)
        self.message_text.place(x=5, y=5, width=270, height=110)


        # --- Submit Button (Custom Styled Button) ---
        submit_button_frame = tk.Frame(self, bg=WHITE_BG) # <--- Changed to WHITE_BG
        submit_button_frame.pack(pady=15)
        self.submit_button_canvas = create_styled_button(submit_button_frame, "Submit", self.submit_message, PUP_RED, PUP_GOLD, width=120, height=30)
        self.submit_button_canvas.pack()

        self.load_user_info()

    def load_user_info(self):
        user_id = self.controller.get_current_user()
        if user_id:
            user_data = self.db.fetch_one("SELECT name, email FROM users WHERE id = ?", (user_id,))
            if user_data:
                self.name_var.set(user_data[0])
                self.email_var.set(user_data[1])

    def submit_message(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        message = self.message_text.get("1.0", tk.END).strip()

        if not name or not email or not message:
            messagebox.showerror("Submission Error", "All fields are required.")
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Submission Error", "Please enter a valid email address.")
            return

        user_id = self.controller.get_current_user()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        success = self.db.execute_query(
            "INSERT INTO contact_messages (user_id, name, email, message, timestamp) VALUES (?, ?, ?, ?, ?)",
            (user_id, name, email, message, timestamp)
        )

        if success:
            messagebox.showinfo("Success", "Your message has been sent!")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Failed to send message. Please try again.")

    def clear_fields(self):
        self.name_var.set("")
        self.email_var.set("")
        self.message_text.delete("1.0", tk.END)
        self.load_user_info()