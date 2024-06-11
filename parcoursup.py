import numpy as np

import parsing


def displayMenu():
    print("")
    print("------------------------")
    print("Stable mariage Algorithm")
    print("------------------------")
    print("Choose which will be the wife:")
    print("1. Student")
    print("2. School")
    print("3. Exit")
    print("")
    print("Enter your choice: ", end="")
    choix = input()
    return choix


def stableMariage(choix):
    # Parse the excel file
    studentList, schoolList = parsing.parse_xlsx("input.xlsx", "sc-1", 0)
    # compute the minimum between the sum of school capacities and the number of students
    assignationNumber = min(len(studentList), sum([school.capacity for school in schoolList]))
    print("Assignation number: " + str(assignationNumber))

    # associate list to wife or husband
    wifeList = []
    husbandList = []
    if choix == "1":
        wifeList = studentList
        husbandList = schoolList
    elif choix == "2":
        wifeList = schoolList
        husbandList = studentList
    elif choix == "3":
        return
    else:
        print("/!\/!\/!\ Invalid choice /!\/!\/!\ \n")
        return

    # a tuple list composed by two list in each cell to store the result for each day
    result = np.empty((5, len(wifeList)), dtype=object)
    # foreach wife, fill result [0][i] with the wife index
    for i in range(len(wifeList)):
        result[0][i] = wifeList[i]

    currentAssignationNumber = 0
    day = 1
    # at the day one, each husband will propose to his capacity wife(s)
    for husband in husbandList:
        for i in range(husband.capacity):
            wife = husband.preferenceList[i]
            # fill result[day][len(wifeList)] with a empty list
            if result[day][wifeList.index(wife)] is None:
                result[day][wifeList.index(wife)] = []
            print(husband.name + " propose to " + wife.name)
            result[day][wifeList.index(wife)].append(husband)

    print("---> Day " + str(day) + ":")
    print(result[day])


# while currentAssignationNumber < assignationNumber:


choix = ""
while (choix != "3"):
    choix = displayMenu()
    stableMariage(choix)

# LA liste des eleves pour une école elle est triée dans
# L'ordre de préference des eleves non ?
