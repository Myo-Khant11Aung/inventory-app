import customtkinter as ctk
from services import update_product
from tkinter import messagebox


class EditProductScreen(ctk.CTkFrame):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.on_success = on_success
        self.product_id = None

        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text="Edit Product",
            font=("Arial", 22)
        ).grid(row=0, column=0, columnspan=2, pady=(20, 30))

        self.name_entry = self._field("Name", 1)
        self.qty_entry = self._field("Quantity", 2)
        self.cost_entry = self._field("Cost Price", 3)
        self.sell_entry = self._field("Sell Price", 4)
        self.sku_entry = self._field("SKU", 5)

        self.save_button = ctk.CTkButton(
            self, text="Save Changes", command=self._on_save
        )
        self.save_button.grid(row=6, column=0, columnspan=2, pady=30)

    def _field(self, label, row):
        ctk.CTkLabel(self, text=label).grid(
            row=row, column=0, padx=20, pady=10, sticky="w"
        )
        entry = ctk.CTkEntry(self)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="ew")
        return entry
    
    def _on_save(self):
        self.save_button.configure(state="disabled", text="Saving...")
        self.after(10, self._save)
    
    def _save(self):
        try:
            update_product(
                self.product_id,
                self.name_entry.get().strip(),
                int(self.qty_entry.get()),
                float(self.cost_entry.get()),
                float(self.sell_entry.get()),
                self.sku_entry.get().strip() or None,
            )
            self.reset_form()
            self.on_success()
    
        except Exception as e:
            self.save_button.configure(state="normal", text="Save Changes")
            messagebox.showerror("Error", str(e))
    
    def reset_form(self):
        self.product_id = None
    
        for entry in (
            self.name_entry,
            self.qty_entry,
            self.cost_entry,
            self.sell_entry,
            self.sku_entry,
        ):
            entry.delete(0, "end")
    
        self.save_button.configure(state="normal", text="Save Changes")
    
    def load_product(self, product):
        self.reset_form()
    
        # product can be 5-tuple or 6-tuple depending on your SELECT
        if len(product) == 5:
            self.product_id, name, qty, cost, sell = product
            sku = None
        else:
            self.product_id, name, qty, cost, sell, sku = product
    
        self.name_entry.insert(0, name)
        self.qty_entry.insert(0, qty)
        self.cost_entry.insert(0, cost)
        self.sell_entry.insert(0, sell)
        if sku:
            self.sku_entry.insert(0, sku)
    
