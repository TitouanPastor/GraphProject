# file responsible of parsing the xlsx input file

import pandas as pd
from Student import *
from School import *


def parse_xlsx(df, debugging):

    # create all students (starting at cell 2 of line 0)
    studentList = []
    header = df.columns.values.tolist()
    i = 2
    while i < len(header):
        # Create a student
        studentList.append(Student(header[i]))
        i += 2
    # print("Students:" + str(studentList) + "\n\n")

    # for each line in the xlsx file create a school
    schoolList = []
    for index, row in df.iterrows():
        # Create a school
        school = School(row.get("Schools"), row.get("Capacity"))

        # Create a list of students for a school
        i = 2
        studentIndex = 0
        while i < len(row):
            studentList[studentIndex].setPriority(row.iloc[i])
            school.add_student(studentList[studentIndex])
            studentIndex += 1
            i += 2
        # sort the students by priority inside the school
        school.preferenceList.sort(key=lambda x: x.priority)
        schoolList.append(school)
        if debugging:
            print("adding school: " + str(school))
            print("--------------------------------")

    header = df.columns.values.tolist()
    i = 2
    studentIndex = 0
    while i < len(header):
        # for each line (ie each school)
        if debugging:
            print("Processing student: " + header[i])
        schoolIndex = 0
        for index, row in df.iterrows():
            schoolList[schoolIndex].setPriority(row.iloc[i + 1])
            studentList[studentIndex].add_school(schoolList[schoolIndex])
            schoolIndex += 1
        # sort the schools by priority inside the student
        studentList[studentIndex].preferenceList.sort(key=lambda sch: sch.priority)
        if debugging:
            print("Modifying student school list: " + ", ".join
            (school.name for school in studentList[studentIndex].preferenceList) + "\n")
        studentIndex += 1
        i += 2

    return studentList, schoolList
