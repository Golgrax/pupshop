import tkinter as tk
from tkinter import messagebox
from tkinter import ttk # For Treeview
from utils.helpers import (
    load_image, PUP_RED, PUP_GOLD, LIGHT_BG, WHITE_BG, GLOBAL_FONT, GLOBAL_FONT_BOLD,
    TITLE_FONT, HEADER_FONT, BORDER_COLOR, CART_ICON_PATH, USER_ICON_PATH
)
import os

class InventoryManagementScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=LIGHT_BG)
        self.controller = controller
        self.db = self.controller.get_db()

        # --- Variables ---
        self.item_id_var = tk.StringVar()
        self.item_name_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.price_var = tk.StringVar()

        # --- Top Bar (Icons) ---
        top_bar_frame = tk.Frame(self, bg=LIGHT_BG)
        top_bar_frame.pack(fill="x", pady=10, padx=20)

        # Cart Icon (can be hidden for admin screen)
        self.cart_icon_image = self.controller.cart_icon
        self.cart_button = tk.Button(top_bar_frame, image=self.cart_icon_image, bd=0, bg=LIGHT_BG,
                                     activebackground=LIGHT_BG, command=lambda: self.controller.show_frame("ShoppingCartScreen"))
        self.cart_button.pack(side="right", padx=5)

        # User Profile Icon (can be replaced by admin logout)
        self.user_icon_image = self.controller.user_icon
        self.profile_button = tk.Button(top_bar_frame, image=self.user_icon_image, bd=0, bg=LIGHT_BG,
                                        activebackground=LIGHT_BG, command=lambda: self.controller.show_frame("ProfileScreen"))
        self.profile_button.pack(side="right", padx=5)

        # Back Button (to home or admin dashboard)
        back_button = tk.Button(top_bar_frame, text="< Back", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=LIGHT_BG, bd=0,
                                activebackground=LIGHT_BG, activeforeground=PUP_GOLD,
                                command=lambda: self.controller.show_frame("HomeScreen"))
        back_button.pack(side="left", padx=5)

        # --- Inventory Management Header ---
        tk.Label(self, text="INVENTORY MANAGEMENT", font=HEADER_FONT, fg=PUP_RED, bg=LIGHT_BG).pack(pady=(40, 20))
        tk.Frame(self, bg=PUP_RED, height=2).pack(fill="x", padx=30, pady=(0, 20)) # Underline

        # --- Input Fields for Item Management ---
        input_frame = tk.Frame(self, bg=LIGHT_BG)
        input_frame.pack(fill="x", padx=30, pady=5)

        # Helper for a simple label + entry row
        def create_input_row(parent, label_text, textvariable, is_readonly=False):
            row_frame = tk.Frame(parent, bg=LIGHT_BG)
            row_frame.pack(fill="x", pady=2)
            tk.Label(row_frame, text=label_text, font=GLOBAL_FONT, fg=PUP_RED, bg=LIGHT_BG, width=15, anchor="w").pack(side="left")
            entry = tk.Entry(row_frame, textvariable=textvariable, font=GLOBAL_FONT, relief="solid", bd=1,
                             highlightbackground=PUP_GOLD, highlightthickness=1, bg="white", fg="gray", insertbackground=PUP_RED)
            entry.pack(side="left", fill="x", expand=True)
            if is_readonly:
                entry.config(state="readonly")
            return entry

        self.item_id_entry = create_input_row(input_frame, "ITEM ID:", self.item_id_var, is_readonly=True) # ID is typically auto-generated
        self.item_name_entry = create_input_row(input_frame, "ITEM NAME:", self.item_name_var)
        self.quantity_entry = create_input_row(input_frame, "QUANTITY:", self.quantity_var)
        self.price_entry = create_input_row(input_frame, "PRICE:", self.price_var)

        # --- Action Buttons ---
        button_frame = tk.Frame(self, bg=LIGHT_BG)
        button_frame.pack(pady=20)

        # Reusing create_styled_button, but adapting for simple aesthetic
        def create_simple_button(parent, text, command, bg_color):
            btn = tk.Button(parent, text=text, command=command, font=GLOBAL_FONT_BOLD,
                            fg="white", bg=bg_color, activebackground=PUP_RED,
                            activeforeground="white", bd=0, relief="flat", width=10)
            btn.pack(side="left", padx=5)
            return btn

        create_simple_button(button_frame, "Add Item:", self.add_item, PUP_RED)
        create_simple_button(button_frame, "View", self.view_item, PUP_GOLD)
        create_simple_button(button_frame, "Update", self.update_item, PUP_RED)
        create_simple_button(button_frame, "Delete", self.delete_item, PUP_GOLD)

        tk.Frame(self, bg=PUP_RED, height=2).pack(fill="x", padx=30, pady=(20, 0)) # Underline


        # --- Inventory Table (Treeview) ---
        # Style for Treeview
        style = ttk.Style()
        style.theme_use("clam") # 'clam', 'alt', 'default', 'classic'
        style.configure("Treeview.Heading", font=GLOBAL_FONT_BOLD, background=PUP_RED, foreground="white")
        style.configure("Treeview", font=GLOBAL_FONT, rowheight=25, background=WHITE_BG, fieldbackground=WHITE_BG)
        style.map('Treeview', background=[('selected', PUP_GOLD)])

        columns = ("ID", "NAME", "QUANTITY", "PRICE")
        self.inventory_tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        self.inventory_tree.pack(fill="both", expand=True, padx=30, pady=10)

        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=100, anchor="center") # Default width

        self.inventory_tree.column("ID", width=50)
        self.inventory_tree.column("NAME", width=150)
        self.inventory_tree.column("QUANTITY", width=80)
        self.inventory_tree.column("PRICE", width=80)

        # Scrollbar for Treeview
        tree_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.inventory_tree.yview)
        tree_scrollbar.pack(side="right", fill="y", padx=(0,30))
        self.inventory_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.inventory_tree.bind("<<TreeviewSelect>>", self.on_item_select)

        self.load_products()

    def load_products(self):
        # Clear existing entries in treeview
        for i in self.inventory_tree.get_children():
            self.inventory_tree.delete(i)

        products = self.db.fetch_all("SELECT id, name, stock_quantity, price FROM products ORDER BY id")
        for prod in products:
            self.inventory_tree.insert("", "end", values=prod)

    def on_item_select(self, event):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            return

        item_values = self.inventory_tree.item(selected_item[0], 'values')
        
        self.item_id_var.set(item_values[0])
        self.item_name_var.set(item_values[1])
        self.quantity_var.set(item_values[2])
        self.price_var.set(item_values[3])

    def clear_fields(self):
        self.item_id_var.set("")
        self.item_name_var.set("")
        self.quantity_var.set("")
        self.price_var.set("")
        self.inventory_tree.selection_remove(self.inventory_tree.selection()) # Deselect item

    def add_item(self):
        name = self.item_name_var.get().strip()
        quantity = self.quantity_var.get().strip()
        price = self.price_var.get().strip()

        if not name or not quantity or not price:
            messagebox.showerror("Error", "Name, Quantity, and Price are required.")
            return
        
        try:
            quantity = int(quantity)
            price = float(price)
            if quantity < 0 or price < 0:
                raise ValueError("Values cannot be negative.")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Price must be a number.")
            return
        
        success = self.db.execute_query(
            "INSERT INTO products (name, stock_quantity, price) VALUES (?, ?, ?)",
            (name, quantity, price)
        )
        if success:
            messagebox.showinfo("Success", "Item added successfully.")
            self.load_products()
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Failed to add item.")

    def view_item(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to view.")
            return
        # Data is already loaded into entry fields by on_item_select

    def update_item(self):
        item_id = self.item_id_var.get().strip()
        name = self.item_name_var.get().strip()
        quantity = self.quantity_var.get().strip()
        price = self.price_var.get().strip()

        if not item_id or not name or not quantity or not price:
            messagebox.showerror("Error", "All fields are required for update.")
            return

        try:
            item_id = int(item_id)
            quantity = int(quantity)
            price = float(price)
            if quantity < 0 or price < 0:
                raise ValueError("Values cannot be negative.")
        except ValueError:
            messagebox.showerror("Error", "ID, Quantity, and Price must be valid numbers.")
            return

        success = self.db.execute_query(
            "UPDATE products SET name = ?, stock_quantity = ?, price = ? WHERE id = ?",
            (name, quantity, price, item_id)
        )
        if success:
            messagebox.showinfo("Success", "Item updated successfully.")
            self.load_products()
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Failed to update item.")

    def delete_item(self):
        item_id = self.item_id_var.get().strip()
        if not item_id:
            messagebox.showwarning("Warning", "Please select an item to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete item ID {item_id}?")
        if not confirm:
            return

        success = self.db.execute_query("DELETE FROM products WHERE id = ?", (int(item_id),))
        if success:
            messagebox.showinfo("Success", "Item deleted successfully.")
            self.load_products()
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Failed to delete item.")

