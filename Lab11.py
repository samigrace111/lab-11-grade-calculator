# Lab 11 Grade Calculator

import os
import matplotlib.pyplot as plt

def load_students(filepath):
    """
    Returns a dict mapping student name -> student ID.
    Each line in students.txt is: <3‑digit ID><student name>
    """
    students = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sid = line[:3]
            name = line[3:]
            students[name] = sid
    return students

def load_assignments(filepath):
    """
    Returns a dict mapping assignment ID -> {'name': name, 'points': pts}.
    assignments.txt is 3 lines per assignment: name, ID, points.
    """
    assignments = {}
    with open(filepath, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]
    for i in range(0, len(lines), 3):
        name = lines[i]
        aid = lines[i+1]
        pts = int(lines[i+2])
        assignments[aid] = {'name': name, 'points': pts}
    return assignments

def load_submissions(dirpath):
    """
    Returns a dict mapping student ID -> list of (assignmentID, percent).
    Each file is one submission: studentID|assignmentID|percent.
    """
    submissions = {}
    for fname in os.listdir(dirpath):
        if fname.startswith('.'):
            continue
        with open(os.path.join(dirpath, fname), 'r') as f:
            line = f.read().strip()
            if not line:
                continue
            stu_id, aid, perc = line.split('|')
            submissions.setdefault(stu_id, []).append((aid, float(perc)))
    return submissions

def student_grade(name, students, assignments, submissions):
    sid = students.get(name)
    if sid is None or sid not in submissions:
        print("Student not found")
        return

    total_points = sum(info['points'] for info in assignments.values())
    earned = 0
    for aid, perc in submissions[sid]:
        pts = assignments[aid]['points']
        earned += (perc / 100.0) * pts

    grade_pct = round(earned / total_points * 100)
    print(f"{grade_pct}%")

def assignment_stats(name, assignments, submissions):
    aid = None
    for id_, info in assignments.items():
        if info['name'] == name:
            aid = id_
            break
    if aid is None:
        print("Assignment not found")
        return

    scores = []
    for subs in submissions.values():
        for sid, perc in subs:
            if sid == aid:
                scores.append(perc)

    if not scores:
        print("Assignment not found")
        return

    mn = int(min(scores))
    mx = int(max(scores))
    avg = int(sum(scores) / len(scores))   # truncated to match example

    print(f"Min: {mn}%")
    print(f"Avg: {avg}%")
    print(f"Max: {mx}%")

def assignment_graph(name, assignments, submissions):

    aid = None
    for id_, info in assignments.items():
        if info['name'] == name:
            aid = id_
            break
    if aid is None:
        print("Assignment not found")
        return

    scores = []
    for subs in submissions.values():
        for sid, perc in subs:
            if sid == aid:
                scores.append(perc)

    if not scores:
        print("Assignment not found")
        return


    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(name)
    plt.xlabel("Percentage")
    plt.ylabel("Number of Students")
    plt.show()

def main():
    data_dir = 'data'
    students = load_students(os.path.join(data_dir, 'students.txt'))
    assignments = load_assignments(os.path.join(data_dir, 'assignments.txt'))
    submissions = load_submissions(os.path.join(data_dir, 'submissions'))


    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    choice = input("Enter your selection: ")

    if choice == '1':
        name = input("What is the student's name: ")
        student_grade(name, students, assignments, submissions)
    elif choice == '2':
        name = input("What is the assignment name: ")
        assignment_stats(name, assignments, submissions)
    elif choice == '3':
        name = input("What is the assignment name: ")
        assignment_graph(name, assignments, submissions)
    else:

        pass

if __name__ == '__main__':
    main()
