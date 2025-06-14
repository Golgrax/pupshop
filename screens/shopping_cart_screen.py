import tkinter as tk
from tkinter import messagebox
from utils.helpers import (
    load_image, PUP_RED, PUP_GOLD, LIGHT_BG, WHITE_BG, GLOBAL_FONT, GLOBAL_FONT_BOLD,
    TITLE_FONT, HEADER_FONT, BORDER_COLOR, CART_ICON_PATH, USER_ICON_PATH, GRAY_TEXT
)
import os

class ShoppingCartScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=WHITE_BG) # Make screen background uniformly white
        self.controller = controller
        self.db = self.controller.get_db()

        self.cart_list_window_id = None

        # --- Top Bar (Icons) ---
        top_bar_frame = tk.Frame(self, bg=WHITE_BG) # Changed to WHITE_BG
        top_bar_frame.pack(fill="x", pady=5, padx=10)

        # Cart Icon
        self.cart_icon_image = self.controller.cart_icon
        self.cart_button = tk.Button(top_bar_frame, image=self.cart_icon_image, bd=0, bg=WHITE_BG, # Changed to WHITE_BG
                                     activebackground=WHITE_BG, command=lambda: self.controller.show_frame("ShoppingCartScreen"))
        self.cart_button.pack(side="right", padx=5)

        # User Profile Icon
        self.user_icon_image = self.controller.user_icon
        self.profile_button = tk.Button(top_bar_frame, image=self.user_icon_image, bd=0, bg=WHITE_BG, # Changed to WHITE_BG
                                        activebackground=WHITE_BG, command=lambda: self.controller.show_frame("ProfileScreen"))
        self.profile_button.pack(side="right", padx=5)

        # Back Button
        back_button = tk.Button(top_bar_frame, text="< Back to Shop", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=WHITE_BG, bd=0, # Changed to WHITE_BG
                                activebackground=WHITE_BG, activeforeground=PUP_GOLD,
                                command=lambda: self.controller.show_frame("HomeScreen"))
        back_button.pack(side="left", padx=5)

        # Create a main_content_area frame that will hold the scrollable list and the checkout button
        main_content_area = tk.Frame(self, bg=WHITE_BG) # Use WHITE_BG
        main_content_area.pack(fill="both", expand=True)

        # --- Shopping Cart Title ---
        self.shopping_cart_title = tk.Label(main_content_area, text="Shopping cart", font=TITLE_FONT, fg=PUP_RED, bg=WHITE_BG, anchor="w") # Changed to WHITE_BG, child of main_content_area
        self.shopping_cart_title.pack(fill="x", padx=10, pady=(5, 5))

        # --- Scrollable Area for Cart Items ---
        self.cart_canvas = tk.Canvas(main_content_area, bg=WHITE_BG, highlightthickness=0) # Changed to WHITE_BG, child of main_content_area
        self.cart_canvas.pack(side="top", fill="both", expand=True, padx=10, pady=5)

        self.cart_scrollbar = tk.Scrollbar(self.cart_canvas, orient="vertical", command=self.cart_canvas.yview) # Scrollbar is child of canvas
        self.cart_scrollbar.pack(side="right", fill="y")

        self.cart_canvas.configure(yscrollcommand=self.cart_scrollbar.set)
        self.cart_canvas.bind('<Configure>', self._on_canvas_configure)

        self.cart_items_frame = tk.Frame(self.cart_canvas, bg=WHITE_BG) # Changed to WHITE_BG
        self.cart_list_window_id = self.cart_canvas.create_window(0, 0, window=self.cart_items_frame, anchor="nw")

        self.cart_item_widgets = {}

        self.load_cart_items()

        # --- CHECK OUT Button ---
        main_content_area.update_idletasks() # Force update to compute accurate main_content_area height
        # Pack this button frame at the bottom of the main_content_area frame.
        self.checkout_button_frame = tk.Frame(main_content_area, bg=WHITE_BG) # Changed to WHITE_BG
        self.checkout_button_frame.pack(side="bottom", fill="x", pady=5)
        self.checkout_button = tk.Button(self.checkout_button_frame, text="CHECK OUT", font=HEADER_FONT,
                                         fg=PUP_RED, bg=PUP_GOLD, activebackground=PUP_RED,
                                         activeforeground="white", bd=0, relief="flat",
                                         command=self.go_to_checkout)
        self.checkout_button.pack(pady=5)

    def _on_canvas_configure(self, event):
        self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))
        canvas_width = event.width
        if self.cart_list_window_id is not None:
            self.cart_canvas.itemconfig(self.cart_list_window_id, width=canvas_width)

    def load_cart_items(self):
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()
        self.cart_item_widgets = {}

        current_cart = self.controller.get_cart()
        if not current_cart:
            tk.Label(self.cart_items_frame, text="Your cart is empty!", font=GLOBAL_FONT_BOLD, fg=GRAY_TEXT, bg=WHITE_BG).pack(pady=50) # Changed to WHITE_BG
            return

        product_ids = ",".join(map(str, current_cart.keys()))
        products_in_cart = self.db.fetch_all(f"SELECT id, name, price, image_path FROM products WHERE id IN ({product_ids})")

        for product in products_in_cart:
            product_id, name, price, image_path = product
            quantity = current_cart.get(product_id, 0)
            if quantity == 0: continue

            product_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images', image_path)
            
            item_frame = tk.Frame(self.cart_items_frame, bg=WHITE_BG, bd=1, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1)
            item_frame.pack(fill="x", pady=3, padx=3)

            left_section = tk.Frame(item_frame, bg=WHITE_BG)
            left_section.pack(side="left", padx=3, pady=3)

            img = load_image(product_image_path, (60, 60)) # Reduced image size
            if img:
                img_label = tk.Label(left_section, image=img, bg=WHITE_BG)
                img_label.image = img
                img_label.pack(side="left", padx=3)
            else:
                tk.Label(left_section, text="[No Image]", font=GLOBAL_FONT, bg=WHITE_BG).pack(side="left", padx=3)

            details_section = tk.Frame(item_frame, bg=WHITE_BG)
            details_section.pack(side="left", fill="x", expand=True, padx=3)

            tk.Label(details_section, text=name, font=GLOBAL_FONT_BOLD, fg=GRAY_TEXT, bg=WHITE_BG, wraplength=120, justify="left").pack(anchor="w") # Reduced wraplength
            tk.Label(details_section, text=f"P{price:.2f}", font=GLOBAL_FONT, fg=PUP_RED, bg=WHITE_BG).pack(anchor="w", pady=(1,0))

            quantity_control_frame = tk.Frame(item_frame, bg=WHITE_BG)
            quantity_control_frame.pack(side="right", padx=3, pady=3)

            # Quantity buttons (+/-) and label
            minus_button = tk.Button(quantity_control_frame, text="-", font=GLOBAL_FONT_BOLD, fg="white", bg=PUP_RED, bd=0, relief="flat", width=2, height=1, # Added width/height
                                     command=lambda p_id=product_id: self.update_quantity(p_id, -1))
            minus_button.pack(side="left")

            quantity_label = tk.Label(quantity_control_frame, text=f"{quantity}", font=GLOBAL_FONT_BOLD, bg=WHITE_BG, fg=PUP_RED)
            quantity_label.pack(side="left", padx=1) # Reduced padx

            plus_button = tk.Button(quantity_control_frame, text="+", font=GLOBAL_FONT_BOLD, fg="white", bg=PUP_RED, bd=0, relief="flat", width=2, height=1, # Added width/height
                                    command=lambda p_id=product_id: self.update_quantity(p_id, 1))
            plus_button.pack(side="left")

            self.cart_item_widgets[product_id] = {
                "frame": item_frame,
                "quantity_label": quantity_label,
                "image_label": img_label
            }
            
            # The 'X' remove button (make it a square button like +/-)
            remove_button = tk.Button(item_frame, text="X", font=GLOBAL_FONT_BOLD, fg="gray", bg=WHITE_BG, bd=0, relief="flat", width=2, height=1, # Added width/height
                                      command=lambda p_id=product_id: self.remove_item(p_id))
            remove_button.pack(side="right", padx=3, anchor="n")


        # --- Scrolling Fix: Force update and trigger configure event after content loads ---
        self.cart_items_frame.update_idletasks() # Force geometry calculations
        self.cart_canvas.config(scrollregion=self.cart_canvas.bbox("all")) # Set scrollregion based on content
        # No need for event_generate here, as bbox("all") implies updates.


    def update_quantity(self, product_id, change):
        current_cart = self.controller.get_cart()
        new_quantity = current_cart.get(product_id, 0) + change

        if new_quantity <= 0:
            self.remove_item(product_id)
        else:
            self.controller.update_cart_quantity(product_id, new_quantity)
            if product_id in self.cart_item_widgets:
                self.cart_item_widgets[product_id]["quantity_label"].config(text=str(new_quantity))

    def remove_item(self, product_id):
        confirm = messagebox.askyesno("Remove Item", "Are you sure you want to remove this item from your cart?")
        if confirm:
            self.controller.remove_from_cart(product_id)
            if product_id in self.cart_item_widgets:
                self.cart_item_widgets[product_id]["frame"].destroy()
                del self.cart_item_widgets[product_id]
            messagebox.showinfo("Cart Update", "Item removed successfully.")
            self.load_cart_items()

    def go_to_checkout(self):
        if not self.controller.get_cart():
            messagebox.showwarning("Checkout", "Your shopping cart is empty!")
            return
        self.controller.show_frame("CheckoutScreen")