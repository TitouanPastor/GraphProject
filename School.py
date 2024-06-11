# school class

class School:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.priority = None
        self.preferenceList = []

    def setPriority(self, priority):
        self.priority = priority

    def add_student(self, student):
        self.preferenceList.append(student)

    def __str__(self):
        return (f"{self.name}")

    def __repr__(self):
        return (f"{self.name}")
