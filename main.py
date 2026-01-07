from ui.ui import InventoryApp
from db import init_db

if __name__ == "__main__":
    init_db()
    app = InventoryApp()
    app.mainloop()