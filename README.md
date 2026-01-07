# Inventory Management Desktop App

A simple, offline-first inventory management desktop application built with Python, CustomTkinter, and SQLite.

This app is designed for small businesses that need a lightweight, local solution for tracking products and stock movements without cloud services, subscriptions, or accounts.

---

## Features

- View all products in a stock dashboard
- Add new products
- Edit existing product details
- Stock In / Stock Out with movement tracking
- Delete products with confirmation
- Visual row selection highlighting
- Persistent local SQLite database
- macOS desktop application build

---

## Tech Stack

- Python 3
- CustomTkinter (desktop UI)
- SQLite (local database)
- PyInstaller (macOS app packaging)

---

## Database

The application uses a local SQLite database stored at:

~/.inverntory_app/inventory.db


The database file is intentionally not tracked in Git and persists across app updates and rebuilds.

---

## Project Structure

inventory_app/
├── main.py
├── services.py
├── db.py
├── migrations.py
├── ui/
│ ├── ui.py
│ └── screens/
│ ├── stock.py
│ ├── add_product.py
│ ├── edit.py
│ └── movement.py
├── README.md
└── .gitignore


---

## Run Locally (Development)

```bash
pip install customtkinter
python3 main.py
```
**##Build MacOS app**

```
pip install pyinstaller

pyinstaller \
  --windowed \
  --onefile \
  --name "Inventory" \
  main.py
```

The built application will be available at:

dist/Inventory.app

**##macOS Security Notice**

Because the app is unsigned, macOS may block it on first launch.

To open the app:
Right-click Inventory.app
Click Open
Click Open again
This is required only once.


