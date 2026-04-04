import pandas as pd
import os
from models import Student
from analyzer import Analyzer
from graphs import plot_subject_avg, plot_pass_fail, plot_student_trend

class StudentController:
    def __init__(self):
        self.students = []
        self.subjects = [] # Starts empty, user defines subjects manually or via CSV

    def process_csv(self, file_path):
        """Processes CSV and updates the student list and subject list."""
        try:
            df = pd.read_csv(file_path)
            if "Name" not in df.columns:
                return False, "CSV must contain a 'Name' column"

            # Identify subjects (Numeric columns excluding Roll No, ID, etc)
            excluded = ["Roll No", "id", "Name", "ID", "Roll Number"]
            new_subjects = [col for col in df.columns if col not in excluded]
            
            if not new_subjects:
                return False, "No subject columns found in CSV"

            self.subjects = new_subjects
            self.students.clear()

            for _, row in df.iterrows():
                marks = {sub: row[sub] for sub in self.subjects}
                s = Student(row["Name"], marks)
                self.students.append(s)

            return True, f"Loaded {len(self.students)} students"
        except Exception as e:
            return False, str(e)

    def add_manual_student(self, name, marks):
        """Adds a single student manually."""
        s = Student(name, marks)
        self.students.append(s)
        return s

    def get_analysis_results(self):
        """Runs the full analysis on current students."""
        if not self.students:
            return None
        analyzer = Analyzer(self.students)
        return analyzer.get_full_analysis()

    def generate_graph(self, g_type):
        """Generates a graph and returns the filename."""
        res = self.get_analysis_results()
        if not res:
            return None

        filename = ""
        if g_type == "subject":
            plot_subject_avg(res["subject_avg"])
            filename = "subject_avg.png"
        elif g_type == "pass":
            plot_pass_fail(*res["pass_fail"])
            filename = "pass_fail.png"
        elif g_type == "trend":
            plot_student_trend(res["student_avgs"])
            filename = "student_trend.png"
        
        return filename if filename and os.path.exists(filename) else None

    def export_data(self, save_path):
        """Exports student data and analysis summary to a CSV."""
        if not self.students:
            return False

        res = self.get_analysis_results()
        
        # Prepare export list
        export_data = []
        for s in self.students:
            row = {"Name": s.name}
            row.update(s.marks)
            row["Average"] = round(s.average, 2)
            row["Grade"] = s.get_grade()
            export_data.append(row)

        df = pd.DataFrame(export_data)
        df.to_csv(save_path, index=False)
        
        # Append summary
        with open(save_path, 'a') as f:
            f.write(f"\nAnalysis Summary\n")
            f.write(f"Topper,{res['topper']}\n")
            f.write(f"Pass,{res['pass_fail'][0]}\n")
            f.write(f"Fail,{res['pass_fail'][1]}\n")
        
        return True

if __name__ == "__main__":
    from gui import StudentAnalyzerApp
    import tkinter as tk

    root = tk.Tk()
    controller = StudentController()
    app = StudentAnalyzerApp(root, controller)
    root.mainloop()
