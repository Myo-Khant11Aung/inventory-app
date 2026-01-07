import customtkinter as ctk
from services import apply_movement
from tkinter import messagebox


class MovementsScreen(ctk.CTkFrame):
    def __init__(self, parent, on_success):
        super().__init__(parent)

        self.on_success = on_success
        self.product = None

        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text="Stock In / Out",
            font=("Arial", 22)
        ).grid(row=0, column=0, columnspan=2, pady=(20, 30))

        self.product_label = ctk.CTkLabel(self, text="")
        self.product_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.qty_entry = self._field("Quantity Change (+ / -)", 2)
        self.reason_entry = self._field("Reason (optional)", 3)

        self.apply_button = ctk.CTkButton(
            self,
            text="Apply",
            command=self._on_apply
        )
        self.apply_button.grid(row=4, column=0, columnspan=2, pady=30)

    def _field(self, label, row):
        ctk.CTkLabel(self, text=label).grid(
            row=row, column=0, padx=20, pady=10, sticky="w"
        )
        entry = ctk.CTkEntry(self)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="ew")
        return entry

    def load_product(self, product):
        self.reset_form()
        self.product = product
    
        product_id, name, qty, *_ = product
        self.product_label.configure(
            text=f"{name} (Current Stock: {qty})"
        )
    def reset_form(self):
        self.product = None
        self.qty_entry.delete(0, "end")
        self.reason_entry.delete(0, "end")
        self.apply_button.configure(state="normal", text="Apply")
    
    def _on_apply(self):
        self.apply_button.configure(state="disabled", text="Applying...")
        self.after(10, self._apply)
    
    def _apply(self):
        try:
            if not self.product:
                raise ValueError("No product selected")
    
            qty_change = int(self.qty_entry.get())
            reason = self.reason_entry.get().strip() or None
            product_id = self.product[0]
    
            apply_movement(product_id, qty_change, reason)
    
            self.reset_form()
            self.on_success()
    
        except Exception as e:
            self.apply_button.configure(state="normal", text="Apply")
            messagebox.showerror("Error", str(e))
    