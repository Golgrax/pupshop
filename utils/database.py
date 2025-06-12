import sqlite3
import bcrypt
import os

# Determine the base directory for the database file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db', 'pup_shop.db')

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def execute_query(self, query, params=()):
        self.connect()
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def fetch_one(self, query, params=()):
        self.connect()
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        self.connect()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def create_tables(self):
        self.connect()
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock_quantity INTEGER NOT NULL,
                image_path TEXT,
                category TEXT,
                description TEXT,
                rating REAL DEFAULT 0.0,
                sales_count INTEGER DEFAULT 0
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                address_line TEXT NOT NULL,
                contact_name TEXT NOT NULL,
                contact_no TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT NOT NULL, -- e.g., 'Pending', 'Shipped', 'Delivered', 'Cancelled'
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                item_price_at_order REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, -- NULLable if not logged in
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            );
            """
        ]
        for query in queries:
            if not self.execute_query(query):
                print(f"Failed to create table with query: {query}")
        print("Database tables checked/created.")

        # Seed initial data for products if table is empty
        self._seed_products()

    def _seed_products(self):
        # Check if products table is empty
        if self.fetch_one("SELECT COUNT(*) FROM products")[0] == 0:
            print("Seeding initial product data...")
            products_to_seed = [
                ("PUP Minimalist Baybayin Lanyard", 140.00, 100, "product_lanyard.png", "Lanyard", "Coquette Baybayin Lanyard, PUP Study With Style."),
                ("PUP Jeepney Signage", 20.00, 200, "product_jeepney_signage.png", "Sticker", "Iskolar Script - PUP Study with Style Stickers."),
                ("PUP Iskolar TOTE BAG", 160.00, 75, "product_iskolar_tote_bag.png", "Bag", "Iskolar Script - PUP Study with Style Tote Bags."),
                ("PUP Study With Style (T-Shirt)", 450.00, 50, "product_study_with_style.png", "Apparel", "PUP Obelisk silhouette - STUDY With Style."),
                # Add more products from the PDF as needed
                ("PUP Baybayin Lanyard (Classic Edition)", 140.00, 100, "product_lanyard.png", "Lanyard", "Classic Edition Polytechnic University (PUP)Lanyard.") # Assuming the other lanyard is this one
            ]
            for prod in products_to_seed:
                self.execute_query(
                    "INSERT INTO products (name, price, stock_quantity, image_path, category, description) VALUES (?, ?, ?, ?, ?, ?)",
                    prod
                )
            print("Product seeding complete.")

