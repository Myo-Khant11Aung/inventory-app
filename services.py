import db

"""has an extra column of price in products table"""


def add_product(name, qty, cost_price=0, sell_price=0, sku=None):
    if not name:
        raise ValueError("Product name is required")
    if cost_price < 0:
        raise ValueError("Cost price cannot be negative")
    if sell_price < 0:
        raise ValueError("Sell price cannot be negative")
    if qty < 0:
        raise ValueError("Quantity cannot be negative")

    with db.connect_db() as conn:
        conn.execute(
            """
            INSERT INTO products (name, sku, price, qty, cost_price, sell_price)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, sku, sell_price, qty, cost_price, sell_price)
        )


def get_products():
    with db.connect_db() as conn:
        return conn.execute(
            "SELECT id,name, qty, cost_price, sell_price FROM products ORDER BY name"
        ).fetchall()

def get_categories():
    with db.connect_db() as conn:
        return conn.execute(
            "SELECT id, name FROM categories ORDER BY name"
        ).fetchall()

def add_category(name):
    if not name:
        raise ValueError("Category name is required")

    with db.connect_db() as conn:
        conn.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (name,)
        )
def update_product(product_id, name, qty, cost_price, sell_price, sku=None):
    with db.connect_db() as conn:
        conn.execute(
            """
            UPDATE products
            SET name = ?, qty = ?, cost_price = ?, sell_price = ?, sku = ?, price = ?
            WHERE id = ?
            """,
            (name, qty, cost_price, sell_price, sku, sell_price, product_id)
        )

def apply_movement(product_id, qty_change, reason=None):
    with db.connect_db() as conn:
        cur = conn.cursor()

        # Update product quantity
        cur.execute(
            "UPDATE products SET qty = qty + ? WHERE id = ?",
            (qty_change, product_id)
        )

        # Record movement
        cur.execute(
            """
            INSERT INTO movements (product_id, qty_change, reason)
            VALUES (?, ?, ?)
            """,
            (product_id, qty_change, reason)
        )

def get_product_choices():
    with db.connect_db() as conn:
        return conn.execute(
            "SELECT id, name FROM products ORDER BY name"
        ).fetchall()
    
def get_product_by_id(product_id):
    with db.connect_db() as conn:
        return conn.execute(
            "SELECT id, name, qty, cost_price, sell_price, sku FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()
    
def delete_product(product_id):
    with db.connect_db() as conn:
        cur = conn.cursor()

        # delete movements first
        cur.execute(
            "DELETE FROM movements WHERE product_id = ?",
            (product_id,)
        )

        # delete product
        cur.execute(
            "DELETE FROM products WHERE id = ?",
            (product_id,)
        )

