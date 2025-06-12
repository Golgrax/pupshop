import bcrypt
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import tkinter as tk
import tkinter.font as tkFont

# --- Path Constants ---
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
ROCA_ONE_FONT_PATH = os.path.join(FONT_DIR, "RocaOne.ttf") # Ensure this is correctly defined

# --- Color Constants ---
PUP_RED = "#9F2228"
PUP_GOLD = "#DD9933"
BUTTON_BLUE_LIGHT = "#A9E8F5"
BUTTON_BLUE_DARK = "#7ACCDC"
GRAY_TEXT = "#555555"
LIGHT_BG = "#F5F5F5" # Outer window background (the 'bezel')
WHITE_BG = "#FFFFFF" # Inner content area background (most of the screen)
BORDER_COLOR = "#D1D1D1"

# --- Font Constants (Initial defaults - will be set after Tkinter root is ready) ---
GLOBAL_FONT = ("Segoe UI", 8)
GLOBAL_FONT_BOLD = ("Segoe UI", 8, "bold")
BUTTON_FONT = ("Segoe UI", 10, "bold") # Default button font

# Global variables to store font objects once loaded
_roca_one_header_font_instance = None
_roca_one_title_font_instance = None
_roca_one_loaded_flag = False

def load_custom_fonts():
    """
    Loads custom fonts. This function MUST be called AFTER tk.Tk() is initialized.
    """
    global _roca_one_header_font_instance, _roca_one_title_font_instance, _roca_one_loaded_flag
    global TITLE_FONT, HEADER_FONT # Update global font constants if successful

    if _roca_one_loaded_flag: # Only load once
        return

    try:
        # Step 1: Register the font file with Tkinter's font system.
        # This makes the font available by its family name.
        # Ensure a Tk root is available (it will be, as this is called in App.__init__)
        tk.Tk().tk.call('font', 'create', 'RocaOneFamily', '-family', 'RocaOne', '-file', ROCA_ONE_FONT_PATH)
        
        # Step 2: Create tkFont.Font instances using the newly registered family name.
        _roca_one_header_font_instance = tkFont.Font(family='RocaOneFamily', size=18)
        _roca_one_title_font_instance = tkFont.Font(family='RocaOneFamily', size=13)
        
        _roca_one_loaded_flag = True
        print(f"Successfully loaded custom font: {ROCA_ONE_FONT_PATH}")

        # Update the global font constants to use these new font instances
        TITLE_FONT = _roca_one_title_font_instance
        HEADER_FONT = _roca_one_header_font_instance

    except Exception as e: # Catch any generic exception during font loading
        print(f"Warning: Could not load custom font '{ROCA_ONE_FONT_PATH}'. Using fallback fonts. Error: {e}")
        _roca_one_loaded_flag = False
        # Fallback fonts (Segoe UI bold) are already set as initial defaults.


# --- Helper Functions (rest remains largely same) ---
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
        # print(f"Error: Image not found at {path}") # Comment out to reduce console spam
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

def create_styled_button(parent_frame, text, command, color_dark, color_light, font_override=None, width=120, height=30):
    """
    Creates a button with a rounded background using a canvas.
    Returns the canvas containing the button.
    """
    actual_font = font_override if font_override else BUTTON_FONT

    # Canvas background must match the parent's (now WHITE_BG for screen frames)
    canvas = tk.Canvas(parent_frame, width=width, height=height, bd=0, highlightthickness=0, bg=WHITE_BG)
    
    # Draw the rounded rectangle background
    create_rounded_rectangle(canvas, 1, 1, width-1, height-1, radius=int(height/2),
                             fill=color_light, outline=color_dark, width=1)

    # Place the actual Tkinter Button on top of the canvas
    button = tk.Button(canvas, text=text, command=command,
                       font=actual_font, fg="black", bg=color_light, bd=0,
                       activebackground=color_dark, activeforeground="white",
                       relief="flat")
    button.place(relx=0.5, rely=0.5, anchor="center", width=width - 6, height=height - 6)

    # Hover effects for visual feedback (Redraw entire rectangle for smooth change)
    def on_enter(event):
        canvas.delete("all") # Clear previous drawing
        create_rounded_rectangle(canvas, 1, 1, width-1, height-1, radius=int(height/2),
                                 fill=color_dark, outline=color_dark, width=1)
        button.config(fg="white", bg=color_dark)
        button.place(relx=0.5, rely=0.5, anchor="center", width=width - 6, height=height - 6) # Re-place to ensure z-order
    def on_leave(event):
        canvas.delete("all") # Clear previous drawing
        create_rounded_rectangle(canvas, 1, 1, width-1, height-1, radius=int(height/2),
                                 fill=color_light, outline=color_dark, width=1)
        button.config(fg="black", bg=color_light)
        button.place(relx=0.5, rely=0.5, anchor="center", width=width - 6, height=height - 6)

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
    frame.pack(anchor="center", pady=(5, 0))

    # Label for the entry field
    label = tk.Label(frame, text=label_text, font=GLOBAL_FONT, bg=WHITE_BG, fg=PUP_RED)
    label.pack(anchor="w", padx=10)

    entry_height = 25 # Define entry height locally here
    canvas_width = width
    canvas_height = entry_height + 4

    # Canvas to draw the rounded border for the entry
    canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, bd=0, highlightthickness=0, bg=WHITE_BG)
    canvas.pack(pady=(2, 5))

    # Draw the rounded rectangle border
    create_rounded_rectangle(canvas, 1, 1, canvas_width-1, canvas_height-1, radius=int(entry_height/2),
                             outline=PUP_RED, width=1, fill="white")

    # The actual Entry widget, placed on the canvas
    entry = tk.Entry(canvas, font=GLOBAL_FONT, relief="flat", bd=0,
                     textvariable=textvariable, bg="white", fg=GRAY_TEXT, insertbackground=PUP_RED)
    entry.place(relx=0.5, rely=0.5, anchor="center", width=width-10, height=entry_height-4)

    if is_password:
        entry.config(show="*")
    return entry