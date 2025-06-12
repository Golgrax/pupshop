import tkinter as tk
from tkinter import messagebox
from utils.helpers import (
    load_image, PUP_RED, LIGHT_BG, WHITE_BG, BORDER_COLOR, PUP_CAMPUS_PATH, TITLE_FONT,
    GLOBAL_FONT, GLOBAL_FONT_BOLD, CART_ICON_PATH, USER_ICON_PATH, GRAY_TEXT,
    HEADER_FONT, PUP_GOLD
)
import os

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=WHITE_BG) # Make screen background uniformly white
        self.controller = controller
        self.db = self.controller.get_db()

        self.product_list_window_id = None

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

        # Create a main_content_area frame that will hold the scrollable list and the checkout button
        main_content_area = tk.Frame(self, bg=WHITE_BG) # Use WHITE_BG
        main_content_area.pack(fill="both", expand=True)

        # --- Campus Banner ---
        self.campus_banner_image = load_image(PUP_CAMPUS_PATH, (300, 120))
        self.campus_banner_label = tk.Label(main_content_area, image=self.campus_banner_image, bg=WHITE_BG) # Changed to WHITE_BG, child of main_content_area
        self.campus_banner_label.pack(pady=5)

        # --- Shopping Cart Title ---
        self.shopping_cart_title = tk.Label(main_content_area, text="Shopping cart", font=TITLE_FONT, fg=PUP_RED, bg=WHITE_BG, anchor="w") # Changed to WHITE_BG, child of main_content_area
        self.shopping_cart_title.pack(fill="x", padx=10, pady=(5, 5))

        # --- Shop Sections (e.g., StudywithStyle) ---
        self.study_with_style_frame = tk.Frame(main_content_area, bg=WHITE_BG) # Changed to WHITE_BG, child of main_content_area
        self.study_with_style_frame.pack(fill="x", padx=10, pady=5)

        self.checkbox_study = tk.BooleanVar(value=True)
        self.checkbox_study_btn = tk.Checkbutton(self.study_with_style_frame, variable=self.checkbox_study,
                                                 bg=WHITE_BG, activebackground=WHITE_BG, bd=0) # Changed to WHITE_BG
        self.checkbox_study_btn.pack(side="left", padx=(0, 5))
        tk.Label(self.study_with_style_frame, text="StudywithStyle", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=WHITE_BG).pack(side="left") # Changed to WHITE_BG


        # --- Product List (using a scrollable canvas) ---
        self.product_canvas = tk.Canvas(main_content_area, bg=WHITE_BG, highlightthickness=0) # Changed to WHITE_BG, child of main_content_area
        self.product_canvas.pack(side="top", fill="both", expand=True, padx=10, pady=5) # Ensure it takes top portion of main_content_area

        self.product_scrollbar = tk.Scrollbar(self.product_canvas, orient="vertical", command=self.product_canvas.yview) # Scrollbar is child of canvas
        self.product_scrollbar.pack(side="right", fill="y")

        self.product_canvas.configure(yscrollcommand=self.product_scrollbar.set)
        self.product_canvas.bind('<Configure>', self._on_canvas_configure)

        self.product_list_frame = tk.Frame(self.product_canvas, bg=WHITE_BG) # Changed to WHITE_BG
        self.product_list_window_id = self.product_canvas.create_window(0, 0, window=self.product_list_frame, anchor="nw")

        self.load_products()

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
        self.product_canvas.configure(scrollregion=self.product_canvas.bbox("all"))
        canvas_width = event.width
        if self.product_list_window_id is not None:
            self.product_canvas.itemconfig(self.product_list_window_id, width=canvas_width)

    def load_products(self):
        for widget in self.product_list_frame.winfo_children():
            widget.destroy()

        products = self.db.fetch_all("SELECT id, name, price, image_path, sales_count FROM products ORDER BY name")

        for product in products:
            product_id, name, price, image_path, sales_count = product
            product_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images', image_path)
            
            product_frame = tk.Frame(self.product_list_frame, bg=WHITE_BG, bd=1, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1)
            product_frame.pack(fill="x", pady=3, padx=3)

            left_section = tk.Frame(product_frame, bg=WHITE_BG)
            left_section.pack(side="left", padx=3, pady=3)

            img = load_image(product_image_path, (60, 60))
            if img:
                img_label = tk.Label(left_section, image=img, bg=WHITE_BG)
                img_label.image = img
                img_label.pack(side="left", padx=3)
            else:
                tk.Label(left_section, text="[No Image]", font=GLOBAL_FONT, bg=WHITE_BG).pack(side="left", padx=3)

            details_section = tk.Frame(product_frame, bg=WHITE_BG)
            details_section.pack(side="left", fill="x", expand=True, padx=3)

            tk.Label(details_section, text=name, font=GLOBAL_FONT_BOLD, fg=GRAY_TEXT, bg=WHITE_BG, wraplength=120, justify="left").pack(anchor="w")
            tk.Label(details_section, text=f"P{price:.2f}", font=GLOBAL_FONT, fg=PUP_RED, bg=WHITE_BG).pack(anchor="w", pady=(1,0))

            quantity_control_frame = tk.Frame(product_frame, bg=WHITE_BG)
            quantity_control_frame.pack(side="right", padx=3, pady=3)

            current_quantity = self.controller.get_cart().get(product_id, 0)
            quantity_label = tk.Label(quantity_control_frame, text=f"{current_quantity}", font=GLOBAL_FONT_BOLD, bg=WHITE_BG, fg=PUP_RED)
            quantity_label.pack(side="right", padx=1) # Reduced padx

            add_button = tk.Button(quantity_control_frame, text="+", font=GLOBAL_FONT_BOLD, fg="white", bg=PUP_RED,
                                   activebackground=PUP_RED, activeforeground="white", bd=0, relief="flat", width=2, height=1, # Added width/height
                                   command=lambda p_id=product_id, q_label=quantity_label: self.add_item_to_cart_and_refresh(p_id, q_label))
            add_button.pack(side="right")
            
            product_frame.bind("<Button-1>", lambda e, p_id=product_id: self.go_to_product_detail(p_id))
            for child in product_frame.winfo_children():
                child.bind("<Button-1>", lambda e, p_id=product_id: self.go_to_product_detail(p_id))

        # --- Scrolling Fix: Force update and trigger configure event after content loads ---
        self.product_list_frame.update_idletasks() # Force geometry calculations
        self.product_canvas.config(scrollregion=self.product_canvas.bbox("all")) # Set scrollregion based on content
        # No need for event_generate here, as bbox("all") implies updates.


    def add_item_to_cart_and_refresh(self, product_id, quantity_label):
        self.controller.add_to_cart(product_id, 1)
        current_quantity = self.controller.get_cart().get(product_id, 0)
        quantity_label.config(text=f"{current_quantity}")

    def go_to_product_detail(self, product_id):
        self.controller.show_frame("ProductDetailScreen", product_id=product_id)

    def go_to_checkout(self):
        if not self.controller.get_cart():
            messagebox.showwarning("Checkout", "Your shopping cart is empty!")
            return
        self.controller.show_frame("CheckoutScreen")