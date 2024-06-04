# school class

class School:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.priority = None
        self.students = []

    def setPriority(self, priority):
        self.priority = priority

    def add_student(self, student):
        self.students.append(student)

    def __str__(self):
        return f"{self.name}, {self.capacity}, {self.students}"

    def __repr__(self):
        return f"{self.name}, {self.capacity}, {self.students}"

