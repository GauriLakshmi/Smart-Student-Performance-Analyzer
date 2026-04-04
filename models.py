# models.py

class Student:
    def __init__(self, name, marks):
        """
        name: string
        marks: dictionary → {"Math": 70, "CS": 80}
        """
        self.name = name
        self.marks = marks
        self.average = self.calculate_average()

    def calculate_average(self):
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)

    def get_result(self):
        return "Pass" if self.average >= 40 else "Fail"

    def get_performance_level(self):
        if self.average < 40:
            return "High Risk"
        elif self.average < 60:
            return "Moderate"
        else:
            return "Safe"

    def get_grade(self):
        avg = self.average

        if avg >= 90:
            return "S"
        elif avg >= 85:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 75:
            return "B+"
        elif avg >= 70:
            return "B"
        elif avg >= 65:
            return "C+"
        elif avg >= 60:
            return "C"
        elif avg >= 55:
            return "D+"
        elif avg >= 40:
            return "D"
        else:
            return "Fail"


# 🔍 Analyzer Class
class Analyzer:
    def __init__(self, students):
        """
        students: list of Student objects
        """
        self.students = students

    def get_student_averages(self):
        return {student.name: student.average for student in self.students}

    def calculate_subject_average(self):
        subject_totals = {}
        subject_counts = {}

        for student in self.students:
            for subject, mark in student.marks.items():
                subject_totals[subject] = subject_totals.get(subject, 0) + mark
                subject_counts[subject] = subject_counts.get(subject, 0) + 1

        subject_avg = {
            subject: subject_totals[subject] / subject_counts[subject]
            for subject in subject_totals
        }

        return subject_avg

    def find_topper(self):
        return max(self.students, key=lambda s: s.average)

    def find_lowest(self):
        return min(self.students, key=lambda s: s.average)

    def count_pass_fail(self):
        pass_count = sum(1 for s in self.students if s.get_result() == "Pass")
        fail_count = sum(1 for s in self.students if s.get_result() == "Fail")
        return pass_count, fail_count

    def get_grade_distribution(self):
        grade_count = {}

        for student in self.students:
            grade = student.get_grade()
            grade_count[grade] = grade_count.get(grade, 0) + 1

        return grade_count

    def get_full_analysis(self):
        return {
            "student_avgs": self.get_student_averages(),
            "subject_avg": self.calculate_subject_average(),
            "topper": self.find_topper().name,
            "lowest": self.find_lowest().name,
            "pass_fail": self.count_pass_fail(),
            "grades": {s.name: s.get_grade() for s in self.students},
            "grade_dist": self.get_grade_distribution()
        }