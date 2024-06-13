# file responsible of parsing the xlsx input file

import pandas as pd
from Student import *
from School import *


def check_integrity(df, debugging):
    print("\nChecking the integrity of the scenario...")
    # create all students (starting at cell 2 of line 0)
    studentList = []

    # Number of students
    student_number = 0

    header = df.columns.values.tolist()

    i = 2
    while i < len(header):
        # Create a student
        studentList.append(Student(header[i]))
        student_number += 1
        i += 2

    # Number of Schools
    school_number = len(df)

    # Calcul of the Total capacity of schools
    capacityTotal = 0

    # for each line in the xlsx file
    schoolList = []
    for index, row in df.iterrows():

        # Check if the capacity != 0

        if row['Capacity'] < 1:
            raise ValueError(f"The school {school.name} has a capacity < 1 \n")

        # Create a school
        school = School(row['Schools'], row['Capacity'])
        schoolList.append(school)
        capacityTotal += school.capacity

        # Create a list of the priority of the school
        i = 2
        priorityListOfSchool = []
        while i < len(row):
            # On vérifie qu'on a pas deux fois la même priorité de la part d'une école pour des élèves différents
            if row.iloc[i] in priorityListOfSchool:
                raise ValueError(
                    f"The school {school.name} is assigning priority  {row.iloc[i]} several times for differents students\n\n")
            elif row.iloc[i] < 1 or row.iloc[i] > student_number:
                raise ValueError(f"The priority {row.iloc[i]} assigned by the school {school.name} is invalid \n\n")
            priorityListOfSchool.append(row.iloc[i])
            i += 2

        if debugging:
            print("Priority list of " + school.name + " school : ")
        compteur = 0
        for y in priorityListOfSchool:
            compteur += 1
            if debugging:
                print("s" + str(compteur), end=' ')
                print("\n")
        for y in priorityListOfSchool:
            if debugging:
                print(y, end=' ')
                print("\n")
                print("-------------------------------")
    if debugging:
        print("Statistics : ")
        print("     Students number -> " + str(student_number))
        print("     Schools number -> " + str(school_number))
        print("     Schools total capacity -> " + str(capacityTotal) + "\n")

    i = 2
    priorityListOfStudent = []
    while i < len(header):
        # print("Processing student: " + header[i])

        for index, row in df.iterrows():
            if (row.iloc[i + 1]) in priorityListOfStudent:
                raise ValueError(f"The student " + str(header[i]) + " assigns priority " + str(
                    row.iloc[i + 1]) + " several times for different schools\n\n")
            if row.iloc[i + 1] < 1 or row.iloc[i + 1] > school_number:
                raise ValueError(f"The priority {row.iloc[i + 1]} assigned by the student {header[i]} is invalid\n\n")
            priorityListOfStudent.append(row.iloc[i + 1])
        if debugging:
            print("Priority list of " + header[i] + " student : ")
        compteur = 0
        for j in priorityListOfSchool:
            compteur += 1
            if debugging:
                print("e" + str(compteur), end=' ')
                print("\n")

        if debugging:
            for x in priorityListOfStudent:
                print(x, end=' ')
                print("\n")
                print("-------------------------------")

        priorityListOfStudent = []
        i += 2
        if debugging:
            print("\n")
    if debugging:
        print("The scenario is OK ! \n")
        print(f"There is {student_number} students for the a capacity of schools of {capacityTotal}")
        if student_number < capacityTotal:
            print("All of students will have a school\n\n")
        elif student_number > capacityTotal:
            print("some student will not have a school\n\n")
        elif student_number == capacityTotal:
            print("each student will have a school and each school will have a student\n\n")
    print("Scenario integrity check completed\n")
