from tkinter import ttk


class ExcelPreviewTable:

    def __init__(self, parent, on_row_select):

        self.on_row_select = on_row_select

        columns = (
            "class",
            "freq",
            "pri",
            "pw",
            "scan_rate"
        )

        self.tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=8
        )

        for col in columns:

            self.tree.heading(
                col,
                text=col.upper()
            )

            self.tree.column(
                col,
                width=180
            )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar = ttk.Scrollbar(
            parent,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscroll=scrollbar.set
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.row_selected
        )

    # ---------------------------------
    # CLEAR TABLE
    # ---------------------------------

    def clear(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

    # ---------------------------------
    # INSERT DATAFRAME
    # ---------------------------------

    def insert_dataframe(self, df):

        self.clear()

        for _, row in df.iterrows():

            self.tree.insert(
                "",
                "end",
                values=(
                    row["Class"],
                    row["Freq"],
                    row["PRI"],
                    row["PW"],
                    row["Scan Rate"]
                )
            )

    # ---------------------------------
    # ROW CLICK EVENT
    # ---------------------------------

    def row_selected(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(selected[0])

        values = item["values"]

        row_data = {

            "Emitter Name": values[0],
            "Frequency List": values[1],
            "PRI List": values[2],
            "PW List": values[3],
            "Scan Rate List": values[4]
        }

        self.on_row_select(row_data)