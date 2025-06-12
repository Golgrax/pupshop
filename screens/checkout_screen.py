import tkinter as tk
from tkinter import messagebox
import datetime
import os
import sqlite3

from utils.helpers import (
    load_image, PUP_RED, PUP_GOLD, LIGHT_BG, WHITE_BG, GLOBAL_FONT, GLOBAL_FONT_BOLD,
    TITLE_FONT, HEADER_FONT, CHECK_MARK_PATH, CART_ICON_PATH, USER_ICON_PATH,
    BORDER_COLOR, GRAY_TEXT
)
# Note: datetime imported twice, can remove one.

class CheckoutScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=LIGHT_BG)
        self.controller = controller
        self.db = self.controller.get_db()

        self.check_mark_img = load_image(CHECK_MARK_PATH, (20, 20)) # Reduced size

        # --- Top Bar (Icons) ---
        top_bar_frame = tk.Frame(self, bg=LIGHT_BG)
        top_bar_frame.pack(fill="x", pady=5, padx=10) # Reduced padding

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

        # Back Button
        back_button = tk.Button(top_bar_frame, text="< Back to Cart", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=LIGHT_BG, bd=0,
                                activebackground=LIGHT_BG, activeforeground=PUP_GOLD,
                                command=lambda: self.controller.show_frame("ShoppingCartScreen"))
        back_button.pack(side="left", padx=5)

        # --- "STUDY WITH PASSION" Header ---
        tk.Label(self, text="STUDY WITH\nPASSION", font=HEADER_FONT, fg=PUP_RED, bg=LIGHT_BG, justify="center").pack(pady=(10, 5)) # Reduced padding
        tk.Label(self, text="PUPStudyWithStyle", font=GLOBAL_FONT, fg="gray", bg=LIGHT_BG).pack()


        # --- Item Summary (Example: First item in cart) ---
        item_frame = tk.Frame(self, bg=WHITE_BG, bd=1, relief="solid", highlightbackground=PUP_GOLD, highlightthickness=1)
        item_frame.pack(fill="x", padx=15, pady=10) # Reduced padding

        self.item_image_label = tk.Label(item_frame, bg=WHITE_BG)
        self.item_image_label.pack(side="left", padx=5, pady=5) # Reduced padding

        item_details_frame = tk.Frame(item_frame, bg=WHITE_BG)
        item_details_frame.pack(side="left", fill="x", expand=True, padx=5) # Reduced padding

        self.item_name_label = tk.Label(item_details_frame, text="", font=GLOBAL_FONT_BOLD, fg="black", bg=WHITE_BG, wraplength=150, justify="left") # Reduced wraplength
        self.item_name_label.pack(anchor="w")
        self.item_desc_label = tk.Label(item_details_frame, text="", font=GLOBAL_FONT, fg="gray", bg=WHITE_BG, wraplength=150, justify="left") # Reduced wraplength
        self.item_desc_label.pack(anchor="w")
        self.item_price_label = tk.Label(item_details_frame, text="P0.00", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=WHITE_BG)
        self.item_price_label.pack(anchor="w", pady=(2,0))

        # --- Delivery Info ---
        delivery_frame = tk.Frame(self, bg=LIGHT_BG)
        delivery_frame.pack(fill="x", padx=15, pady=5) # Reduced padding
        tk.Label(delivery_frame, text="Estimated delivery: May 8-9", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=LIGHT_BG).pack(anchor="w")
        tk.Label(delivery_frame, text="Standard shipping", font=GLOBAL_FONT, fg="gray", bg=LIGHT_BG).pack(anchor="w")
        self.shipping_cost_label = tk.Label(delivery_frame, text="P36.00", font=GLOBAL_FONT, fg="gray", bg=LIGHT_BG)
        self.shipping_cost_label.pack(side="right", padx=5)

        # --- Order Summary ---
        summary_frame = tk.Frame(self, bg=LIGHT_BG, bd=1, relief="solid", highlightbackground=BORDER_COLOR, highlightthickness=1)
        summary_frame.pack(fill="x", padx=15, pady=5) # Reduced padding

        tk.Label(summary_frame, text="Order summary", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=LIGHT_BG).grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=3) # Reduced padding
        
        tk.Label(summary_frame, text="Subtotal", font=GLOBAL_FONT, fg="gray", bg=LIGHT_BG).grid(row=1, column=0, sticky="w", padx=5, pady=1) # Reduced padding
        self.subtotal_label = tk.Label(summary_frame, text="P0.00", font=GLOBAL_FONT, fg="gray", bg=LIGHT_BG)
        self.subtotal_label.grid(row=1, column=1, sticky="e", padx=5, pady=1)

        tk.Label(summary_frame, text="Shipping", font=GLOBAL_FONT, fg="gray", bg=LIGHT_BG).grid(row=2, column=0, sticky="w", padx=5, pady=1) # Reduced padding
        self.summary_shipping_label = tk.Label(summary_frame, text="P0.00", font=GLOBAL_FONT, fg="gray", bg=LIGHT_BG)
        self.summary_shipping_label.grid(row=2, column=1, sticky="e", padx=5, pady=1)

        tk.Label(summary_frame, text="Total", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=LIGHT_BG).grid(row=3, column=0, sticky="w", padx=5, pady=3) # Reduced padding
        self.total_label = tk.Label(summary_frame, text="P0.00", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=LIGHT_BG)
        self.total_label.grid(row=3, column=1, sticky="e", padx=5, pady=3)

        summary_frame.grid_columnconfigure(1, weight=1)

        # --- Payment Method ---
        payment_frame = tk.Frame(self, bg=LIGHT_BG)
        payment_frame.pack(fill="x", padx=15, pady=5) # Reduced padding
        tk.Label(payment_frame, text="Payment method", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=LIGHT_BG).pack(anchor="w")
        cash_delivery_frame = tk.Frame(payment_frame, bg=LIGHT_BG)
        cash_delivery_frame.pack(fill="x", pady=2) # Reduced padding
        tk.Label(cash_delivery_frame, text="Cash on delivery", font=GLOBAL_FONT, fg="gray", bg=LIGHT_BG).pack(side="left")
        self.check_mark_label = tk.Label(cash_delivery_frame, image=self.check_mark_img, bg=LIGHT_BG)
        self.check_mark_label.pack(side="right")


        # --- CHECK OUT NOW! Button ---
        checkout_button_frame = tk.Frame(self, bg=LIGHT_BG)
        checkout_button_frame.pack(fill="x", pady=10) # Reduced padding
        self.checkout_now_button = tk.Button(checkout_button_frame, text="CHECK OUT NOW!", font=HEADER_FONT,
                                             fg=PUP_RED, bg=PUP_GOLD, activebackground=PUP_RED,
                                             activeforeground="white", bd=0, relief="flat",
                                             command=self.process_checkout)
        self.checkout_now_button.pack(pady=5) # Reduced padding

        self.load_checkout_details()

    def load_checkout_details(self):
        cart_items = self.controller.get_cart()
        if not cart_items:
            messagebox.showwarning("Checkout", "Your cart is empty. Please add items before checking out.")
            self.controller.show_frame("ShoppingCartScreen")
            return

        product_ids = ",".join(map(str, cart_items.keys()))
        products_data = self.db.fetch_all(f"SELECT id, name, price, image_path, description FROM products WHERE id IN ({product_ids})")

        subtotal = 0.0
        total_items = 0
        first_item_details = None

        for prod_id, name, price, img_path, desc in products_data:
            quantity = cart_items.get(prod_id, 0)
            subtotal += price * quantity
            total_items += quantity
            
            if first_item_details is None:
                first_item_details = {
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "img_path": img_path
                }
        
        if first_item_details:
            self.item_name_label.config(text=first_item_details['name'])
            self.item_desc_label.config(text=first_item_details['desc'])
            self.item_price_label.config(text=f"P{first_item_details['price']:.2f}")
            item_image_full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images', first_item_details['img_path'])
            item_img = load_image(item_image_full_path, (80, 80)) # Reduced image size
            if item_img:
                self.item_image_label.config(image=item_img)
                self.item_image_label.image = item_img
        else:
            self.item_name_label.config(text="No items in cart")
            self.item_desc_label.config(text="")
            self.item_price_label.config(text="P0.00")
            self.item_image_label.config(image='')


        shipping_cost = 36.00
        total_amount = subtotal + shipping_cost

        self.subtotal_label.config(text=f"P{subtotal:.2f}")
        self.summary_shipping_label.config(text=f"P{shipping_cost:.2f}")
        self.shipping_cost_label.config(text=f"P{shipping_cost:.2f}")
        self.total_label.config(text=f"P{total_amount:.2f}")

        if total_items == 1:
            item_text = "1 item"
        else:
            item_text = f"{total_items} items"
        # Re-create/update this label as it's not a fixed part of the __init__ structure.
        # Ensure it's removed if it exists before re-creating.
        if hasattr(self, 'summary_frame_title_label'):
            self.summary_frame_title_label.destroy()
        self.summary_frame_title_label = tk.Label(self, text=f"{item_text}, total P{total_amount:.2f}",
                                                  font=GLOBAL_FONT, fg="gray", bg=LIGHT_BG)
        self.summary_frame_title_label.pack(pady=5)


    def process_checkout(self):
        user_id = self.controller.get_current_user()
        if not user_id:
            messagebox.showwarning("Checkout Error", "Please log in to place an order.")
            self.controller.show_frame("LoginScreen")
            return

        cart_items = self.controller.get_cart()
        if not cart_items:
            messagebox.showwarning("Checkout", "Your cart is empty!")
            return

        subtotal = 0.0
        product_details = {}
        for prod_id, quantity in cart_items.items():
            product_data = self.db.fetch_one("SELECT name, price, stock_quantity FROM products WHERE id = ?", (prod_id,))
            if product_data:
                name, price, stock = product_data
                if stock < quantity:
                    messagebox.showerror("Checkout Error", f"Not enough stock for {name}. Available: {stock}")
                    return
                subtotal += price * quantity
                product_details[prod_id] = {"name": name, "price": price, "quantity": quantity}
            else:
                messagebox.showerror("Checkout Error", f"Product ID {prod_id} not found.")
                return

        shipping_cost = 36.00
        total_amount = subtotal + shipping_cost

        confirm = messagebox.askyesno("Confirm Order", f"Total amount: P{total_amount:.2f}\nConfirm purchase?")
        if not confirm:
            return

        self.db.connect()
        try:
            self.db.cursor.execute("BEGIN TRANSACTION;")

            order_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.cursor.execute(
                "INSERT INTO orders (user_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)",
                (user_id, order_date, total_amount, 'Pending')
            )
            order_id = self.db.cursor.lastrowid

            for prod_id, details in product_details.items():
                self.db.cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, item_price_at_order) VALUES (?, ?, ?, ?)",
                    (order_id, prod_id, details['quantity'], details['price'])
                )
                self.db.cursor.execute(
                    "UPDATE products SET stock_quantity = stock_quantity - ?, sales_count = sales_count + ? WHERE id = ?",
                    (details['quantity'], details['quantity'], prod_id)
                )

            self.db.conn.commit()
            messagebox.showinfo("Order Placed", f"Your order (Ref No: {order_id}) has been placed successfully!")
            self.controller.clear_cart()
            self.controller.show_frame("OrderHistoryScreen")
        except sqlite3.Error as e:
            self.db.conn.rollback()
            messagebox.showerror("Order Error", f"Failed to place order: {e}")
        finally:
            pass