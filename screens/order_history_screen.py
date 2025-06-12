import tkinter as tk
from tkinter import messagebox
from utils.helpers import (
    load_image, PUP_RED, PUP_GOLD, LIGHT_BG, WHITE_BG, GLOBAL_FONT, GLOBAL_FONT_BOLD,
    TITLE_FONT, HEADER_FONT, BORDER_COLOR, CART_ICON_PATH, USER_ICON_PATH, GRAY_TEXT,
    create_rounded_rectangle
)
class OrderHistoryScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=WHITE_BG) # Make screen background uniformly white
        self.controller = controller
        self.db = self.controller.get_db()

        self.order_list_window_id = None

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

        # --- Order History Header (Custom Canvas Drawing) ---
        header_canvas = tk.Canvas(self, width=250, height=40, bd=0, highlightthickness=0, bg=WHITE_BG) # <--- Changed to WHITE_BG
        header_canvas.pack(pady=10)
        create_rounded_rectangle(header_canvas, 1, 1, 249, 39, radius=20,
                                 fill=PUP_GOLD, outline=PUP_RED, width=2)
        header_canvas.create_text(125, 20, text="Order History", font=TITLE_FONT, fill=PUP_RED, anchor="center")


        # --- Order Table Header ---
        header_frame = tk.Frame(self, bg=WHITE_BG) # <--- Changed to WHITE_BG
        header_frame.pack(fill="x", padx=10, pady=(10, 3))

        tk.Label(header_frame, text="Ref No.", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=WHITE_BG, bd=0, relief="flat").pack(side="left", expand=True) # <--- Changed to WHITE_BG
        tk.Label(header_frame, text="Order\nstatus", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=WHITE_BG, bd=0, relief="flat").pack(side="left", expand=True) # <--- Changed to WHITE_BG
        tk.Label(header_frame, text="Quantity", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=WHITE_BG, bd=0, relief="flat").pack(side="left", expand=True) # <--- Changed to WHITE_BG
        tk.Label(header_frame, text="Payment", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=WHITE_BG, bd=0, relief="flat").pack(side="left", expand=True) # <--- Changed to WHITE_BG

        # --- Scrollable Area for Order Items ---
        self.order_canvas = tk.Canvas(self, bg=WHITE_BG, highlightthickness=0) # <--- Changed to WHITE_BG
        self.order_canvas.pack(side="left", fill="both", expand=True, padx=10)

        self.order_scrollbar = tk.Scrollbar(self.order_canvas, orient="vertical", command=self.order_canvas.yview) # Scrollbar is child of canvas
        self.order_scrollbar.pack(side="right", fill="y")

        self.order_canvas.configure(yscrollcommand=self.order_scrollbar.set)
        self.order_canvas.bind('<Configure>', self._on_canvas_configure)

        self.order_list_frame = tk.Frame(self.order_canvas, bg=WHITE_BG) # <--- Changed to WHITE_BG
        self.order_list_window_id = self.order_canvas.create_window(0, 0, window=self.order_list_frame, anchor="nw")

        self.load_orders()

    def _on_canvas_configure(self, event):
        self.order_canvas.configure(scrollregion=self.order_canvas.bbox("all"))
        canvas_width = event.width
        if self.order_list_window_id is not None:
            self.order_canvas.itemconfig(self.order_list_window_id, width=canvas_width)

    def load_orders(self):
        user_id = self.controller.get_current_user()
        if not user_id:
            messagebox.showwarning("Access Denied", "Please log in to view your order history.")
            self.controller.show_frame("LoginScreen")
            return

        for widget in self.order_list_frame.winfo_children():
            widget.destroy()

        orders = self.db.fetch_all("SELECT id, order_date, total_amount, status FROM orders WHERE user_id = ? ORDER BY order_date DESC", (user_id,))

        if not orders:
            tk.Label(self.order_list_frame, text="No orders found.", font=GLOBAL_FONT_BOLD, fg=GRAY_TEXT, bg=WHITE_BG).pack(pady=50) # <--- Changed to WHITE_BG
            return

        for order in orders:
            order_id, order_date, total_amount, status = order
            total_quantity = self.db.fetch_one("SELECT SUM(quantity) FROM order_items WHERE order_id = ?", (order_id,))[0] or 0

            order_frame = tk.Frame(self.order_list_frame, bg=WHITE_BG, bd=1, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1)
            order_frame.pack(fill="x", pady=3, padx=3)

            tk.Label(order_frame, text=order_id, font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG).pack(side="left", expand=True)
            tk.Label(order_frame, text=status, font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG).pack(side="left", expand=True)
            tk.Label(order_frame, text=total_quantity, font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG).pack(side="left", expand=True)
            tk.Label(order_frame, text=f"P{total_amount:.2f}", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG).pack(side="left", expand=True)
            
        # Scrolling Fix: Force update and trigger configure event after content loads
        self.order_list_frame.update_idletasks()
        self.order_canvas.config(scrollregion=self.order_canvas.bbox("all"))
        self.order_canvas.event_generate('<Configure>')
            
    def view_order_details(self, order_id):
        messagebox.showinfo("Order Details", f"Viewing details for Order ID: {order_id}")