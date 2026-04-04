# 📊 Smart Student Performance Analyzer

**Smart Student Performance Analyzer** is a powerful Python-based desktop application designed to evaluate and visualize student academic performance. Whether you use manual data entry or bulk-upload CSV files, this tool provides instant insights through data analysis, grade distribution, and interactive graphs.

## 🚀 Features

- **📂 Dynamic CSV Upload**: Smartly identifies subject columns from any dataset (Science, History, English, Maths, etc.) without needing a fixed structure.
- **👤 Dynamic Manual Entry**: Add students one-by-one with a custom "Subject & Marks" interface—no more boring default subjects!
- **📊 Interactive Visualizations**:
  - **Subject-wise Average**: Bar charts for performance comparison.
  - **Pass/Fail Distribution**: Pie charts to see class results.
  - **Performance Trends**: Line graphs to track student excellence.
- **✅ Detailed Analysis**: Instant pop-up summaries showing the **Topper**, **Lowest Performer**, and total **Pass/Fail counts**.
- **💾 Export to CSV**: Save your structured data and analysis reports for record-keeping.
- **🎨 Premium Dark UI**: A modern, responsive dashboard built with Tkinter for a sleek user experience.

---

## 🛠️ Tech Stack

- **Lanuage**: Python 3.x
- **GUI**: Tkinter (Standard Library)
- **Data Management**: Pandas
- **Visualization**: Matplotlib
- **Image Handling**: Pillow (PIL)

---

## 📦 Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```powershell
   git clone https://github.com/GauriLakshmi/Smart-Student-Performance-Analyzer.git
   cd Smart-Student-Performance-Analyzer
   ```

2. **(Optional) Set up a Virtual Environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

---

## 🖥️ Usage

1. **Start the Application**:
   ```powershell
   python main.py
   ```

2. **Adding Students**:
   - **Manual**: Type a name, click `➕ Add Subject Entry` to define your subjects (e.g., "History", 85).
   - **CSV**: Click `📂 Load CSV File` to upload your own list. 
   > *Note: Your CSV only needs a "Name" column; all other numeric columns will be detected as subjects automatically.*

3. **Analyze**:
   - Click `📊 View Analysis` for a quick summary.
   - Click `📊 Subject Avg`, `🥧 Pass/Fail`, or `📈 Trend` to see visual data.

4. **Export**:
   - Click `💾 Export Data` to save a finished report.

---

## 📁 Project Structure

```text
├── main.py         # Entry point (Controller)
├── gui.py          # Dashboard Interface (View)
├── analyzer.py     # Data Analysis Logic (Model)
├── models.py       # Student Class Definitions
├── graphs.py       # Matplotlib Visualizations
└── requirements.txt # Project Dependencies
```

## 🤝 Contributing

Feel free to fork this project, report issues, or suggest new features via pull requests!

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
