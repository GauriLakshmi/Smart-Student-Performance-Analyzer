# graphs.py

import matplotlib.pyplot as plt


# 📊 Bar Chart → Subject Averages
def plot_subject_avg(subject_avg):
    subjects = list(subject_avg.keys())
    averages = list(subject_avg.values())

    plt.figure()
    plt.bar(subjects, averages, color='skyblue')
    plt.xlabel("Subjects")
    plt.ylabel("Average Marks")
    plt.title("Subject-wise Average")
    plt.savefig("subject_avg.png")
    plt.close()


# 🥧 Pie Chart → Pass vs Fail
def plot_pass_fail(pass_count, fail_count):
    labels = ["Pass", "Fail"]
    values = [pass_count, fail_count]

    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['green', 'red'])
    plt.title("Pass vs Fail Distribution")
    plt.savefig("pass_fail.png")
    plt.close()


# 📈 Line Graph → Student Performance
def plot_student_trend(student_avgs):
    names = list(student_avgs.keys())
    avgs = list(student_avgs.values())

    plt.figure()
    plt.plot(names, avgs, marker='o')
    plt.xlabel("Students")
    plt.ylabel("Average Marks")
    plt.title("Student Performance Trend")
    plt.xticks(rotation=30)
    plt.savefig("student_trend.png")
    plt.close()


# 🎓 Pie Chart → Grade Distribution (🔥 extra feature)
def plot_grade_distribution(grade_dist):
    labels = list(grade_dist.keys())
    values = list(grade_dist.values())

    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Grade Distribution")
    plt.savefig("grade_distribution.png")
    plt.close()