import bcrypt
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import tkinter as tk

# --- Path Constants (Ensure these are correct and images exist) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'assets', 'images')
FONT_DIR = os.path.join(BASE_DIR, 'assets', 'fonts')

PUP_LOGO_PATH = os.path.join(IMAGE_DIR, 'pup_logo.png')
QUESTION_MARK_PATH = os.path.join(IMAGE_DIR, 'question_mark.png')
CART_ICON_PATH = os.path.join(IMAGE_DIR, 'cart_icon.png')
USER_ICON_PATH = os.path.join(IMAGE_DIR, 'user_icon.png')
PUP_CAMPUS_PATH = os.path.join(IMAGE_DIR, 'pup_campus.png')
ADD_TO_CART_BTN_PATH = os.path.join(IMAGE_DIR, 'add_to_cart.png')
BUY_NOW_BTN_PATH = os.path.join(IMAGE_DIR, 'buy_now.png')
CHECK_MARK_PATH = os.path.join(IMAGE_DIR, 'check_mark.png')

# --- Color Constants ---
PUP_RED = "#9F2228"
PUP_GOLD = "#DD9933"
BUTTON_BLUE_LIGHT = "#A9E8F5"
BUTTON_BLUE_DARK = "#7ACCDC"
GRAY_TEXT = "#555555"
LIGHT_BG = "#F5F5F5" # Outer background color (the 'bezel' of the phone)
WHITE_BG = "#FFFFFF" # Inner content background color (most of the screen)
BORDER_COLOR = "#D1D1D1"

# --- Font Constants (ADJUSTED FOR SMALLER SCREEN) ---
GLOBAL_FONT = ("Segoe UI", 8)
GLOBAL_FONT_BOLD = ("Segoe UI", 8, "bold")
BUTTON_FONT = ("Segoe UI", 10, "bold")
TITLE_FONT = ("Segoe UI", 13, "bold") # For "Order History", "Shopping cart"
HEADER_FONT = ("Segoe UI", 18, "bold") # For "Mula sayo para sa bayan", "STUDY WITH PASSION"

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
              x1, y1 + radius]
    return canvas.create_polygon(points, smooth=True, **kwargs)

def create_styled_button(parent_frame, text, command, color_dark, color_light, font=BUTTON_FONT, width=120, height=30):
    """
    Creates a button with a rounded background using a canvas.
    Returns the canvas containing the button.
    """
    # The canvas background must match the parent's actual background (now WHITE_BG)
    canvas = tk.Canvas(parent_frame, width=width, height=height, bd=0, highlightthickness=0, bg=WHITE_BG)
    
    # Draw the rounded rectangle background
    create_rounded_rectangle(canvas, 1, 1, width-1, height-1, radius=int(height/2),
                             fill=color_light, outline=color_dark, width=1)

    # Place the actual Tkinter Button on top of the canvas
    button = tk.Button(canvas, text=text, command=command,
                       font=font, fg="black", bg=color_light, bd=0, # Button bg also uses color_light
                       activebackground=color_dark, activeforeground="white",
                       relief="flat")
    button.place(relx=0.5, rely=0.5, anchor="center", width=width - 6, height=height - 6)

    # Hover effects for visual feedback
    def on_enter(event):
        create_rounded_rectangle(canvas, 1, 1, width-1, height-1, radius=int(height/2),
                                 fill=color_dark, outline=color_dark, width=1)
        button.config(fg="white", bg=color_dark)
    def on_leave(event):
        create_rounded_rectangle(canvas, 1, 1, width-1, height-1, radius=int(height/2),
                                 fill=color_light, outline=color_dark, width=1)
        button.config(fg="black", bg=color_light)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return canvas


def create_rounded_entry_field(parent_frame, label_text, textvariable, is_password=False, width=280):
    """
    Creates an entry field with a label and a rounded border drawn on a canvas.
    Returns the Entry widget.
    """
    # Frame to group label and entry, its background matches the screen's (WHITE_BG)
    frame = tk.Frame(parent_frame, bg=WHITE_BG)
    frame.pack(anchor="center", pady=(5, 0)) # Centered, reduced vertical padding

    # Label for the entry field
    label = tk.Label(frame, text=label_text, font=GLOBAL_FONT, bg=WHITE_BG, fg=PUP_RED)
    label.pack(anchor="w", padx=10) # Reduced horizontal padding for label

    entry_height = 25 # Define entry height locally here
    canvas_width = width
    canvas_height = entry_height + 4 # Add a bit for border thickness

    # Canvas to draw the rounded border for the entry
    canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, bd=0, highlightthickness=0, bg=WHITE_BG)
    canvas.pack(pady=(2, 5)) # Reduced vertical padding for canvas

    # Draw the rounded rectangle border
    create_rounded_rectangle(canvas, 1, 1, canvas_width-1, canvas_height-1, radius=int(entry_height/2),
                             outline=PUP_RED, width=1, fill="white") # Outline width 1, fill white

    # The actual Entry widget, placed on the canvas
    entry = tk.Entry(canvas, font=GLOBAL_FONT, relief="flat", bd=0, # Ensure no native border
                     textvariable=textvariable, bg="white", fg=GRAY_TEXT, insertbackground=PUP_RED)
    entry.place(relx=0.5, rely=0.5, anchor="center", width=width-10, height=entry_height-4) # Place to fit inside canvas

    if is_password:
        entry.config(show="*")
    return entry