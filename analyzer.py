from models import Student

class Analyzer:
    def __init__(self, students):
        """
        students: list of Student objects
        """
        self.students = students

    def get_student_averages(self):
        """Return dictionary of student name and average"""
        return {s.name: s.get_average() for s in self.students}

    def calculate_subject_average(self):
        """Calculate average marks for each subject"""
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
        """Return student with highest average"""
        return max(self.students, key=lambda s: s.get_average())

    def find_lowest(self):
        """Return student with lowest average"""
        return min(self.students, key=lambda s: s.get_average())

    def count_pass_fail(self):
        """Return number of pass and fail students"""
        pass_count = sum(1 for s in self.students if s.get_result() == "Pass")
        fail_count = sum(1 for s in self.students if s.get_result() == "Fail")
        return pass_count, fail_count

    def get_grade_distribution(self):
        """Return count of each grade"""
        grade_count = {}

        for student in self.students:
            grade = student.get_grade()
            grade_count[grade] = grade_count.get(grade, 0) + 1

        return grade_count

    def get_full_analysis(self, subject=None):
        """Return complete analysis in dictionary form. If subject is provided, compute stats for that subject."""
        if subject:
            valid_students = [s for s in self.students if subject in s.marks]
            if not valid_students:
                return None
            
            def get_sub_val(s): return s.marks[subject]
            
            top_s = max(valid_students, key=get_sub_val)
            low_s = min(valid_students, key=get_sub_val)
            
            pass_c = sum(1 for s in valid_students if get_sub_val(s) >= 40)
            fail_c = sum(1 for s in valid_students if get_sub_val(s) < 40)
            
            pass_list = [(s.name, get_sub_val(s)) for s in valid_students if get_sub_val(s) >= 40]
            fail_list = [(s.name, get_sub_val(s)) for s in valid_students if get_sub_val(s) < 40]
            
            def get_sub_grade(mark):
                if mark >= 90: return 'A+'
                elif mark >= 80: return 'A'
                elif mark >= 70: return 'B'
                elif mark >= 60: return 'C'
                elif mark >= 50: return 'D'
                elif mark >= 40: return 'E'
                else: return 'F'
                
            grades_dist = {}
            student_scores = {}
            for s in valid_students:
                mark = get_sub_val(s)
                grade = get_sub_grade(mark)
                grades_dist[grade] = grades_dist.get(grade, 0) + 1
                student_scores[s.name] = mark

            return {
                "student_avgs": student_scores,
                "subject_avg": self.calculate_subject_average(),
                "topper": top_s.name,
                "lowest": low_s.name,
                "pass_fail": (pass_c, fail_c),
                "pass_list": pass_list,
                "fail_list": fail_list,
                "grades": {s.name: get_sub_grade(get_sub_val(s)) for s in valid_students},
                "grade_dist": grades_dist
            }

        pass_list = [(s.name, s.get_average()) for s in self.students if s.get_result() == "Pass"]
        fail_list = [(s.name, s.get_average()) for s in self.students if s.get_result() == "Fail"]

        return {
            "student_avgs": self.get_student_averages(),
            "subject_avg": self.calculate_subject_average(),
            "topper": self.find_topper().name if self.students else None,
            "lowest": self.find_lowest().name if self.students else None,
            "pass_fail": self.count_pass_fail(),
            "pass_list": pass_list,
            "fail_list": fail_list,
            "grades": {s.name: s.get_grade() for s in self.students},
            "grade_dist": self.get_grade_distribution()
        }