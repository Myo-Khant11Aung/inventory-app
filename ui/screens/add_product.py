import customtkinter as ctk
from services import add_product
from tkinter import messagebox


class AddProductScreen(ctk.CTkFrame):
    def __init__(self, parent, on_success):
        super().__init__(parent)

        self.on_success = on_success
        self.grid_columnconfigure(1, weight=1)

        self._build_header()
        self._build_form()
        self._build_actions()

    # ---------- UI BUILDING ----------

    def _build_header(self):
        ctk.CTkLabel(
            self,
            text="Add Product",
            font=("Arial", 22)
        ).grid(row=0, column=0, columnspan=2, pady=(20, 30))

    def _build_form(self):
        self.name_entry = self._field("Name", 1)
        self.qty_entry = self._field("Quantity", 2)
        self.cost_entry = self._field("Cost Price", 3)
        self.sell_entry = self._field("Sell Price", 4)
        self.sku_entry = self._field("SKU (optional)", 5)

    def _build_actions(self):
        self.save_button = ctk.CTkButton(
            self,
            text="Save Product",
            command=self._on_save_clicked
        )
        self.save_button.grid(row=6, column=0, columnspan=2, pady=30)

    def _field(self, label, row):
        ctk.CTkLabel(self, text=label).grid(
            row=row, column=0, padx=20, pady=10, sticky="w"
        )
        entry = ctk.CTkEntry(self, corner_radius=4)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="ew")
        return entry

    # ---------- LOGIC ----------

    def _on_save_clicked(self):
        """UI-safe click handler"""
        self.save_button.configure(state="disabled", text="Saving...")
        self.after(10, self._save_product)  # let UI repaint first

    def _save_product(self):
        try:
            data = self._collect_form_data()
            add_product(**data)
            self.reset_form()
            self.on_success()

        except Exception as e:
            self._restore_button()
            messagebox.showerror("Error", str(e))

    def _collect_form_data(self):
        name = self.name_entry.get().strip()
        if not name:
            raise ValueError("Name is required")

        return {
            "name": name,
            "qty": int(self.qty_entry.get()),
            "cost_price": float(self.cost_entry.get()),
            "sell_price": float(self.sell_entry.get()),
            "sku": self.sku_entry.get().strip() or None,
        }

    def _restore_button(self):
        self.save_button.configure(state="normal", text="Save Product")

    def reset_form(self):
        for entry in (
            self.name_entry,
            self.qty_entry,
            self.cost_entry,
            self.sell_entry,
            self.sku_entry,
        ):
            entry.delete(0, "end")
    
        self.save_button.configure(
            state="normal",
            text="Save Product"
        )


