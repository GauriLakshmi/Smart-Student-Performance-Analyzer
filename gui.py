import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

# 🎨 COLORS
BG = "#0f172a"
CARD = "#1e293b"
BTN1 = "#22c55e"
BTN2 = "#3b82f6"
BTN3 = "#a855f7"
BTN4 = "#f59e0b"
TEXT = "#e2e8f0"
ACCENT = "#38bdf8"

class StudentAnalyzerApp:
    def __init__(self, root, controller=None):
        self.root = root
        self.controller = controller
        self.root.title("Student Performance Analyzer")
        
        # 📏 WINDOW CONFIG
        self.root.geometry("1100x900")
        self.root.minsize(950, 750)
        self.root.configure(bg=BG)

        # Track dynamic subject rows: list of (subject_entry, marks_entry) tuples
        self.subject_rows = []

        self.setup_ui()

    def setup_ui(self):
        # 🔥 MAIN CONTAINER
        self.main_container = tk.Frame(self.root, bg=BG)
        self.main_container.pack(fill="both", expand=True)

        # 🔥 SCROLLABLE CANVAS
        self.canvas = tk.Canvas(self.main_container, bg=BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        def on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)

        self.canvas.bind("<Configure>", on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 🖱️ Scroll Bind
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # --- CONTENT ---
        self.content_holder = tk.Frame(self.scrollable_frame, bg=BG)
        self.content_holder.pack(pady=20, fill="x", expand=True)

        # 🔥 TITLE
        tk.Label(self.content_holder, text="📊 Smart Student Performance Analyzer", font=("Segoe UI", 26, "bold"), bg=BG, fg=ACCENT).pack(pady=(10, 30))

        # 📥 INPUT SECTION (Dynamic Manual Entry)
        tk.Label(self.content_holder, text="👤 Step 1: Add Student Details", font=("Segoe UI", 16, "bold"), bg=BG, fg=TEXT).pack(pady=5)
        
        self.input_card = tk.Frame(self.content_holder, bg=CARD, padx=30, pady=30, relief="flat")
        self.input_card.pack(pady=10, padx=80, fill="x")

        # 🏷️ NAME ROW - NOW PROPERLY ALIGNED
        name_container = tk.Frame(self.input_card, bg=CARD)
        name_container.pack(fill="x", pady=(0, 20))
        
        tk.Label(name_container, text="Full Name:", bg=CARD, fg=TEXT, font=("Segoe UI", 12, "bold"), width=12, anchor="w").pack(side="left", padx=(5, 10))
        self.entry_name = tk.Entry(name_container, font=("Segoe UI", 12), width=40)
        self.entry_name.pack(side="left", fill="x", expand=True)

        # 📝 SUBJECTS AREA
        self.subjects_container = tk.Frame(self.input_card, bg=CARD)
        self.subjects_container.pack(fill="x")

        # ➕ ADD SUBJECT BUTTON
        self.add_sub_btn = tk.Button(self.input_card, text="➕ Add Subject Entry", bg="#475569", fg="white", 
                                    font=("Segoe UI", 10, "bold"), command=self.add_subject_row, 
                                    padx=10, pady=5, relief="flat", cursor="hand2")
        self.add_sub_btn.pack(pady=15)

        # 🔘 CONTROL BUTTONS
        btn_frame = tk.Frame(self.content_holder, bg=BG)
        btn_frame.pack(pady=30)

        self.styled_btn(btn_frame, "✅ Confirm & Add Student", BTN1, self.on_add_student).grid(row=0, column=0, padx=10)
        self.styled_btn(btn_frame, "📂 Load CSV File", BTN3, self.on_load_csv).grid(row=0, column=1, padx=10)
        self.styled_btn(btn_frame, "📊 View Analysis", BTN2, self.on_analyze).grid(row=0, column=2, padx=10)
        self.styled_btn(btn_frame, "💾 Export Data", BTN4, self.on_export).grid(row=0, column=3, padx=10)

        # 📋 TABLE
        self.setup_table_style()
        tk.Label(self.content_holder, text="📋 Step 2: Student Marks List", font=("Segoe UI", 16, "bold"), bg=BG, fg=TEXT).pack(pady=(20, 5))
        
        self.table_container = tk.Frame(self.content_holder, bg=BG)
        self.table_container.pack(pady=10, padx=50, fill="x")

        self.table = ttk.Treeview(self.table_container, columns=("Name", "Avg"), show="headings", height=8)
        self.update_table_headers()
        self.table.pack(fill="x")

        # 📈 VISUALS
        tk.Label(self.content_holder, text="📈 Step 3: Performance Insights", font=("Segoe UI", 16, "bold"), bg=BG, fg=TEXT).pack(pady=(40, 10))

        graph_btn_frame = tk.Frame(self.content_holder, bg=BG)
        graph_btn_frame.pack(pady=10)

        self.styled_btn(graph_btn_frame, "📊 Subject Avg", "#f59e0b", lambda: self.on_show_graph("subject")).grid(row=0, column=0, padx=10)
        self.styled_btn(graph_btn_frame, "🥧 Pass/Fail", "#ef4444", lambda: self.on_show_graph("pass")).grid(row=0, column=1, padx=10)
        self.styled_btn(graph_btn_frame, "📈 Trend", "#10b981", lambda: self.on_show_graph("trend")).grid(row=0, column=2, padx=10)

        self.graph_display_card = tk.Frame(self.content_holder, bg=CARD, padx=10, pady=10)
        self.graph_display_card.pack(pady=30)
        
        self.graph_label = tk.Label(self.graph_display_card, bg=CARD)
        self.graph_label.pack()

    def add_subject_row(self, sub_name="", sub_mark=""):
        """Adds a new row with Subject Name and Marks entries."""
        row_frame = tk.Frame(self.subjects_container, bg=CARD)
        row_frame.pack(fill="x", pady=5)

        tk.Label(row_frame, text="Subject:", bg=CARD, fg=TEXT, font=("Segoe UI", 12, "bold"), width=12, anchor="w").pack(side="left", padx=(5, 10))
        sub_entry = tk.Entry(row_frame, font=("Segoe UI", 11), width=20)
        sub_entry.insert(0, sub_name)
        sub_entry.pack(side="left", padx=10)

        tk.Label(row_frame, text="Marks:", bg=CARD, fg=TEXT, font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
        mark_entry = tk.Entry(row_frame, font=("Segoe UI", 11), width=10)
        mark_entry.insert(0, str(sub_mark))
        mark_entry.pack(side="left", padx=10)

        # Delete button for row
        def remove_row():
            self.subject_rows.remove((sub_entry, mark_entry))
            row_frame.destroy()

        del_btn = tk.Button(row_frame, text="✕", bg="#ef4444", fg="white", font=("Segoe UI", 8, "bold"), 
                           command=remove_row, relief="flat", cursor="hand2", padx=5)
        del_btn.pack(side="left", padx=10)

        self.subject_rows.append((sub_entry, mark_entry))

    def setup_table_style(self):
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", background=CARD, foreground="white", rowheight=35, fieldbackground=CARD, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", background="#2d3748", foreground="white", font=("Segoe UI", 11, "bold"))
        self.style.map("Treeview", background=[("selected", ACCENT)])

    def update_table_headers(self):
        subjects = self.controller.subjects if self.controller else []
        self.table_columns = ("Name",) + tuple(subjects) + ("Avg",)
        self.table["columns"] = self.table_columns
        for col in self.table_columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=120, anchor="center")

    def styled_btn(self, parent, text, color, cmd):
        return tk.Button(parent, text=text, command=cmd, bg=color, fg="white", 
                        font=("Segoe UI", 11, "bold"), padx=25, pady=10, 
                        relief="flat", cursor="hand2")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_add_student(self):
        name = self.entry_name.get()
        if not name:
            messagebox.showwarning("Warning", "Student name is required")
            return
        
        marks = {}
        new_subjects = []
        try:
            for sub_ent, mark_ent in self.subject_rows:
                sub = sub_ent.get().strip()
                mark = mark_ent.get().strip()
                if sub and mark:
                    marks[sub] = int(mark)
                    if sub not in self.controller.subjects:
                        new_subjects.append(sub)
        except ValueError:
            messagebox.showerror("Error", "Marks must be numbers")
            return

        if not marks:
            messagebox.showwarning("Warning", "Add at least one subject and marks")
            return

        # Update controller subjects if new ones were added manually
        if new_subjects:
            self.controller.subjects.extend([s for s in new_subjects if s not in self.controller.subjects])
            self.update_table_headers()

        s = self.controller.add_manual_student(name, marks)
        
        # Refresh table rows to account for possibly new columns
        self.refresh_table()
        
        # Clear entries
        self.entry_name.delete(0, tk.END)
        for _, m_ent in self.subject_rows: m_ent.delete(0, tk.END)

    def refresh_table(self):
        for item in self.table.get_children(): self.table.delete(item)
        for s in self.controller.students:
            row = [s.name] + [s.marks.get(sub, 0) for sub in self.controller.subjects] + [round(s.average, 2)]
            self.table.insert("", "end", values=row)

    def on_load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not path: return

        success, msg = self.controller.process_csv(path)
        if not success:
            messagebox.showerror("Error", msg)
            return

        # Clear existing dynamic rows and populate with CSV subjects
        for child in self.subjects_container.winfo_children(): child.destroy()
        self.subject_rows.clear()
        for sub in self.controller.subjects:
            self.add_subject_row(sub_name=sub)

        self.update_table_headers()
        self.refresh_table()
        messagebox.showinfo("Success", msg)

    def on_analyze(self):
        res = self.controller.get_analysis_results()
        if not res: return messagebox.showwarning("Warning", "No data")

        msg = f"🏆 TOPPER: {res['topper'].upper()}\n📉 LOWEST: {res['lowest'].upper()}\n\n✅ PASSED: {res['pass_fail'][0]}\n❌ FAILED: {res['pass_fail'][1]}"
        messagebox.showinfo("Analysis Summary", msg)

    def on_export(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path: return
        if self.controller.export_data(path): messagebox.showinfo("Done", "Exported successfully")

    def on_show_graph(self, g_type):
        filename = self.controller.generate_graph(g_type)
        if filename:
            img = Image.open(filename).resize((800, 450))
            img_tk = ImageTk.PhotoImage(img)
            self.graph_label.config(image=img_tk)
            self.graph_label.image = img_tk
        else:
            messagebox.showwarning("No Data", "Add students first")