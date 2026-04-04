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

