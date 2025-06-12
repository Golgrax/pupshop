import bcrypt
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import tkinter as tk

# --- Path Constants ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'assets', 'images')
FONT_DIR = os.path.join(BASE_DIR, 'assets', 'fonts') # For custom fonts

PUP_LOGO_PATH = os.path.join(IMAGE_DIR, 'pup_logo.png')
QUESTION_MARK_PATH = os.path.join(IMAGE_DIR, 'question_mark.png')
CART_ICON_PATH = os.path.join(IMAGE_DIR, 'cart_icon.png')
USER_ICON_PATH = os.path.join(IMAGE_DIR, 'user_icon.png')
PUP_CAMPUS_PATH = os.path.join(IMAGE_DIR, 'pup_campus.png')
ADD_TO_CART_BTN_PATH = os.path.join(IMAGE_DIR, 'add_to_cart.png') # If using image buttons
BUY_NOW_BTN_PATH = os.path.join(IMAGE_DIR, 'buy_now.png') # If using image buttons
CHECK_MARK_PATH = os.path.join(IMAGE_DIR, 'check_mark.png')

# --- Color Constants ---
PUP_RED = "#9F2228"
PUP_GOLD = "#DD9933" # More yellowish gold
BUTTON_BLUE_LIGHT = "#A9E8F5"
BUTTON_BLUE_DARK = "#7ACCDC"
GRAY_TEXT = "#555555"
LIGHT_BG = "#F5F5F5"
WHITE_BG = "#FFFFFF"
BORDER_COLOR = "#D1D1D1" # A light gray for borders
TRANSPARENT_COLOR = '#00000000' # For transparent canvas background, not directly used for Tkinter bg

# --- Font Constants ---
# Using common system fonts. If you have specific .ttf files, load them.
# Example: custom_font = ImageFont.truetype(os.path.join(FONT_DIR, "MyCustomFont.ttf"), size)
GLOBAL_FONT = ("Segoe UI", 10)
GLOBAL_FONT_BOLD = ("Segoe UI", 10, "bold")
BUTTON_FONT = ("Segoe UI", 12, "bold")
TITLE_FONT = ("Segoe UI", 16, "bold") # For "Order History", "Shopping cart"
HEADER_FONT = ("Segoe UI", 24, "bold") # For "Mula sayo para sa bayan", "STUDY WITH PASSION"

# --- Helper Functions ---
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def load_image(path, size=None):
    """Loads an image and returns a PhotoImage object."""
    try:
        img = Image.open(path)
        if size:
            img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except FileNotFoundError:
        print(f"Error: Image not found at {path}")
        # Return a placeholder image or None
        return None
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    """Draws a rounded rectangle on a Tkinter canvas."""
    points = [x1 + radius, y1,
              x2 - radius, y1,
              x2, y1 + radius,
              x2, y2 - radius,
              x2 - radius, y2,
              x1 + radius, y2,
              x1, y2 - radius,
              x1, y1 + radius]
    return canvas.create_polygon(points, smooth=True, **kwargs)

def create_styled_button(parent_frame, text, command, color_dark, color_light, font=BUTTON_FONT, width=150, height=40):
    """
    Creates a button with a rounded background using a canvas.
    Returns the Tkinter Button widget.
    """
    canvas = tk.Canvas(parent_frame, width=width, height=height, bd=0, highlightthickness=0, bg=LIGHT_BG)
    # Draw the rounded rectangle background
    create_rounded_rectangle(canvas, 1, 1, width-1, height-1, radius=int(height/2),
                             fill=color_light, outline=color_dark, width=1)

    # Place the actual Tkinter Button on top of the canvas
    button = tk.Button(canvas, text=text, command=command,
                       font=font, fg="black", bg=color_light, bd=0,
                       activebackground=color_dark, activeforeground="white",
                       relief="flat")
    # Position the button to cover the canvas drawing
    button.place(relx=0.5, rely=0.5, anchor="center", width=width - 10, height=height - 10)

    # Make the button react to hover by changing canvas color (optional)
    def on_enter(event):
        create_rounded_rectangle(canvas, 1, 1, width-1, height-1, radius=int(height/2),
                                 fill=color_dark, outline=color_dark, width=1)
        button.config(fg="white")
    def on_leave(event):
        create_rounded_rectangle(canvas, 1, 1, width-1, height-1, radius=int(height/2),
                                 fill=color_light, outline=color_dark, width=1)
        button.config(fg="black")

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return canvas # Return the canvas which contains the button


# Custom entry field for the rounded look
def create_rounded_entry_field(parent_frame, label_text, textvariable, is_password=False, width=300):
    frame = tk.Frame(parent_frame, bg=LIGHT_BG)
    frame.pack(anchor="w", padx=50, pady=(10, 0))

    label = tk.Label(frame, text=label_text, font=GLOBAL_FONT, bg=LIGHT_BG, fg=PUP_RED)
    label.pack(anchor="w")

    # Create a canvas to draw the rounded border
    entry_height = 30
    canvas_width = width + 2 # Add a bit for border
    canvas_height = entry_height + 2
    canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, bd=0, highlightthickness=0, bg=LIGHT_BG)
    canvas.pack(pady=(5, 0))

    # Draw the rounded rectangle border
    create_rounded_rectangle(canvas, 0, 0, canvas_width, canvas_height, radius=int(entry_height/2),
                             outline=PUP_RED, width=1, fill="white")

    # Create the actual Entry widget without a border and place it on the canvas
    entry = tk.Entry(canvas, width=int(width/10), font=GLOBAL_FONT, relief="flat", bd=0,
                     textvariable=textvariable, bg="white", fg=GRAY_TEXT, insertbackground=PUP_RED)
    entry.place(relx=0.5, rely=0.5, anchor="center", width=width-10, height=entry_height-4) # Adjust for padding

    if is_password:
        entry.config(show="*")
    return entry