import tkinter as tk
from tkinter import messagebox
from utils.helpers import (
    load_image, PUP_RED, PUP_GOLD, LIGHT_BG, WHITE_BG, GLOBAL_FONT, GLOBAL_FONT_BOLD,
    TITLE_FONT, HEADER_FONT, ADD_TO_CART_BTN_PATH, BUY_NOW_BTN_PATH, BORDER_COLOR,
    CART_ICON_PATH, USER_ICON_PATH, GRAY_TEXT
)
import os

class ProductDetailScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=WHITE_BG) # Make screen background uniformly white
        self.controller = controller
        self.db = self.controller.get_db()
        self.current_product = None

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
        back_button = tk.Button(top_bar_frame, text="< Back", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=WHITE_BG, bd=0, # Changed to WHITE_BG
                                activebackground=WHITE_BG, activeforeground=PUP_GOLD,
                                command=lambda: self.controller.show_frame("HomeScreen"))
        back_button.pack(side="left", padx=5)


        # --- Product Image ---
        self.product_display_image = None
        self.product_image_label = tk.Label(self, bg=WHITE_BG) # Changed to WHITE_BG
        self.product_image_label.pack(pady=5)

        # --- Price and Sold Count ---
        price_sold_frame = tk.Frame(self, bg=WHITE_BG) # Changed to WHITE_BG
        price_sold_frame.pack(fill="x", padx=15, pady=3)

        self.price_label = tk.Label(price_sold_frame, text="P0.00", font=HEADER_FONT, fg=PUP_RED, bg=WHITE_BG) # Changed to WHITE_BG
        self.price_label.pack(side="left")
        self.sold_label = tk.Label(price_sold_frame, text="0 sold", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG) # Changed to WHITE_BG
        self.sold_label.pack(side="right")

        # --- Product Name ---
        self.name_label = tk.Label(self, text="", font=TITLE_FONT, fg=GRAY_TEXT, bg=WHITE_BG, wraplength=280, justify="left") # Changed to WHITE_BG
        self.name_label.pack(fill="x", padx=15, pady=(0, 5))

        # --- Separator Line ---
        tk.Frame(self, bg=BORDER_COLOR, height=1).pack(fill="x", padx=10, pady=5)

        # --- Details Section (Guaranteed, Free Return, etc.) ---
        details_frame = tk.Frame(self, bg=WHITE_BG) # Changed to WHITE_BG
        details_frame.pack(fill="x", padx=15, pady=3)

        tk.Label(details_frame, text="Guaranteed to get by : 17-19 May", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG).pack(anchor="w", pady=1) # Changed to WHITE_BG
        tk.Label(details_frame, text="Free & Easy Return", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG).pack(anchor="w", pady=1) # Changed to WHITE_BG
        tk.Label(details_frame, text="Merchandise Protection", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG).pack(anchor="w", pady=1) # Changed to WHITE_BG

        # --- Separator Line ---
        tk.Frame(self, bg=BORDER_COLOR, height=1).pack(fill="x", padx=10, pady=5)

        # --- Select Variation (Placeholder) ---
        tk.Label(self, text="Select variation", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=WHITE_BG).pack(anchor="w", padx=15, pady=(0, 3)) # Changed to WHITE_BG
        
        variation_frame = tk.Frame(self, bg=WHITE_BG) # Changed to WHITE_BG
        variation_frame.pack(fill="x", padx=15, pady=(0, 5))

        tk.Label(variation_frame, text="36", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG, width=4, relief="solid", bd=1).pack(side="left", padx=3)
        tk.Label(variation_frame, text="37", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG, width=4, relief="solid", bd=1).pack(side="left", padx=3)
        tk.Label(variation_frame, text="38", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG, width=4, relief="solid", bd=1).pack(side="left", padx=3)

        # --- Separator Line ---
        tk.Frame(self, bg=BORDER_COLOR, height=1).pack(fill="x", padx=10, pady=5)

        # --- Product Rating (Simulated) ---
        rating_frame = tk.Frame(self, bg=WHITE_BG) # Changed to WHITE_BG
        rating_frame.pack(fill="x", padx=15, pady=(0, 10))

        tk.Label(rating_frame, text="4.9", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=WHITE_BG).pack(side="left") # Changed to WHITE_BG
        tk.Label(rating_frame, text="★", font=(GLOBAL_FONT[0], 12), fg=PUP_GOLD, bg=WHITE_BG).pack(side="left", padx=(0, 3)) # Changed to WHITE_BG
        self.rating_text_label = tk.Label(rating_frame, text="Product rating (100)", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG) # Changed to WHITE_BG
        self.rating_text_label.pack(side="left")


        # --- Action Buttons ---
        button_actions_frame = tk.Frame(self, bg=WHITE_BG) # Changed to WHITE_BG
        button_actions_frame.pack(fill="x", pady=5)

        # Load button images (ADJUSTED SIZE to match create_styled_button, as these are meant to be images)
        self.add_to_cart_img = load_image(ADD_TO_CART_BTN_PATH, (120, 30))
        self.buy_now_img = load_image(BUY_NOW_BTN_PATH, (120, 30))

        # Add to Cart Button
        self.add_to_cart_button = tk.Button(button_actions_frame, image=self.add_to_cart_img, bd=0, bg=WHITE_BG, # Changed to WHITE_BG
                                            activebackground=WHITE_BG, command=self.add_to_cart_action)
        self.add_to_cart_button.image = self.add_to_cart_img
        self.add_to_cart_button.pack(side="left", padx=(10, 5))

        # Buy Now Button
        self.buy_now_button = tk.Button(button_actions_frame, image=self.buy_now_img, bd=0, bg=WHITE_BG, # Changed to WHITE_BG
                                        activebackground=WHITE_BG, command=self.buy_now_action)
        self.buy_now_button.image = self.buy_now_img
        self.buy_now_button.pack(side="left", padx=(5, 0))


    def load_product(self, product_id):
        product_data = self.db.fetch_one("SELECT id, name, price, image_path, sales_count, description, rating FROM products WHERE id = ?", (product_id,))
        if product_data:
            self.current_product = {
                "id": product_data[0],
                "name": product_data[1],
                "price": product_data[2],
                "image_path": product_data[3],
                "sales_count": product_data[4],
                "description": product_data[5],
                "rating": product_data[6]
            }
            self.price_label.config(text=f"P{self.current_product['price']:.2f}")
            self.sold_label.config(text=f"{self.current_product['sales_count']} sold")
            self.name_label.config(text=self.current_product['name'])
            self.rating_text_label.config(text=f"Product rating ({int(self.current_product['rating']*20)} ratings)")

            product_image_full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images', self.current_product['image_path'])
            self.product_display_image = load_image(product_image_full_path, (180, 180))
            self.product_image_label.config(image=self.product_display_image)
            self.product_image_label.image = self.product_display_image
        else:
            messagebox.showerror("Error", "Product not found!")
            self.controller.show_frame("HomeScreen")

    def add_to_cart_action(self):
        if self.current_product:
            self.controller.add_to_cart(self.current_product['id'], 1)
        else:
            messagebox.showwarning("Cart", "No product selected.")

    def buy_now_action(self):
        if self.current_product:
            self.controller.clear_cart()
            self.controller.add_to_cart(self.current_product['id'], 1)
            self.controller.show_frame("CheckoutScreen")
        else:
            messagebox.showwarning("Buy Now", "No product selected.")