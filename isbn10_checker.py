import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------
# ISBN-10 Logic Functions
# -----------------------

def clean_isbn(isbn: str) -> str:
    return isbn.replace("-", "").replace(" ", "").upper()

def compute_check_digit(isbn9: str) -> str:
    total = 0
    weight = 10
    for ch in isbn9:
        total += int(ch) * weight
        weight -= 1
    check_digit = (11 - (total % 11)) % 11
    return "X" if check_digit == 10 else str(check_digit)

def is_valid_isbn10(isbn10: str) -> bool:
    s = clean_isbn(isbn10)
    if len(s) != 10:
        return False
    if not s[:9].isdigit():
        return False
    if not (s[9].isdigit() or s[9] == "X"):
        return False

    total = 0
    weight = 10
    for i in range(10):
        val = 10 if s[i] == "X" else int(s[i])
        total += val * weight
        weight -= 1
    return total % 11 == 0


# -----------------------
# GUI App
# -----------------------

class ISBNApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ISBN-10 Checker & Fixer")
        self.geometry("980x600")
        self.minsize(980, 600)

        self._setup_style()
        self._build_ui()
        self._setup_text_tags()

    # -----------------------
    # UI Styling
    # -----------------------

    def _setup_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        self.configure(bg="#0f172a")  # slate-900

        style.configure("App.TFrame", background="#0f172a")
        style.configure("Card.TFrame", background="#111827")
        style.configure("CardTitle.TLabel", background="#111827", foreground="#e5e7eb",
                        font=("Segoe UI", 12, "bold"))
        style.configure("Title.TLabel", background="#0f172a", foreground="#f8fafc",
                        font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", background="#0f172a", foreground="#cbd5e1",
                        font=("Segoe UI", 10))
        style.configure("Field.TLabel", background="#111827", foreground="#cbd5e1",
                        font=("Segoe UI", 10))
        style.configure("Status.TLabel", background="#111827", foreground="#cbd5e1",
                        font=("Segoe UI", 10, "bold"))

        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8))
        style.configure("Ghost.TButton", font=("Segoe UI", 10), padding=(12, 8))

        style.configure("TNotebook", background="#0f172a", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(14, 10), font=("Segoe UI", 10, "bold"))

    # -----------------------
    # Build Layout
    # -----------------------

    def _build_ui(self):
        root = ttk.Frame(self, style="App.TFrame")
        root.pack(fill="both", expand=True, padx=18, pady=18)

        header = ttk.Frame(root, style="App.TFrame")
        header.pack(fill="x", pady=(0, 14))
        ttk.Label(header, text="ISBN-10 Checker & Fixer", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Validate ISBN-10 numbers and generate the correct check digit if invalid. Single & Batch testing.",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(4, 0))

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        self.single_tab = ttk.Frame(notebook, style="App.TFrame")
        self.batch_tab = ttk.Frame(notebook, style="App.TFrame")

        notebook.add(self.single_tab, text="Single Test")
        notebook.add(self.batch_tab, text="Batch Test")

        self._build_single_tab()
        self._build_batch_tab_right_results() 

        footer = ttk.Frame(root, style="App.TFrame")
        footer.pack(fill="x", pady=(14, 0))

        ttk.Button(footer, text="Clear All Results", style="Ghost.TButton",
                   command=self.clear_all_results).pack(side="left")
        ttk.Button(footer, text="Exit", style="Primary.TButton",
                   command=self.destroy).pack(side="right")

    # -----------------------
    # Single Test Tab (2 columns)
    # -----------------------

    def _build_single_tab(self):
        container = ttk.Frame(self.single_tab, style="App.TFrame")
        container.pack(fill="both", expand=True, padx=6, pady=6)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        # Left card: input
        in_card = ttk.Frame(container, style="Card.TFrame")
        in_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        in_card.columnconfigure(0, weight=1)

        ttk.Label(in_card, text="Input", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w", padx=14, pady=(12, 8)
        )
        ttk.Label(in_card, text="Enter ISBN-10 (hyphens optional):", style="Field.TLabel").grid(
            row=1, column=0, sticky="w", padx=14
        )

        self.single_entry = ttk.Entry(in_card, font=("Consolas", 12))
        self.single_entry.grid(row=2, column=0, sticky="ew", padx=14, pady=(8, 10))
        self.single_entry.bind("<Return>", lambda e: self.single_check())
        self.single_entry.focus()

        btn_row = ttk.Frame(in_card, style="Card.TFrame")
        btn_row.grid(row=3, column=0, sticky="w", padx=14, pady=(0, 14))

        ttk.Button(btn_row, text="Check & Fix", style="Primary.TButton",
                   command=self.single_check).pack(side="left")
        ttk.Button(btn_row, text="Clear", style="Ghost.TButton",
                   command=self.clear_single).pack(side="left", padx=10)

        self.single_status = ttk.Label(in_card, text="Status: —", style="Status.TLabel")
        self.single_status.grid(row=4, column=0, sticky="w", padx=14, pady=(0, 12))

        # Right card: result
        out_card = ttk.Frame(container, style="Card.TFrame")
        out_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        out_card.columnconfigure(0, weight=1)
        out_card.rowconfigure(1, weight=1)

        ttk.Label(out_card, text="Result", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w", padx=14, pady=(12, 8)
        )

        self.single_result = tk.Text(
            out_card, font=("Consolas", 11), wrap="word",
            bd=0, highlightthickness=0,
            bg="#0b1220", fg="#e5e7eb", insertbackground="#e5e7eb"
        )
        self.single_result.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))

    # -----------------------
    # Batch Test Tab (Input LEFT, Results RIGHT)
    # -----------------------

    def _build_batch_tab_right_results(self):
        container = ttk.Frame(self.batch_tab, style="App.TFrame")
        container.pack(fill="both", expand=True, padx=6, pady=6)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        # LEFT: Batch input card
        left = ttk.Frame(container, style="Card.TFrame")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(2, weight=1)

        ttk.Label(left, text="Batch Input", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w", padx=14, pady=(12, 8)
        )
        ttk.Label(left, text="Enter ISBN-10 values (one per line):", style="Field.TLabel").grid(
            row=1, column=0, sticky="w", padx=14
        )

        input_wrap = ttk.Frame(left, style="Card.TFrame")
        input_wrap.grid(row=2, column=0, sticky="nsew", padx=14, pady=(8, 10))
        input_wrap.columnconfigure(0, weight=1)
        input_wrap.rowconfigure(0, weight=1)

        input_scroll = ttk.Scrollbar(input_wrap, orient="vertical")
        input_scroll.grid(row=0, column=1, sticky="ns")

        self.batch_input = tk.Text(
            input_wrap, font=("Consolas", 11), wrap="none",
            bd=0, highlightthickness=0,
            bg="#0b1220", fg="#e5e7eb", insertbackground="#e5e7eb",
            yscrollcommand=input_scroll.set
        )
        self.batch_input.grid(row=0, column=0, sticky="nsew")
        input_scroll.config(command=self.batch_input.yview)

        btn_row = ttk.Frame(left, style="Card.TFrame")
        btn_row.grid(row=3, column=0, sticky="w", padx=14, pady=(0, 12))

        ttk.Button(btn_row, text="Run Batch Test", style="Primary.TButton",
                   command=self.run_batch).pack(side="left")
        ttk.Button(btn_row, text="Clear", style="Ghost.TButton",
                   command=self.clear_batch).pack(side="left", padx=10)

        self.batch_status = ttk.Label(left, text="Status: —", style="Status.TLabel")
        self.batch_status.grid(row=4, column=0, sticky="w", padx=14, pady=(0, 12))

        # RIGHT: Batch results card
        right = ttk.Frame(container, style="Card.TFrame")
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        ttk.Label(right, text="Batch Results", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w", padx=14, pady=(12, 8)
        )

        results_wrap = ttk.Frame(right, style="Card.TFrame")
        results_wrap.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        results_wrap.columnconfigure(0, weight=1)
        results_wrap.rowconfigure(0, weight=1)

        results_scroll = ttk.Scrollbar(results_wrap, orient="vertical")
        results_scroll.grid(row=0, column=1, sticky="ns")

        self.batch_result = tk.Text(
            results_wrap, font=("Consolas", 11), wrap="word",
            bd=0, highlightthickness=0,
            bg="#0b1220", fg="#e5e7eb", insertbackground="#e5e7eb",
            yscrollcommand=results_scroll.set
        )
        self.batch_result.grid(row=0, column=0, sticky="nsew")
        results_scroll.config(command=self.batch_result.yview)

    # -----------------------
    # Tags + Status
    # -----------------------

    def _setup_text_tags(self):
        for t in (self.single_result, self.batch_result):
            t.tag_configure("good", foreground="#22c55e")
            t.tag_configure("bad", foreground="#ef4444")
            t.tag_configure("muted", foreground="#94a3b8")
            t.tag_configure("bold", font=("Consolas", 11, "bold"))

    def _set_status(self, which: str, kind: str, text: str):
        color = {"good": "#22c55e", "bad": "#ef4444", "muted": "#cbd5e1"}.get(kind, "#cbd5e1")
        if which == "single":
            self.single_status.configure(text=text, foreground=color)
        else:
            self.batch_status.configure(text=text, foreground=color)

    # -----------------------
    # Actions
    # -----------------------

    def single_check(self):
        raw = self.single_entry.get().strip()
        self.single_result.delete("1.0", tk.END)

        if not raw:
            messagebox.showwarning("Missing Input", "Please enter an ISBN-10.")
            self._set_status("single", "bad", "Status: Missing input")
            return

        s = clean_isbn(raw)

        if len(s) != 10 or not s[:9].isdigit() or not (s[9].isdigit() or s[9] == "X"):
            self.single_result.insert(tk.END, "INVALID FORMAT ❌\n", ("bad", "bold"))
            self.single_result.insert(tk.END, f"\nInput:   {raw}\n", "muted")
            self.single_result.insert(tk.END, f"Cleaned: {s}\n", "muted")
            self._set_status("single", "bad", "Status: Invalid format")
            return

        if is_valid_isbn10(raw):
            self.single_result.insert(tk.END, "VALID ISBN ✅\n", ("good", "bold"))
            self.single_result.insert(tk.END, f"\nInput:   {raw}\n", "muted")
            self.single_result.insert(tk.END, f"Cleaned: {s}\n", "muted")
            self._set_status("single", "good", "Status: Valid")
        else:
            correct = compute_check_digit(s[:9])
            corrected = s[:9] + correct
            self.single_result.insert(tk.END, "INVALID ISBN ❌\n", ("bad", "bold"))
            self.single_result.insert(tk.END, f"\nInput:   {raw}\n", "muted")
            self.single_result.insert(tk.END, f"Cleaned: {s}\n\n", "muted")
            self.single_result.insert(tk.END, "Correct check digit: ", "muted")
            self.single_result.insert(tk.END, f"{correct}\n", ("bad", "bold"))
            self.single_result.insert(tk.END, "Correct ISBN-10:     ", "muted")
            self.single_result.insert(tk.END, f"{corrected}\n", ("good", "bold"))
            self._set_status("single", "bad", "Status: Invalid (fixed)")

    def run_batch(self):
        self.batch_result.delete("1.0", tk.END)
        lines = [ln.strip() for ln in self.batch_input.get("1.0", tk.END).splitlines() if ln.strip()]

        if not lines:
            messagebox.showwarning("Missing Input", "Please enter at least one ISBN in Batch Input.")
            self._set_status("batch", "bad", "Status: Missing input")
            return

        valid_count = 0
        invalid_count = 0
        format_count = 0

       # self.batch_result.insert(tk.END, "--- Batch Test Results ---\n\n", ("muted", "bold"))

        for isbn in lines:
            s = clean_isbn(isbn)

            if len(s) != 10 or not s[:9].isdigit() or not (s[9].isdigit() or s[9] == "X"):
                self.batch_result.insert(tk.END, f"{isbn} → ", "muted")
                self.batch_result.insert(tk.END, "Invalid format\n", ("bad", "bold"))
                format_count += 1
                continue

            if is_valid_isbn10(isbn):
                self.batch_result.insert(tk.END, f"{isbn} → ", "muted")
                self.batch_result.insert(tk.END, "VALID ✅\n", ("good", "bold"))
                valid_count += 1
            else:
                correct = compute_check_digit(s[:9])
                self.batch_result.insert(tk.END, f"{isbn} → ", "muted")
                self.batch_result.insert(tk.END, "INVALID ❌ ", ("bad", "bold"))
                self.batch_result.insert(tk.END, f"(correct digit: {correct})\n", "muted")
                invalid_count += 1

        self.batch_result.insert(tk.END, "\nSummary:\n", ("muted", "bold"))
        self.batch_result.insert(
            tk.END,
            f"Valid: {valid_count}   Invalid: {invalid_count}   Format errors: {format_count}\n",
            "muted"
        )

        self.batch_result.see(tk.END)

        if format_count > 0:
            self._set_status("batch", "bad", "Status: Done (some format errors)")
        else:
            self._set_status("batch", "good", "Status: Done")

    def clear_single(self):
        self.single_entry.delete(0, tk.END)
        self.single_result.delete("1.0", tk.END)
        self._set_status("single", "muted", "Status: —")
        self.single_entry.focus()

    def clear_batch(self):
        self.batch_input.delete("1.0", tk.END)
        self.batch_result.delete("1.0", tk.END)
        self._set_status("batch", "muted", "Status: —")

    def clear_all_results(self):
        self.single_result.delete("1.0", tk.END)
        self.batch_result.delete("1.0", tk.END)
        self._set_status("single", "muted", "Status: —")
        self._set_status("batch", "muted", "Status: —")
        messagebox.showinfo("Cleared", "All results cleared.")


if __name__ == "__main__":
    app = ISBNApp()
    app.mainloop()
