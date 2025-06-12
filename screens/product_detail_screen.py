import tkinter as tk
from tkinter import messagebox
from utils.helpers import (
    load_image, PUP_RED, PUP_GOLD, LIGHT_BG, WHITE_BG, GLOBAL_FONT, GLOBAL_FONT_BOLD,
    TITLE_FONT, HEADER_FONT, ADD_TO_CART_BTN_PATH, BUY_NOW_BTN_PATH, BORDER_COLOR,
    CART_ICON_PATH, USER_ICON_PATH
)
import os

class ProductDetailScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=LIGHT_BG)
        self.controller = controller
        self.db = self.controller.get_db()
        self.current_product = None # Store loaded product data

        # --- Top Bar (Icons) ---
        top_bar_frame = tk.Frame(self, bg=LIGHT_BG)
        top_bar_frame.pack(fill="x", pady=10, padx=20)

        # Cart Icon
        self.cart_icon_image = self.controller.cart_icon
        self.cart_button = tk.Button(top_bar_frame, image=self.cart_icon_image, bd=0, bg=LIGHT_BG,
                                     activebackground=LIGHT_BG, command=lambda: self.controller.show_frame("ShoppingCartScreen"))
        self.cart_button.pack(side="right", padx=5)

        # User Profile Icon
        self.user_icon_image = self.controller.user_icon
        self.profile_button = tk.Button(top_bar_frame, image=self.user_icon_image, bd=0, bg=LIGHT_BG,
                                        activebackground=LIGHT_BG, command=lambda: self.controller.show_frame("ProfileScreen"))
        self.profile_button.pack(side="right", padx=5)

        # Back Button (optional, to go back to home screen)
        back_button = tk.Button(top_bar_frame, text="< Back", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=LIGHT_BG, bd=0,
                                activebackground=LIGHT_BG, activeforeground=PUP_GOLD,
                                command=lambda: self.controller.show_frame("HomeScreen"))
        back_button.pack(side="left", padx=5)


        # --- Product Image ---
        self.product_display_image = None # PhotoImage object
        self.product_image_label = tk.Label(self, bg=LIGHT_BG)
        self.product_image_label.pack(pady=10)

        # --- Price and Sold Count ---
        price_sold_frame = tk.Frame(self, bg=LIGHT_BG)
        price_sold_frame.pack(fill="x", padx=30, pady=5)

        self.price_label = tk.Label(price_sold_frame, text="P0.00", font=HEADER_FONT, fg=PUP_RED, bg=LIGHT_BG)
        self.price_label.pack(side="left")
        self.sold_label = tk.Label(price_sold_frame, text="0 sold", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=LIGHT_BG)
        self.sold_label.pack(side="right")

        # --- Product Name ---
        self.name_label = tk.Label(self, text="", font=TITLE_FONT, fg=GRAY_TEXT, bg=LIGHT_BG, wraplength=400, justify="left")
        self.name_label.pack(fill="x", padx=30, pady=(0, 10))

        # --- Separator Line ---
        tk.Frame(self, bg=BORDER_COLOR, height=1).pack(fill="x", padx=20, pady=10)

        # --- Details Section (Guaranteed, Free Return, etc.) ---
        details_frame = tk.Frame(self, bg=LIGHT_BG)
        details_frame.pack(fill="x", padx=30, pady=5)

        tk.Label(details_frame, text="Guaranteed to get by : 17-19 May", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=LIGHT_BG).pack(anchor="w", pady=2)
        tk.Label(details_frame, text="Free & Easy Return", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=LIGHT_BG).pack(anchor="w", pady=2)
        tk.Label(details_frame, text="Merchandise Protection", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=LIGHT_BG).pack(anchor="w", pady=2)

        # --- Separator Line ---
        tk.Frame(self, bg=BORDER_COLOR, height=1).pack(fill="x", padx=20, pady=10)

        # --- Select Variation (Placeholder for future functionality) ---
        tk.Label(self, text="Select variation", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=LIGHT_BG).pack(anchor="w", padx=30, pady=(0, 5))
        
        variation_frame = tk.Frame(self, bg=LIGHT_BG)
        variation_frame.pack(fill="x", padx=30, pady=(0, 10))

        # Example variations, could be radio buttons or option menus
        tk.Label(variation_frame, text="36", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG, width=5, relief="solid", bd=1).pack(side="left", padx=5)
        tk.Label(variation_frame, text="37", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG, width=5, relief="solid", bd=1).pack(side="left", padx=5)
        tk.Label(variation_frame, text="38", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=WHITE_BG, width=5, relief="solid", bd=1).pack(side="left", padx=5)

        # --- Separator Line ---
        tk.Frame(self, bg=BORDER_COLOR, height=1).pack(fill="x", padx=20, pady=10)

        # --- Product Rating (Simulated) ---
        rating_frame = tk.Frame(self, bg=LIGHT_BG)
        rating_frame.pack(fill="x", padx=30, pady=(0, 20))

        tk.Label(rating_frame, text="4.9", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=LIGHT_BG).pack(side="left")
        # Star icon placeholder (you could use a star image)
        tk.Label(rating_frame, text="★", font=(GLOBAL_FONT[0], 14), fg=PUP_GOLD, bg=LIGHT_BG).pack(side="left", padx=(0, 5))
        self.rating_text_label = tk.Label(rating_frame, text="Product rating (100)", font=GLOBAL_FONT, fg=GRAY_TEXT, bg=LIGHT_BG)
        self.rating_text_label.pack(side="left")


        # --- Action Buttons ---
        button_actions_frame = tk.Frame(self, bg=LIGHT_BG)
        button_actions_frame.pack(fill="x", pady=10)

        # Load button images
        self.add_to_cart_img = load_image(ADD_TO_CART_BTN_PATH, (180, 40))
        self.buy_now_img = load_image(BUY_NOW_BTN_PATH, (180, 40))

        # Add to Cart Button
        self.add_to_cart_button = tk.Button(button_actions_frame, image=self.add_to_cart_img, bd=0, bg=LIGHT_BG,
                                            activebackground=LIGHT_BG, command=self.add_to_cart_action)
        self.add_to_cart_button.image = self.add_to_cart_img # Keep reference
        self.add_to_cart_button.pack(side="left", padx=(30, 10))

        # Buy Now Button
        self.buy_now_button = tk.Button(button_actions_frame, image=self.buy_now_img, bd=0, bg=LIGHT_BG,
                                        activebackground=LIGHT_BG, command=self.buy_now_action)
        self.buy_now_button.image = self.buy_now_img # Keep reference
        self.buy_now_button.pack(side="left", padx=(10, 0))


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
            # Update UI elements
            self.price_label.config(text=f"P{self.current_product['price']:.2f}")
            self.sold_label.config(text=f"{self.current_product['sales_count']} sold")
            self.name_label.config(text=self.current_product['name'])
            self.rating_text_label.config(text=f"Product rating ({int(self.current_product['rating']*20)} ratings)") # Assuming 5-star max, scale to 100

            product_image_full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images', self.current_product['image_path'])
            self.product_display_image = load_image(product_image_full_path, (250, 250)) # Adjust size as needed
            self.product_image_label.config(image=self.product_display_image)
            self.product_image_label.image = self.product_display_image # Keep reference
        else:
            messagebox.showerror("Error", "Product not found!")
            self.controller.show_frame("HomeScreen") # Go back to home if product not found

    def add_to_cart_action(self):
        if self.current_product:
            # For simplicity, add 1 quantity. Could add a quantity selector.
            self.controller.add_to_cart(self.current_product['id'], 1)
        else:
            messagebox.showwarning("Cart", "No product selected.")

    def buy_now_action(self):
        if self.current_product:
            # Clear current cart and add this product, then go to checkout
            self.controller.clear_cart()
            self.controller.add_to_cart(self.current_product['id'], 1)
            self.controller.show_frame("CheckoutScreen")
        else:
            messagebox.showwarning("Buy Now", "No product selected.")
