import tkinter as tk
from tkinter import messagebox
from utils.helpers import (
    load_image, PUP_RED, PUP_GOLD, LIGHT_BG, WHITE_BG, GLOBAL_FONT, GLOBAL_FONT_BOLD,
    TITLE_FONT, HEADER_FONT, BORDER_COLOR, USER_ICON_PATH, CART_ICON_PATH, create_rounded_entry_field
)

class ProfileScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=LIGHT_BG)
        self.controller = controller
        self.db = self.controller.get_db()

        # --- Variables for Address fields ---
        self.address1_line_var = tk.StringVar()
        self.address1_name_var = tk.StringVar()
        self.address1_contact_var = tk.StringVar()

        self.address2_line_var = tk.StringVar()
        self.address2_name_var = tk.StringVar()
        self.address2_contact_var = tk.StringVar()

        # --- Top Bar (Icons) ---
        top_bar_frame = tk.Frame(self, bg=LIGHT_BG)
        top_bar_frame.pack(fill="x", pady=10, padx=20)

        # Cart Icon
        self.cart_icon_image = self.controller.cart_icon
        self.cart_button = tk.Button(top_bar_frame, image=self.cart_icon_image, bd=0, bg=LIGHT_BG,
                                     activebackground=LIGHT_BG, command=lambda: self.controller.show_frame("ShoppingCartScreen"))
        self.cart_button.pack(side="right", padx=5)

        # User Profile Icon (Main profile icon)
        self.user_icon_image = self.controller.user_icon # Large user icon for profile
        self.profile_button = tk.Button(top_bar_frame, image=self.user_icon_image, bd=0, bg=LIGHT_BG,
                                        activebackground=LIGHT_BG, command=lambda: self.controller.show_frame("ProfileScreen"))
        self.profile_button.pack(side="right", padx=5) # This one is just for the header, not the main profile pic

        # Back Button
        back_button = tk.Button(top_bar_frame, text="< Back to Shop", font=GLOBAL_FONT_BOLD, fg=PUP_RED, bg=LIGHT_BG, bd=0,
                                activebackground=LIGHT_BG, activeforeground=PUP_GOLD,
                                command=lambda: self.controller.show_frame("HomeScreen"))
        back_button.pack(side="left", padx=5)

        # --- Main User Icon ---
        self.main_user_icon_image = load_image(USER_ICON_PATH, (100, 100)) # Larger icon
        self.main_user_icon_label = tk.Label(self, image=self.main_user_icon_image, bg=LIGHT_BG)
        self.main_user_icon_label.pack(pady=20)

        # --- Address 1 Section ---
        tk.Label(self, text="Address: 1", font=TITLE_FONT, fg=PUP_RED, bg=LIGHT_BG, anchor="w").pack(fill="x", padx=30, pady=(10,5))
        
        # Use custom rounded entry for consistency, or standard entry with border
        self.address1_line_entry = create_rounded_entry_field(self, "Address:", self.address1_line_var, width=350)
        self.address1_name_entry = create_rounded_entry_field(self, "Name:", self.address1_name_var, width=350)
        self.address1_contact_entry = create_rounded_entry_field(self, "Contact No. :", self.address1_contact_var, width=350)
        
        self.save_address1_button = tk.Button(self, text="Save Address 1", font=GLOBAL_FONT_BOLD, fg="white", bg=PUP_GOLD,
                                              activebackground=PUP_RED, bd=0, relief="flat", command=lambda: self.save_address(1))
        self.save_address1_button.pack(pady=10)


        # --- Address 2 Section ---
        tk.Label(self, text="Address: 2", font=TITLE_FONT, fg=PUP_RED, bg=LIGHT_BG, anchor="w").pack(fill="x", padx=30, pady=(20,5))

        self.address2_line_entry = create_rounded_entry_field(self, "Address:", self.address2_line_var, width=350)
        self.address2_name_entry = create_rounded_entry_field(self, "Name:", self.address2_name_var, width=350)
        self.address2_contact_entry = create_rounded_entry_field(self, "Contact No. :", self.address2_contact_var, width=350)
        
        self.save_address2_button = tk.Button(self, text="Save Address 2", font=GLOBAL_FONT_BOLD, fg="white", bg=PUP_GOLD,
                                              activebackground=PUP_RED, bd=0, relief="flat", command=lambda: self.save_address(2))
        self.save_address2_button.pack(pady=10)

        self.load_addresses() # Load existing addresses on screen display

    def load_addresses(self):
        user_id = self.controller.get_current_user()
        if not user_id:
            messagebox.showwarning("Access Denied", "Please log in to view/manage your profile.")
            self.controller.show_frame("LoginScreen")
            return

        addresses = self.db.fetch_all("SELECT id, address_line, contact_name, contact_no FROM addresses WHERE user_id = ? ORDER BY id ASC", (user_id,))
        
        # Clear fields first
        self.address1_line_var.set("")
        self.address1_name_var.set("")
        self.address1_contact_var.set("")
        self.address2_line_var.set("")
        self.address2_name_var.set("")
        self.address2_contact_var.set("")

        if len(addresses) > 0:
            self.address1_id = addresses[0][0] # Store ID for update
            self.address1_line_var.set(addresses[0][1])
            self.address1_name_var.set(addresses[0][2])
            self.address1_contact_var.set(addresses[0][3])
        if len(addresses) > 1:
            self.address2_id = addresses[1][0] # Store ID for update
            self.address2_line_var.set(addresses[1][1])
            self.address2_name_var.set(addresses[1][2])
            self.address2_contact_var.set(addresses[1][3])
        
    def save_address(self, address_num):
        user_id = self.controller.get_current_user()
        if not user_id:
            messagebox.showwarning("Save Error", "You must be logged in to save addresses.")
            return

        if address_num == 1:
            address_line = self.address1_line_var.get().strip()
            contact_name = self.address1_name_var.get().strip()
            contact_no = self.address1_contact_var.get().strip()
            address_id_to_update = getattr(self, 'address1_id', None)
        else: # address_num == 2
            address_line = self.address2_line_var.get().strip()
            contact_name = self.address2_name_var.get().strip()
            contact_no = self.address2_contact_var.get().strip()
            address_id_to_update = getattr(self, 'address2_id', None)
        
        if not address_line or not contact_name or not contact_no:
            messagebox.showerror("Save Error", "All fields for the address must be filled.")
            return

        if address_id_to_update:
            # Update existing address
            success = self.db.execute_query(
                "UPDATE addresses SET address_line = ?, contact_name = ?, contact_no = ? WHERE id = ?",
                (address_line, contact_name, contact_no, address_id_to_update)
            )
            action = "updated"
        else:
            # Insert new address
            success = self.db.execute_query(
                "INSERT INTO addresses (user_id, address_line, contact_name, contact_no) VALUES (?, ?, ?, ?)",
                (user_id, address_line, contact_name, contact_no)
            )
            # After insert, reload to get the new ID
            if success:
                self.load_addresses() # Reload all addresses to get new IDs
            action = "added"

        if success:
            messagebox.showinfo("Success", f"Address {address_num} {action} successfully!")
        else:
            messagebox.showerror("Error", f"Failed to {action} address {address_num}.")
