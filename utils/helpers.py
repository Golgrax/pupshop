import bcrypt
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import tkinter as tk
import tkinter.font as tkFont # Import tkinter.font for custom font loading

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
ROCA_ONE_FONT_PATH = os.path.join(FONT_DIR, "RocaOne.ttf") # <--- ADD THIS LINE

# --- Color Constants ---
PUP_RED = "#9F2228"
PUP_GOLD = "#DD9933"
BUTTON_BLUE_LIGHT = "#A9E8F5"
BUTTON_BLUE_DARK = "#7ACCDC"
GRAY_TEXT = "#555555"
LIGHT_BG = "#F5F5F5"
WHITE_BG = "#FFFFFF"
BORDER_COLOR = "#D1D1D1"

# --- Font Constants (Initial defaults - will be set after Tkinter root is ready) ---
GLOBAL_FONT = ("Segoe UI", 8)
GLOBAL_FONT_BOLD = ("Segoe UI", 8, "bold")
BUTTON_FONT = ("Segoe UI", 10, "bold")
TITLE_FONT = ("Segoe UI", 13, "bold")
HEADER_FONT = ("Segoe UI", 18, "bold")

# Global variables to store font objects once loaded
_roca_one_header_font = None
_roca_one_title_font = None
_roca_one_loaded_flag = False # To track if custom font was successfully loaded

def load_custom_fonts():
    """
    Loads custom fonts. This function MUST be called AFTER tk.Tk() is initialized.
    """
    global _roca_one_header_font, _roca_one_title_font, _roca_one_loaded_flag
    global TITLE_FONT, HEADER_FONT # Also update the global font constants

    if _roca_one_loaded_flag: # Only load once
        return

    try:
        # Check if the font family "RocaOne" is already known to Tkinter,
        # which means it might have been loaded by the OS or a previous attempt.
        # This can still raise RuntimeError if called too early, which is why
        # this function is crucial.
        
        # We need to create a dummy root just to load fonts if one isn't available,
        # but in our App structure, the root is guaranteed when this function is called.
        
        # Attempt to create font instances by file path
        # A common way to load is to first add it via Tk's font system if needed,
        # but direct file loading can sometimes work on its own depending on Tk version.
        
        # Best practice is often to add via Tk().call if platform-specific methods are needed
        # Or simply rely on tkFont.Font(file=...) which handles adding it.

        # Test if the font can be created from file
        test_font_instance = tkFont.Font(family="RocaOne", file=ROCA_ONE_FONT_PATH, size=10)
        # If no error, it means the font file was processed.
        # Now, create the specific font objects for our use.
        
        # Define the font instances to be used by Tkinter widgets
        _roca_one_header_font = tkFont.Font(family="RocaOne", size=18)
        _roca_one_title_font = tkFont.Font(family="RocaOne", size=13)
        
        _roca_one_loaded_flag = True
        print(f"Successfully loaded custom font: {ROCA_ONE_FONT_PATH}")

        # Update the global font constants to use the custom font instances
        TITLE_FONT = _roca_one_title_font
        HEADER_FONT = _roca_one_header_font

    except Exception as e: # Catch any exception during font loading
        print(f"Warning: Could not load custom font '{ROCA_ONE_FONT_PATH}'. Using fallback fonts. Error: {e}")
        _roca_one_loaded_flag = False
        # Fallback fonts are already set as initial defaults, so no change needed here.


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
            # Image.LANCZOS is good for downsampling, previously Image.ANTIALIAS
            img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except FileNotFoundError:
        # print(f"Error: Image not found at {path}") # Commented out to reduce console spam
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
    # Use provided font_override or default BUTTON_FONT
    actual_font = font_override if font_override else BUTTON_FONT

    canvas = tk.Canvas(parent_frame, width=width, height=height, bd=0, highlightthickness=0, bg=WHITE_BG)
    
    create_rounded_rectangle(canvas, 1, 1, width-1, height-1, radius=int(height/2),
                             fill=color_light, outline=color_dark, width=1)

    button = tk.Button(canvas, text=text, command=command,
                       font=actual_font, fg="black", bg=color_light, bd=0,
                       activebackground=color_dark, activeforeground="white",
                       relief="flat")
    button.place(relx=0.5, rely=0.5, anchor="center", width=width - 6, height=height - 6)

    def on_enter(event):
        canvas.delete("all")
        create_rounded_rectangle(canvas, 1, 1, width-1, height-1, radius=int(height/2),
                                 fill=color_dark, outline=color_dark, width=1)
        button.config(fg="white", bg=color_dark)
        button.place(relx=0.5, rely=0.5, anchor="center", width=width - 6, height=height - 6) 
    def on_leave(event):
        canvas.delete("all")
        create_rounded_rectangle(canvas, 1, 1, width-1, height-1, radius=int(height/2),
                                 fill=color_light, outline=color_dark, width=1)
        button.config(fg="black", bg=color_light)
        button.place(relx=0.5, rely=0.5, anchor="center", width=width - 6, height=height - 6)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return canvas


def create_rounded_entry_field(parent_frame, label_text, textvariable, is_password=False, width=280):
    frame = tk.Frame(parent_frame, bg=WHITE_BG)
    frame.pack(anchor="center", pady=(5, 0))

    label = tk.Label(frame, text=label_text, font=GLOBAL_FONT, bg=WHITE_BG, fg=PUP_RED)
    label.pack(anchor="w", padx=10)

    entry_height = 25
    canvas_width = width
    canvas_height = entry_height + 4

    canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, bd=0, highlightthickness=0, bg=WHITE_BG)
    canvas.pack(pady=(2, 5))

    create_rounded_rectangle(canvas, 1, 1, canvas_width-1, canvas_height-1, radius=int(entry_height/2),
                             outline=PUP_RED, width=1, fill="white")

    entry = tk.Entry(canvas, font=GLOBAL_FONT, relief="flat", bd=0,
                     textvariable=textvariable, bg="white", fg=GRAY_TEXT, insertbackground=PUP_RED)
    entry.place(relx=0.5, rely=0.5, anchor="center", width=width-10, height=entry_height-4)

    if is_password:
        entry.config(show="*")
    return entry