from tkinter import ttk

class PreviewTable:

    def __init__(self, parent):

        columns = (
            "frequency",
            "pri",
            "pw",
            "scan_rate",
            "emitter"
        )

        self.tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=12
        )

        for col in columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=120)

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            parent,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscroll=scrollbar.set)

        scrollbar.grid(row=0, column=1, sticky="ns")

    def clear(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def insert_rows(self, rows, limit=200):

        self.clear()

        for row in rows[:limit]:
            self.tree.insert(
                "",
                "end",
                values=(
                    row["frequency"],
                    row["pri"],
                    row["pw"],
                    row["scan_rate"],
                    row["emitter"]
                )
            )