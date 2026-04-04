import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from PIL import Image, ImageTk

from models import Student, Analyzer
from graphs import plot_subject_avg, plot_pass_fail, plot_student_trend

# 🎨 COLORS
BG = "#0f172a"
CARD = "#1e293b"
BTN1 = "#22c55e"
BTN2 = "#3b82f6"
BTN3 = "#a855f7"
TEXT = "#e2e8f0"
ACCENT = "#38bdf8"

students = []

# ➕ Add student
def add_student():
    name = entry_name.get()
    try:
        math = int(entry_math.get())
        cs = int(entry_cs.get())
        physics = int(entry_physics.get())
    except:
        messagebox.showerror("Error", "Invalid marks")
        return

    s = Student(name, {"Math": math, "CS": cs, "Physics": physics})
    students.append(s)

    table.insert("", "end", values=(name, math, cs, physics, round(s.average, 2)))

# 📂 Load CSV
def load_csv():
    file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file:
        return

    df = pd.read_csv(file)

    for _, row in df.iterrows():
        s = Student(row["Name"], {
            "Math": row["Math"],
            "CS": row["CS"],
            "Physics": row["Physics"]
        })
        students.append(s)

        table.insert("", "end", values=(
            row["Name"], row["Math"], row["CS"], row["Physics"], round(s.average, 2)
        ))

# 📊 Analyze
def analyze():
    if not students:
        return

    analyzer = Analyzer(students)
    results = analyzer.get_full_analysis()

    topper = results["topper"]
    p, f = results["pass_fail"]

    messagebox.showinfo("Analysis", f"Topper: {topper}\nPass: {p}\nFail: {f}")

# 📈 Show Graph
def show_graph(graph_type):
    if not students:
        return

    analyzer = Analyzer(students)
    results = analyzer.get_full_analysis()

    if graph_type == "subject":
        plot_subject_avg(results["subject_avg"])
        file = "subject_avg.png"

    elif graph_type == "pass":
        plot_pass_fail(*results["pass_fail"])
        file = "pass_fail.png"

    elif graph_type == "trend":
        plot_student_trend(results["student_avgs"])
        file = "student_trend.png"

    img = Image.open(file).resize((520, 300))
    img_tk = ImageTk.PhotoImage(img)

    graph_label.config(image=img_tk)
    graph_label.image = img_tk


# 🖥️ ROOT
root = tk.Tk()
root.title("Student Analyzer Dashboard")
root.geometry("950x700")
root.configure(bg=BG)

# 🔥 SCROLLABLE PAGE
canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg=BG)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 🖱️ Smooth scroll
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# 🔥 TITLE
tk.Label(
    scrollable_frame,
    text="📊 Student Performance Dashboard",
    font=("Segoe UI", 20, "bold"),
    bg=BG,
    fg=ACCENT
).pack(pady=15)

# 📥 INPUT CARD
input_frame = tk.Frame(scrollable_frame, bg=CARD, padx=15, pady=15)
input_frame.pack(pady=10)

tk.Label(input_frame, text="👤 Name", bg=CARD, fg=TEXT).grid(row=0, column=0, padx=5, pady=5)
tk.Label(input_frame, text="📘 Math", bg=CARD, fg=TEXT).grid(row=1, column=0, padx=5, pady=5)
tk.Label(input_frame, text="💻 CS", bg=CARD, fg=TEXT).grid(row=2, column=0, padx=5, pady=5)
tk.Label(input_frame, text="🔬 Physics", bg=CARD, fg=TEXT).grid(row=3, column=0, padx=5, pady=5)

entry_name = tk.Entry(input_frame)
entry_name.grid(row=0, column=1, padx=5, pady=5)

entry_math = tk.Entry(input_frame)
entry_math.grid(row=1, column=1, padx=5, pady=5)

entry_cs = tk.Entry(input_frame)
entry_cs.grid(row=2, column=1, padx=5, pady=5)

entry_physics = tk.Entry(input_frame)
entry_physics.grid(row=3, column=1, padx=5, pady=5)

# 🔘 BUTTON ROW
btn_frame = tk.Frame(scrollable_frame, bg=BG)
btn_frame.pack(pady=15)

def styled_btn(parent, text, color, cmd):
    return tk.Button(
        parent,
        text=text,
        command=cmd,
        bg=color,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=10,
        pady=5,
        relief="flat",
        cursor="hand2"
    )

styled_btn(btn_frame, "➕ Add Student", BTN1, add_student).grid(row=0, column=0, padx=10)
styled_btn(btn_frame, "📂 Load CSV", BTN3, load_csv).grid(row=0, column=1, padx=10)
styled_btn(btn_frame, "📊 Analyze", BTN2, analyze).grid(row=0, column=2, padx=10)

# 📋 TABLE
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
    background=CARD,
    foreground="white",
    rowheight=28,
    fieldbackground=CARD
)

style.map("Treeview", background=[("selected", ACCENT)])

columns = ("Name", "Math", "CS", "Physics", "Avg")
table = ttk.Treeview(scrollable_frame, columns=columns, show="headings", height=6)

for col in columns:
    table.heading(col, text=col)

table.pack(pady=15)

# 📊 GRAPH TITLE
tk.Label(
    scrollable_frame,
    text="📈 Visual Insights",
    font=("Segoe UI", 14, "bold"),
    bg=BG,
    fg=TEXT
).pack(pady=10)

# 📈 GRAPH BUTTONS
graph_frame = tk.Frame(scrollable_frame, bg=BG)
graph_frame.pack(pady=10)

styled_btn(graph_frame, "📊 Subject Avg", "#f59e0b", lambda: show_graph("subject")).grid(row=0, column=0, padx=5)
styled_btn(graph_frame, "🥧 Pass/Fail", "#ef4444", lambda: show_graph("pass")).grid(row=0, column=1, padx=5)
styled_btn(graph_frame, "📈 Trend", "#10b981", lambda: show_graph("trend")).grid(row=0, column=2, padx=5)

# 🖼️ GRAPH DISPLAY
graph_label = tk.Label(scrollable_frame, bg=CARD, bd=2, relief="ridge")
graph_label.pack(pady=20)

root.mainloop()