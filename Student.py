# student class

class Student:
    def __init__(self, name):
        self.priority = None
        self.name = name
        self.schools = []

    def setPriority(self, priority):
        self.priority = priority

    def add_school(self, school):
        self.schools.append(school)

    def __str__(self):
        return self.name + " " + str(self.schools)

    def __repr__(self):
        return self.name + " " + str(self.schools)

