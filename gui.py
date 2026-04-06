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

        # 📱 LEFT SIDEBAR (Data Input)
        self.sidebar = tk.Frame(self.main_container, bg="#0b1121", width=320)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        tk.Label(self.sidebar, text="Control Center", font=("Segoe UI", 18, "bold"), bg="#0b1121", fg=ACCENT).pack(pady=(30, 20))
        
        # Add Student Mode
        self.input_card = tk.Frame(self.sidebar, bg=CARD, padx=15, pady=15, relief="flat")
        self.input_card.pack(pady=10, padx=15, fill="x")
        
        tk.Label(self.input_card, text="👤 Add Manual Entry", bg=CARD, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,10))
        
        name_container = tk.Frame(self.input_card, bg=CARD)
        name_container.pack(fill="x")
        tk.Label(name_container, text="Name:", bg=CARD, fg=TEXT, font=("Segoe UI", 10)).pack(side="left")
        self.entry_name = tk.Entry(name_container, font=("Segoe UI", 10), width=15)
        self.entry_name.pack(side="left", fill="x", expand=True, padx=(10, 0))

        self.subjects_container = tk.Frame(self.input_card, bg=CARD)
        self.subjects_container.pack(fill="x", pady=10)

        self.add_sub_btn = tk.Button(self.input_card, text="➕ Add Subject Row", bg="#475569", fg="white", 
                                    font=("Segoe UI", 9, "bold"), command=self.add_subject_row, 
                                    padx=5, pady=5, relief="flat", cursor="hand2")
        self.add_sub_btn.pack(pady=(0, 10))

        self.styled_btn(self.input_card, "✅ Add Student", BTN1, self.on_add_student).pack(fill="x")

        # File Modes
        tk.Frame(self.sidebar, bg="#475569", height=1).pack(fill="x", padx=20, pady=20)
        tk.Label(self.sidebar, text="📁 File Operations", bg="#0b1121", fg=TEXT, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20)
        
        self.styled_btn(self.sidebar, "📂 Load CSV File", BTN3, self.on_load_csv).pack(fill="x", padx=20, pady=10)
        self.styled_btn(self.sidebar, "💾 Export Data", BTN4, self.on_export).pack(fill="x", padx=20, pady=10)

        # 🖥️ RIGHT DASHBOARD (Analytics)
        self.dashboard_frame = tk.Frame(self.main_container, bg=BG)
        self.dashboard_frame.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(self.dashboard_frame, bg=BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.dashboard_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        def on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.bind("<Configure>", on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.content_holder = tk.Frame(self.scrollable_frame, bg=BG, padx=40, pady=30)
        self.content_holder.pack(fill="both", expand=True)
        
        tk.Label(self.content_holder, text="📊 Live Analytics Dashboard", font=("Segoe UI", 22, "bold"), bg=BG, fg="white").pack(anchor="w", pady=(0, 20))

        # --- STAT CARDS ---
        self.stats_frame = tk.Frame(self.content_holder, bg=BG)
        self.stats_frame.pack(fill="x", pady=(0, 20))
        
        self.stat_students = self.create_stat_card("Total Students", "0", BTN2)
        self.stat_passrate = self.create_stat_card("Pass Rate", "0%", BTN1)
        self.stat_topper = self.create_stat_card("Top Performer", "N/A", BTN4)

        # --- TABLE ---
        self.setup_table_style()
        tk.Label(self.content_holder, text="📋 Student Records", font=("Segoe UI", 14, "bold"), bg=BG, fg=TEXT).pack(anchor="w", pady=(20, 5))
        
        self.table_container = tk.Frame(self.content_holder, bg=BG)
        self.table_container.pack(fill="x")

        self.table = ttk.Treeview(self.table_container, columns=("Name", "Avg"), show="headings", height=8)
        self.update_table_headers()
        self.table.pack(fill="x")

        # --- GRAPHS & FILTERS ---
        tk.Label(self.content_holder, text="📈 Performance Visualizations", font=("Segoe UI", 14, "bold"), bg=BG, fg=TEXT).pack(anchor="w", pady=(40, 10))

        filter_frame = tk.Frame(self.content_holder, bg=BG)
        filter_frame.pack(fill="x", pady=5)
        
        tk.Label(filter_frame, text="Analyze Subject:", bg=BG, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(side="left")
        self.subject_var = tk.StringVar(value="Overall")
        self.subject_dropdown = ttk.Combobox(filter_frame, textvariable=self.subject_var, state="readonly", font=("Segoe UI", 10), width=15)
        self.subject_dropdown.pack(side="left", padx=10)
        self.subject_dropdown["values"] = ["Overall"]
        
        graph_btn_frame = tk.Frame(filter_frame, bg=BG)
        graph_btn_frame.pack(side="left", padx=20)
        
        self.styled_btn(graph_btn_frame, "📊 Subject Avg", "#f59e0b", lambda: self.on_show_graph("subject")).grid(row=0, column=0, padx=5)
        self.styled_btn(graph_btn_frame, "🥧 Pass/Fail", "#ef4444", lambda: self.on_show_graph("pass")).grid(row=0, column=1, padx=5)
        self.styled_btn(graph_btn_frame, "📈 Trend", "#10b981", lambda: self.on_show_graph("trend")).grid(row=0, column=2, padx=5)
        self.styled_btn(graph_btn_frame, "🎓 Grade Dist", "#8b5cf6", lambda: self.on_show_graph("grade_dist")).grid(row=0, column=3, padx=5)

        self.graph_display_card = tk.Frame(self.content_holder, bg=CARD, padx=10, pady=10)
        self.graph_display_card.pack(fill="x", pady=20)
        
        self.graph_label = tk.Label(self.graph_display_card, bg=CARD)
        self.graph_label.pack()

        self.list_frame = tk.Frame(self.graph_display_card, bg=CARD)
        self.list_frame.pack(fill="x", pady=(10, 5))
        
        tk.Label(self.list_frame, text="List of students:", bg=CARD, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.list_var = tk.StringVar(value="Select...")
        self.list_dropdown = ttk.Combobox(self.list_frame, textvariable=self.list_var, values=["Select...", "Pass", "Fail"], state="readonly", font=("Segoe UI", 10), width=10)
        self.list_dropdown.pack(side="left", padx=5)
        self.list_dropdown.bind("<<ComboboxSelected>>", self.on_list_filter_change)

        self.graph_info_text = tk.Text(self.graph_display_card, bg="#1e293b", fg=TEXT, font=("Segoe UI", 11), height=6, wrap="word", relief="flat")

    def create_stat_card(self, title, init_val, bg_color):
        card = tk.Frame(self.stats_frame, bg=bg_color, padx=20, pady=15)
        card.pack(side="left", padx=(0, 20), expand=True, fill="both")
        
        tk.Label(card, text=title, bg=bg_color, fg="#e2e8f0", font=("Segoe UI", 11)).pack(anchor="w")
        val_label = tk.Label(card, text=init_val, bg=bg_color, fg="white", font=("Segoe UI", 20, "bold"))
        val_label.pack(anchor="w", pady=(5, 0))
        return val_label

    def update_stats_dashboard(self):
        res = self.controller.get_analysis_results()
        if not res:
            self.stat_students.config(text="0")
            self.stat_passrate.config(text="0%")
            self.stat_topper.config(text="N/A")
            return
            
        total = len(self.controller.students)
        passes = res["pass_fail"][0]
        pass_rate = (passes / total) * 100 if total > 0 else 0
        topper = res["topper"]
        
        self.stat_students.config(text=str(total))
        self.stat_passrate.config(text=f"{pass_rate:.1f}%")
        self.stat_topper.config(text=topper.upper() if topper else "N/A")

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
        self.table_columns = ("Name",) + tuple(subjects) + ("Avg", "Grade", "Status")
        self.table["columns"] = self.table_columns
        for col in self.table_columns:
            self.table.heading(col, text=col)
            width = 120 if col == "Name" else 80
            self.table.column(col, width=width, anchor="center")
            
        if hasattr(self, 'subject_dropdown'):
            self.subject_dropdown["values"] = ["Overall"] + subjects
            if self.subject_var.get() not in ["Overall"] + subjects:
                self.subject_var.set("Overall")

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
            row = [s.name] + [s.marks.get(sub, 0) for sub in self.controller.subjects] + [
                round(s.get_average(), 2), s.get_grade(), s.get_result()
            ]
            self.table.insert("", "end", values=row)
        
        self.update_stats_dashboard()

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
        subj = self.subject_var.get()
        subject_param = None if subj == "Overall" else subj
        
        res = self.controller.get_analysis_results(subject_param)
        if not res: return messagebox.showwarning("Warning", "No data")

        title = f"Analysis Summary - {subj}"
        msg = f"🏆 TOPPER: {res['topper'].upper()}\n📉 LOWEST: {res['lowest'].upper()}\n\n✅ PASSED: {res['pass_fail'][0]}\n❌ FAILED: {res['pass_fail'][1]}"
        messagebox.showinfo(title, msg)

    def on_export(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path: return
        if self.controller.export_data(path): messagebox.showinfo("Done", "Exported successfully")

    def on_list_filter_change(self, event=None):
        selection = self.list_var.get()
        if selection == "Select...":
            self.graph_info_text.pack_forget()
            return
            
        subj = self.subject_var.get()
        subject_param = None if subj == "Overall" else subj
        res = self.controller.get_analysis_results(subject_param)
        
        if not res:
            return messagebox.showwarning("Warning", "No data available")

        self.graph_info_text.pack(fill="x", pady=(5, 0))
        self.graph_info_text.config(state="normal")
        self.graph_info_text.delete(1.0, tk.END)
        
        if selection == "Pass":
            st_list = res.get("pass_list", [])
            icon = "✅ PASSED"
        else:
            st_list = res.get("fail_list", [])
            icon = "❌ FAILED"
            
        if not st_list:
            display_text = f"{icon} STUDENTS:\nNone"
        else:
            lines = [f"• {name} (Marks: {round(mark, 2)})" for name, mark in st_list]
            display_text = f"{icon} STUDENTS:\n" + "\n".join(lines)
            
        self.graph_info_text.insert(tk.END, display_text)
        self.graph_info_text.config(state="disabled")

    def on_show_graph(self, g_type):
        subj = self.subject_var.get()
        subject_param = None if subj == "Overall" else subj
        
        if g_type == "subject" and subject_param is not None:
             messagebox.showinfo("Info", "Subject Avg graph shows all subjects. Switching back to Overall view.")
             self.subject_var.set("Overall")
             subject_param = None
             
        filename = self.controller.generate_graph(g_type, subject_param)
        if filename:
            img = Image.open(filename).resize((800, 450))
            img_tk = ImageTk.PhotoImage(img)
            self.graph_label.config(image=img_tk)
            self.graph_label.image = img_tk
            
            # Refresh list if currently displayed
            if self.list_var.get() != "Select...":
                self.on_list_filter_change()
        else:
            messagebox.showwarning("No Data", "Add students first")