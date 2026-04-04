class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        self.average = self.calculate_average()

    def calculate_average(self):
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)

    def get_result(self):
        return "Pass" if self.average >= 40 else "Fail"


class Analyzer:
    def __init__(self, students):
        self.students = students

    def get_student_averages(self):
        return {s.name: s.average for s in self.students}

    def calculate_subject_average(self):
        subject_totals = {}
        subject_counts = {}

        for student in self.students:
            for subject, mark in student.marks.items():
                subject_totals[subject] = subject_totals.get(subject, 0) + mark
                subject_counts[subject] = subject_counts.get(subject, 0) + 1

        return {
            sub: subject_totals[sub] / subject_counts[sub]
            for sub in subject_totals
        }

    def find_topper(self):
        return max(self.students, key=lambda s: s.average)

    def count_pass_fail(self):
        pass_count = sum(1 for s in self.students if s.get_result() == "Pass")
        fail_count = sum(1 for s in self.students if s.get_result() == "Fail")
        return pass_count, fail_count

    def get_full_analysis(self):
        return {
            "student_avgs": self.get_student_averages(),
            "subject_avg": self.calculate_subject_average(),
            "topper": self.find_topper().name,
            "pass_fail": self.count_pass_fail()
        }