import tkinter as tk
import pandas as pd

from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from app.utils import parse_input_list
from app.generator import generate_tracks
from app.csv_handler import append_to_csv
from app.preview_table import PreviewTable

from app.excel_preview import ExcelPreviewTable


class RadarDatasetGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("Radar Emitter Dataset Generator")
        self.root.geometry("1100x750")
        self.root.configure(bg="#0f172a")
        self.root["padx"] = 10
        self.root["pady"] = 10

        self.staging_rows = []
        self.generated_rows = []

        self.excel_df = None

        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Progress bar
        self.style.configure(
            "blue.Horizontal.TProgressbar",
            troughcolor="#1e293b",
            background="#3b82f6",
            bordercolor="#1e293b",
            lightcolor="#3b82f6",
            darkcolor="#3b82f6"
        )

        # LabelFrame
        self.style.configure(
            "Card.TLabelframe",
            background="#0f172a",
            foreground="white",
            borderwidth=0
        )

        self.style.configure(
            "Card.TLabelframe.Label",
            background="#0f172a",
            foreground="#f8fafc",
            font=("Segoe UI", 11, "bold")
        )

        self.build_input_frame()
        self.build_control_frame()
        self.build_excel_preview_frame()
        self.build_preview_frame()
        self.build_stats_frame()

    def build_input_frame(self):

        frame = ttk.LabelFrame(
            self.root,
            text="Emitter Parameters",
            style="Card.TLabelframe",
            padding=10
        )

        frame.pack(fill="x", padx=10, pady=10)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)

        labels = [
            "Emitter Name",
            "Frequency List",
            "Frequency Tolerance %",
            "PRI List",
            "PRI Tolerance %",
            "PW List",
            "PW Tolerance %",
            "Scan Rate List",
            "Scan Tolerance %",
            "Tracks / Combination"
        ]

        self.entries = {}

        for i, label in enumerate(labels):

            tk.Label(
                frame,
                text=label,
                font=("Segoe UI", 10),
                bg="#111827",
                fg="white"
            ).grid(
                row=i,
                column=0,
                sticky="w",
                pady=5
            )

            entry = tk.Entry(
                frame,
                width=60,
                font=("Segoe UI", 10),
                bg="#1e293b",
                fg="white",
                insertbackground="white",
                relief="flat",
                bd=8
            )

            entry.grid(
                row=i,
                column=1,
                padx=10,
                pady=5
            )

            self.entries[label] = entry


    def build_control_frame(self):

        frame = tk.Frame(self.root, bg="#0f172a")

        frame.pack(fill="x", padx=10, pady=10)

        for i in range(6):
            frame.columnconfigure(i, weight=1)

        # -----------------------------
        # PROGRESS BAR
        # -----------------------------

        self.progress = ttk.Progressbar(
            frame,
            orient="horizontal",
            mode="determinate",
            style="blue.Horizontal.TProgressbar"
        )

        self.progress.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        # -----------------------------
        # GENERATE BUTTON
        # -----------------------------

        generate_btn = tk.Button(
            frame,
            text="Generate To Staging",
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=10,
            cursor="hand2",
            width=18,
            command=self.generate_dataset
        )

        generate_btn.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        # -----------------------------
        # APPEND BUTTON
        # -----------------------------

        append_btn = tk.Button(
            frame,
            text="Append Staging",
            bg="#10b981",
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=10,
            cursor="hand2",
            width=18,
            command=self.append_staging
        )

        append_btn.grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

        # -----------------------------
        # CLEAR BUTTON
        # -----------------------------

        clear_btn = tk.Button(
            frame,
            text="Clear Staging",
            bg="#ef4444",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=10,
            cursor="hand2",
            width=18,
            command=self.clear_staging
        )

        clear_btn.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        # -----------------------------
        # SAVE BUTTON
        # -----------------------------

        save_btn = tk.Button(
            frame,
            text="Save Final CSV",
            bg="#3b82f6",
            fg="white",
            activebackground="#3b82f6",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=10,
            cursor="hand2",
            width=18,
            command=self.save_csv
        )

        save_btn.grid(
            row=0,
            column=4,
            padx=5,
            pady=5
        )

        load_btn = tk.Button(
            frame,
            text="Load Excel",
            bg="#8b5cf6",
            fg="white",
            activebackground="#7c3aed",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=10,
            cursor="hand2",
            width=18,
            command=self.load_excel
        )       

        load_btn.grid(
            row=0,
            column=5,
            padx=5,
            pady=5
        )
    
    def build_excel_preview_frame(self):

        frame = ttk.LabelFrame(
            self.root,
            text="Excel Emitter Library",
            style="Card.TLabelframe",
            padding=10
        )

        frame.pack(
            fill="both",
            expand=False,
            padx=10,
            pady=10
        )

        self.excel_preview = ExcelPreviewTable(
            frame,
            self.fill_form_from_excel
        )

    def build_preview_frame(self):

        frame = ttk.LabelFrame(
            self.root,
            text="Dataset Preview",
            style="Card.TLabelframe",
            padding=10
        )

        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.preview = PreviewTable(frame)


    def build_stats_frame(self):

        frame = ttk.LabelFrame(
            self.root,
            text="Statistics",
            style="Card.TLabelframe",
            padding=10
        )

        frame.pack(fill="x", padx=20, pady=15)

        self.stats_label = tk.Label(
            frame,
            text="Rows: 0 | Combinations: 0",
            font=("Segoe UI", 10, "bold"),
            bg="#111827",
            fg="#38bdf8",
            pady=10
        )

        self.stats_label.pack(anchor="w")



    def generate_dataset(self):

        try:

            # -----------------------------
            # INPUT EXTRACTION
            # -----------------------------

            emitter = self.entries[
                "Emitter Name"
            ].get().strip()

            freqs = parse_input_list(
                self.entries["Frequency List"].get()
            )

            freq_tol = float(
                self.entries[
                    "Frequency Tolerance %"
                ].get() or 0
            )

            pris = parse_input_list(
                self.entries["PRI List"].get()
            )

            pri_tol = float(
                self.entries[
                    "PRI Tolerance %"
                ].get() or 0
            )

            pws = parse_input_list(
                self.entries["PW List"].get()
            )

            pw_tol = float(
                self.entries[
                    "PW Tolerance %"
                ].get() or 0
            )

            scans = parse_input_list(
                self.entries["Scan Rate List"].get()
            )

            scan_tol = float(
                self.entries[
                    "Scan Tolerance %"
                ].get() or 0
            )

            tracks = int(
                self.entries[
                    "Tracks / Combination"
                ].get()
            )

            # -----------------------------
            # VALIDATION
            # -----------------------------

            if not emitter:
                raise ValueError(
                    "Emitter name cannot be empty."
                )

            if not freqs:
                raise ValueError(
                    "Frequency list cannot be empty."
                )

            if not pris:
                raise ValueError(
                    "PRI list cannot be empty."
                )

            if not pws:
                raise ValueError(
                    "PW list cannot be empty."
                )

            if tracks <= 0:
                raise ValueError(
                    "Tracks must be greater than 0."
                )

            # -----------------------------
            # HANDLE OPTIONAL SCAN
            # -----------------------------

            scan_count = len(scans) if scans else 1

            combinations = (
                len(freqs)
                * len(pris)
                * len(pws)
                * scan_count
            )

            # -----------------------------
            # RESET PROGRESS BAR
            # -----------------------------

            self.progress["value"] = 0

            self.progress["maximum"] = combinations

            self.root.update_idletasks()

            # -----------------------------
            # GENERATE DATASET
            # -----------------------------

            rows = generate_tracks(
                freqs,
                pris,
                pws,
                scans,
                freq_tol,
                pri_tol,
                pw_tol,
                scan_tol,
                tracks,
                emitter
            )

            # -----------------------------
            # STORE GENERATED ROWS
            # -----------------------------

            self.staging_rows.extend(rows)

            # -----------------------------
            # UPDATE PREVIEW TABLE
            # -----------------------------

            self.preview.insert_rows(self.staging_rows)

            # -----------------------------
            # UPDATE PROGRESS BAR
            # -----------------------------

            self.progress["value"] = combinations

            # -----------------------------
            # UPDATE STATISTICS
            # -----------------------------

            self.stats_label.config(
                text=(
                    f"Staging Rows: {len(self.staging_rows)} | "
                    f"Final Rows: {len(self.generated_rows)} | "
                    f"Last Combos: {combinations}"
                )
            )

            # -----------------------------
            # SUCCESS MESSAGE
            # -----------------------------

            preview_limit = min(200, len(self.staging_rows))

            messagebox.showinfo(
                "Success",
                (
                    f"{len(rows)} rows generated.\n"
                    f"Previewing first {preview_limit} rows."
                )
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def append_staging(self):

        if not self.staging_rows:

            messagebox.showwarning(
                "Warning",
                "No staging data available."
            )

            return

        appended_count = len(self.staging_rows)

        self.generated_rows.extend(
            self.staging_rows
        )

        self.staging_rows.clear()

        self.preview.clear()

        self.stats_label.config(
            text=(
                f"Staging Rows: 0 | "
                f"Final Rows: {len(self.generated_rows)}"
            )
        )

        messagebox.showinfo(
            "Success",
            (
                f"{appended_count} staging rows "
                f"appended to final dataset."
            )
        )


    def clear_staging(self):

        self.staging_rows.clear()

        self.preview.clear()

        self.stats_label.config(
            text=(
                f"Staging Rows: 0 | "
                f"Final Rows: {len(self.generated_rows)}"
            )
        )

        messagebox.showinfo(
            "Cleared",
            "Staging dataset cleared."
        )

    def load_excel(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Excel Files", "*.xlsx *.xls")
            ]
        )

        if not file_path:
            return

        try:

            self.excel_df = pd.read_excel(
                file_path
            )

            required_columns = [
                "Freq",
                "PRI",
                "PW",
                "Scan Rate",
                "Class"
            ]

            for col in required_columns:

                if col not in self.excel_df.columns:

                    raise ValueError(
                        f"Missing column: {col}"
                    )

            self.excel_preview.insert_dataframe(
                self.excel_df
            )

            messagebox.showinfo(
                "Success",
                "Excel file loaded successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def fill_form_from_excel(self, row_data):

        for key, value in row_data.items():

            if key not in self.entries:
                continue

            self.entries[key].delete(0, tk.END)

            if pd.isna(value):
                continue

            self.entries[key].insert(
                0,
                str(value)
            )

    def save_csv(self):

        if not self.generated_rows:

            messagebox.showwarning(
                "Warning",
                "No data generated."
            )

            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )

        if not file_path:
            return

        append_to_csv(
            self.generated_rows,
            file_path
        )

        messagebox.showinfo(
            "Saved",
            f"Dataset saved to:\n{file_path}"
        )
