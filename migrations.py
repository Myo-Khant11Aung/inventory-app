MIGRATIONS = [
    """
    CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
    );
    """,
    """
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sku TEXT UNIQUE,
        price REAL NOT NULL,
        qty INTEGER NOT NULL DEFAULT 0,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );
    """,

    """
    CREATE TABLE movements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        qty_change INTEGER NOT NULL,
        reason TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
    """,
    """
    ALTER TABLE products ADD COLUMN cost_price REAL NOT NULL DEFAULT 0;
    ALTER TABLE products ADD COLUMN sell_price REAL NOT NULL DEFAULT 0;
    """,
    
]