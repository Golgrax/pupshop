import tkinter as tk
from tkinter import messagebox
import os

# Import database and helper utilities
from utils.database import Database
from utils.helpers import (
    load_image, PUP_RED, PUP_GOLD, LIGHT_BG, WHITE_BG, PUP_LOGO_PATH,
    QUESTION_MARK_PATH, CART_ICON_PATH, USER_ICON_PATH,
    HEADER_FONT, TITLE_FONT, GLOBAL_FONT, # These are initially defaults, will be updated by load_custom_fonts
    create_rounded_rectangle,
    load_custom_fonts # <--- IMPORT THE FONT LOADING FUNCTION
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
from screens.inventory_management_screen import InventoryManagementScreen

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PUP E-Shop")
        self.geometry("360x640")
        self.resizable(False, False)
        self.configure(bg=LIGHT_BG)

        # --- IMPORTANT FIX: Initialize core attributes first ---
        self.db = Database()
        self.db.create_tables()

        self.current_user_id = None
        self.shopping_cart = {}
        self.current_frame_name = None

        # Load common images once
        self.pup_logo = load_image(PUP_LOGO_PATH, (120, 120))
        self.question_mark_icon = load_image(QUESTION_MARK_PATH, (40, 40))
        self.cart_icon = load_image(CART_ICON_PATH, (30, 30))
        self.user_icon = load_image(USER_ICON_PATH, (30, 30))
        # --- End of crucial initializations ---

        # --- FONT LOADING FIX: Load custom fonts after Tkinter root is ready ---
        load_custom_fonts() # <--- CALL THE FONT LOADING FUNCTION HERE

        # --- CORRECTED CANVAS AND CONTAINER SETUP ---
        canvas_width = 360
        canvas_height = 640
        border_radius = 20

        self.outer_canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bd=0, highlightthickness=0, bg=LIGHT_BG)
        self.outer_canvas.pack(fill="both", expand=True)

        create_rounded_rectangle(self.outer_canvas, 5, 5, canvas_width - 5, canvas_height - 5,
                                 radius=border_radius, fill=WHITE_BG, outline=PUP_RED, width=2)

        container_x = 15
        container_y = 15
        container_width = canvas_width - 2 * container_x
        container_height = canvas_height - 2 * container_y

        self.container = tk.Frame(self.outer_canvas, bg=WHITE_BG)
        self.container.place(x=container_x, y=container_y, width=container_width, height=container_height)
        # --- END CORRECTED SETUP ---

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
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

        self.show_frame("LoginScreen", animate=False)

        self.help_button = tk.Button(self.outer_canvas, image=self.question_mark_icon, command=self.show_help, bd=0, bg=LIGHT_BG,
                                     activebackground=LIGHT_BG)
        self.help_button.place(relx=0.9, rely=0.95, anchor="se", x=-10, y=-10)


    def show_frame(self, page_name, product_id=None, animate=True):
        """
        Switches between frames with an optional slide animation.
        """
        new_frame = self.frames[page_name]

        if page_name == "ProductDetailScreen" and product_id is not None:
            new_frame.load_product(product_id)
        elif page_name == "ShoppingCartScreen":
            new_frame.load_cart_items()
        elif page_name == "OrderHistoryScreen":
            new_frame.load_orders()
        elif page_name == "ProfileScreen":
            new_frame.load_addresses()
        elif page_name == "InventoryManagementScreen":
             new_frame.load_products()

        if self.current_frame_name is None or not animate:
            new_frame.tkraise()
            self.current_frame_name = page_name
            return

        old_frame = self.frames[self.current_frame_name]
        
        width = self.container.winfo_width()

        new_frame.place(x=width, y=0, relwidth=1, relheight=1)
        new_frame.tkraise()

        step = 25
        delay = 10

        def animate_swipe():
            if not old_frame.winfo_ismapped() or not new_frame.winfo_ismapped():
                return

            current_x_old = old_frame.winfo_x()
            current_x_new = new_frame.winfo_x()

            if current_x_new > 0:
                old_frame.place(x=current_x_old - step, y=0, relwidth=1, relheight=1)
                new_frame.place(x=current_x_new - step, y=0, relwidth=1, relheight=1)
                self.after(delay, animate_swipe)
            else:
                old_frame.place_forget()
                new_frame.place(x=0, y=0, relwidth=1, relheight=1)
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