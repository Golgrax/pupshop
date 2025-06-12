import tkinter as tk
from tkinter import messagebox
import os
# import time # This import isn't actually used, can be removed

# Import database and helper utilities
from utils.database import Database
from utils.helpers import (
    load_image, PUP_RED, PUP_GOLD, LIGHT_BG, WHITE_BG, PUP_LOGO_PATH,
    QUESTION_MARK_PATH, CART_ICON_PATH, USER_ICON_PATH, create_rounded_rectangle,
    HEADER_FONT, TITLE_FONT, GLOBAL_FONT
)

# Import screen modules
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.home_screen import HomeScreen
from screens.product_detail_screen import ProductDetailScreen
from screens.shopping_cart_screen import ShoppingCartScreen
from screens.checkout_screen import CheckoutScreen
from screens.order_history_screen import OrderHistoryScreen
from screens.profile_screen import ProfileScreen
from screens.contact_us_screen import ContactUsScreen
from screens.inventory_management_screen import InventoryManagementScreen # For future admin features

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PUP E-Shop")
        self.geometry("360x640") # A common modern phone portrait resolution
        self.resizable(False, False)
        self.configure(bg=LIGHT_BG)

        # --- IMPORTANT FIX: Initialize core attributes first ---
        self.db = Database()
        self.db.create_tables() # This might trigger product seeding, which might use image paths etc.

        self.current_user_id = None
        self.shopping_cart = {} # {product_id: quantity}
        self.current_frame_name = None # <--- Initialize this *before* any frames are created

        # Load common images once (needs to be after `self.db` for pathing)
        self.pup_logo = load_image(PUP_LOGO_PATH, (120, 120))
        self.question_mark_icon = load_image(QUESTION_MARK_PATH, (40, 40))
        self.cart_icon = load_image(CART_ICON_PATH, (30, 30))
        self.user_icon = load_image(USER_ICON_PATH, (30, 30))
        # --- End of crucial initializations ---

        # To simulate the rounded phone screen border, we draw a rounded rectangle on a canvas
        # and place the main content frame inside it. This is a common workaround.
        self.outer_canvas = tk.Canvas(self, width=500, height=800, bd=0, highlightthickness=0, bg=LIGHT_BG)
        self.outer_canvas.pack(fill="both", expand=True)
        # Draw the outer rounded rectangle (simulating device border)
        self.outer_canvas = tk.Canvas(self, width=360, height=640, bd=0, highlightthickness=0, bg=LIGHT_BG)
        self.outer_canvas.pack(fill="both", expand=True)
        self.outer_canvas.create_oval(5, 5, 355, 635, fill=WHITE_BG, outline=PUP_RED, width=2)
        self.container = tk.Frame(self.outer_canvas, bg=LIGHT_BG)
        self.container.place(x=15, y=15, width=330, height=610) # Adjusted for the new outer size

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # List all screen classes to initialize
        screen_classes = [
            LoginScreen,
            RegisterScreen,
            HomeScreen,
            ProductDetailScreen,
            ShoppingCartScreen,
            CheckoutScreen,
            OrderHistoryScreen,
            ProfileScreen,
            ContactUsScreen,
            InventoryManagementScreen,
        ]

        for F in screen_classes:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Initial screen: Login or Register
        self.show_frame("LoginScreen", animate=False) # No animation for initial display

        # Common help button (bottom right)
        self.help_button = tk.Button(self.outer_canvas, image=self.question_mark_icon, command=self.show_help, bd=0, bg=LIGHT_BG,
                                     activebackground=LIGHT_BG)
        self.help_button.place(relx=0.9, rely=0.95, anchor="se", x=-10, y=-10)


    def show_frame(self, page_name, product_id=None, animate=True):
        """
        Switches between frames with an optional slide animation.
        """
        new_frame = self.frames[page_name]

        # Pass data to specific screens if needed
        if page_name == "ProductDetailScreen" and product_id is not None:
            new_frame.load_product(product_id)
        elif page_name == "ShoppingCartScreen":
            new_frame.load_cart_items()
        elif page_name == "OrderHistoryScreen":
            new_frame.load_orders()
        elif page_name == "ProfileScreen":
            new_frame.load_addresses()
        elif page_name == "InventoryManagementScreen":
             new_frame.load_products() # Assuming this screen loads products

        if self.current_frame_name is None or not animate:
            # No animation if it's the first frame or animation is disabled
            new_frame.tkraise()
            self.current_frame_name = page_name
            return

        old_frame = self.frames[self.current_frame_name]
        width = self.container.winfo_width() # Get current width of the container

        # Place the new frame to the right of the old frame for a left-swipe effect
        new_frame.place(x=width, y=0, relwidth=1, relheight=1)
        new_frame.tkraise() # Bring new frame to top

        # Animation loop
        step = 25 # Pixels to move per step
        delay = 10 # Milliseconds per step

        def animate_swipe():
            current_x_old = old_frame.winfo_x()
            current_x_new = new_frame.winfo_x()

            if current_x_new > 0:
                # Move both frames to the left
                old_frame.place(x=current_x_old - step, y=0, relwidth=1, relheight=1)
                new_frame.place(x=current_x_new - step, y=0, relwidth=1, relheight=1)
                self.after(delay, animate_swipe)
            else:
                # Animation finished, snap to final positions
                old_frame.place_forget() # Hide old frame
                new_frame.place(x=0, y=0, relwidth=1, relheight=1) # Ensure new frame is correctly placed
                self.current_frame_name = page_name

        animate_swipe()


    def set_current_user(self, user_id):
        self.current_user_id = user_id

    def get_current_user(self):
        return self.current_user_id

    def get_db(self):
        return self.db

    def get_cart(self):
        return self.shopping_cart

    def add_to_cart(self, product_id, quantity=1):
        if product_id in self.shopping_cart:
            self.shopping_cart[product_id] += quantity
        else:
            self.shopping_cart[product_id] = quantity
        messagebox.showinfo("Cart Update", f"Added {quantity} item(s) to cart.")

    def remove_from_cart(self, product_id):
        if product_id in self.shopping_cart:
            del self.shopping_cart[product_id]
            messagebox.showinfo("Cart Update", "Item removed from cart.")

    def update_cart_quantity(self, product_id, quantity):
        if product_id in self.shopping_cart:
            if quantity > 0:
                self.shopping_cart[product_id] = quantity
            else:
                self.remove_from_cart(product_id)

    def clear_cart(self):
        self.shopping_cart = {}

    def show_help(self):
        messagebox.showinfo("Help", "This is the help section of the PUP E-Shop app. "
                                   "Navigate through the different screens using the buttons and icons.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
