from models import Student
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