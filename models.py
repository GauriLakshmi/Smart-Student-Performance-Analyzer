class Student:
    def __init__(self, name, marks):
        """
        name: string
        marks: dictionary {subject: marks}
        """
        self.name = name
        self.marks = marks

    def get_average(self):
        """Calculate and return average marks"""
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)

    def get_result(self):
        """Return Pass or Fail based on average"""
        return "Pass" if self.get_average() >= 40 else "Fail"

    def get_grade(self):
        """Return grade based on average"""
        avg = self.get_average()

        if avg >= 90:
            return 'S'
        elif avg >= 85:
            return 'A+'
        elif avg >= 80:
            return 'A'
        elif avg >= 70:
            return 'B'
        elif avg >= 60:
            return 'C'
        elif avg >= 50:
            return 'D'
        elif avg >= 40:
            return 'E'
        else:
            return 'F'

    def to_dict(self):
        """Optional: Convert student data to dictionary (useful for CSV/JSON)"""
        return {
            "name": self.name,
            "marks": self.marks,
            "average": self.get_average(),
            "result": self.get_result(),
            "grade": self.get_grade()
        }