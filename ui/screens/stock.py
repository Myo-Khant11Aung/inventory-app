import customtkinter as ctk
from services import get_products


class StockScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # ---- STATE FIRST ----
        self.selected_product_id = None
        self.selected_product = None
        self.row_widgets = {}
        self.products = []

        # ---- UI BUILD ----
        self._configure_layout()
        self._build_header()
        self._build_table()

    # ---------- LAYOUT ----------

    def _configure_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _build_header(self):
        ctk.CTkLabel(
            self,
            text="Stock Dashboard",
            font=("Arial", 22)
        ).grid(
            row=0, column=0, pady=(20, 10), padx=20, sticky="ew"
        )

    def _build_table(self):
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(
            row=1, column=0, padx=20, pady=10, sticky="nsew"
        )
        self.table_frame.grid_columnconfigure(0, weight=1)

        self._build_headers()
        self.refresh()

    # ---------- TABLE ----------

    def _build_headers(self):
        headers = ["Name", "Qty", "Cost Pr", "Sell Pr"]

        header_frame = ctk.CTkFrame(self.table_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        header_frame.grid_columnconfigure(0, weight=3, uniform="header")
        header_frame.grid_columnconfigure((1, 2, 3), weight=1, uniform="header")

        for col, text in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=text,
                font=("Arial", 18, "bold"),
                anchor="w" if col == 0 else "e"
            ).grid(
                row=0, column=col, padx=10, pady=8,
                sticky="w" if col == 0 else "e"
            )

    def refresh(self):
        # Remove old rows (keep header)
        for widget in self.table_frame.winfo_children():
            if widget.grid_info().get("row") != 0:
                widget.destroy()
    
        self.row_widgets.clear()
        self.selected_product_id = None
        self.selected_product = None
    
        self.products = get_products()
    
        for row_index, product in enumerate(self.products, start=1):
            self._build_row(row_index, product)

    def _build_row(self, row_index, product):
        product_id, name, qty, cost_price, sell_price = product
    
        bg_color = "#2a2a2a" if row_index % 2 == 0 else "#1f1f1f"
    
        row = ctk.CTkFrame(
            self.table_frame,
            fg_color=bg_color,
            corner_radius=6
        )
        row.grid(row=row_index, column=0, sticky="ew", padx=6, pady=4)
    
        self.row_widgets[product_id] = row
    
        row.grid_columnconfigure(0, weight=3, uniform="row")
        row.grid_columnconfigure((1, 2, 3), weight=1, uniform="row")
    
        row.bind("<Button-1>", lambda e, pid=product_id: self._on_row_selected(pid))
    
        values = (name, qty, cost_price, sell_price)
    
        for col, value in enumerate(values):
            lbl = ctk.CTkLabel(
                row,
                text=f"{value:.2f}" if col in (2, 3) else str(value),
                font=("Arial", 16),
                anchor="w" if col == 0 else "e"
            )
            lbl.grid(
                row=0,
                column=col,
                padx=10,
                pady=6,
                sticky="w" if col == 0 else "e"
            )
            lbl.bind("<Button-1>", lambda e, pid=product_id: self._on_row_selected(pid))
    
    
    def _select_product(self, product):
        self.selected_product = product

    def _on_row_selected(self, product_id):
        # un-highlight previous
        if self.selected_product_id in self.row_widgets:
            self._set_row_highlight(self.selected_product_id, False)
    
        # highlight new
        self.selected_product_id = product_id
        self._set_row_highlight(product_id, True)
    
        # store selected product tuple
        self.selected_product = next(
            p for p in self.products if p[0] == product_id
        )

    def _set_row_highlight(self, product_id, selected):
        row = self.row_widgets.get(product_id)
        if not row:
            return
    
        if selected:
            row.configure(fg_color="#3b82f6")  # blue
        else:
            index = list(self.row_widgets.keys()).index(product_id)
            default_color = "#2a2a2a" if index % 2 == 0 else "#1f1f1f"
            row.configure(fg_color=default_color)
    
    
