import customtkinter as ctk
from ui.screens.add_product import AddProductScreen
from ui.screens.stock import StockScreen
from ui.screens.edit import EditProductScreen
from ui.screens.movement import MovementsScreen
from services import delete_product
from tkinter import messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class InventoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Inventory Management System")
        self.geometry("1000x600")

        self._configure_layout()
        self._build_sidebar()
        self._build_main_area()
        self._build_screens()

        self.show_stock()

    # ---------- LAYOUT ----------

    def _configure_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="Inventory",
            font=("Arial", 18)
        ).pack(pady=(20, 30))

        self._sidebar_button("Stock", self.show_stock)
        self._sidebar_button("Add Product", self.show_add_product)
        self._sidebar_button("Stock In / Out", self.show_movements)
        self._sidebar_button("Edit Product", self.show_edit_product)
        self._sidebar_button_delete("Delete", self.delete_selected_product)



    def _sidebar_button(self, text, command):
        ctk.CTkButton(
            self.sidebar,
            text=text,
            command=lambda: self.after(10, command)
        ).pack(fill="x", padx=10, pady=6)

    def _sidebar_button_delete(self, text, command):
        ctk.CTkButton(
            self.sidebar,
            text=text,
            command=lambda: self.after(10, command), fg_color="#7f1d1d", hover_color="#991b1b"
        ).pack(fill="x", padx=10, pady=6)


    def _build_main_area(self):
        self.main_area = ctk.CTkFrame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

    # ---------- SCREENS ----------

    def _build_screens(self):
        self.stock_screen = StockScreen(self.main_area)

        self.add_product_screen = AddProductScreen(
            self.main_area,
            on_success=self._on_product_added
        )
        self.edit_product_screen = EditProductScreen(
            self.main_area,
            on_success=self._on_product_edited
        )
        self.movements_screen = MovementsScreen(
            self.main_area,
            on_success=self._on_movement_applied
        )
        self.screens = {
            "stock": self.stock_screen,
            "add_product": self.add_product_screen,
            "edit_product": self.edit_product_screen,
            "movements": self.movements_screen,
        }

        for screen in self.screens.values():
            screen.grid(row=0, column=0, sticky="nsew")

    # ---------- NAVIGATION ----------

    def show_stock(self):
        self.screens["stock"].tkraise()
        self.after(50, self.stock_screen.refresh)

    def show_add_product(self):
        self.add_product_screen.reset_form()
        self.screens["add_product"].tkraise()

    def show_movements(self):
        fresh_product = self._get_fresh_selected_product()
        if not fresh_product:
            return
    
        self.movements_screen.load_product(fresh_product)
        self.screens["movements"].tkraise()

    # ---------- CALLBACKS ----------

    def _on_product_added(self):
        self.show_stock()

    def show_edit_product(self):
        fresh_product = self._get_fresh_selected_product()
        if not fresh_product:
            return
    
        self.edit_product_screen.load_product(fresh_product)
        self.screens["edit_product"].tkraise()

    def _refresh_all_product_data(self):
    
        # Refresh movements dropdown if screen exists
        if hasattr(self.movements_screen, "refresh_products"):
            self.movements_screen.refresh_products()
    
        # Refresh edit dropdown if you later convert edit to dropdown
        if hasattr(self.edit_product_screen, "refresh_products"):
            self.edit_product_screen.refresh_products()
    
    def _on_movement_applied(self):
       self._refresh_all_product_data()
       self.show_stock()

    def _on_product_edited(self):
       self._refresh_all_product_data()
       self.show_stock()

    def _get_fresh_selected_product(self):
        product = getattr(self.stock_screen, "selected_product", None)
        if not product:
            return None
    
        product_id = product[0]  # always id first
        from services import get_product_by_id
        return get_product_by_id(product_id)
    
    def delete_selected_product(self):
        product = self.stock_screen.selected_product
        if not product:
            messagebox.showwarning(
                "No selection",
                "Please select a product to delete."
            )
            return
    
        product_id, name, *_ = product
    
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete '{name}'?\n\nThis cannot be undone."
        )
    
        if not confirm:
            return
    
        delete_product(product_id)
    
        # refresh UI
        self.stock_screen.refresh()
    
