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
    sc = input()
    print("Choose the sheet of the xlsx file:")
    print("1. sc-1")
    print("2. sc-2")
    print("3. sc-3")
    print("4. Other")
    print("")
    print("Enter your choice: ", end="")
    sheet = input()
    if sheet == "1":
        sheet = "sc-1"
    elif sheet == "2":
        sheet = "sc-2"
    elif sheet == "3":
        sheet = "sc-3"
    elif sheet == "4":
        print("Enter the sheet name: ", end="")
        sheet = input()
    return sc, sheet


def stableMariage(choix, sc="sc-1"):
    # Parse the Excel file
    studentList, schoolList = parsing.parse_xlsx("input.xlsx", sc, 0)
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
    result = np.empty((10, len(wifeList)), dtype=object)
    # foreach wife, fill result [0][i] with the wife index
    for i in range(len(wifeList)):
        result[0][i] = wifeList[i]

    currentAssignationNumber = 0
    day = 1
    Moreproposals = 1
    while Moreproposals:

        print("--------------------------------------------------")
        print("Day " + str(day))

        # at day, each husband will propose to his capacity wife(s)
        for husband in husbandList:
            for i in range(husband.capacity):
                if i < len(husband.preferenceList):
                    wife = husband.preferenceList[i]
                    # fill result[day][len(wifeList)] with a empty list
                    if result[day][wifeList.index(wife)] is None:
                        result[day][wifeList.index(wife)] = []
                    print(husband.name + " propose to " + wife.name)
                    result[day][wifeList.index(wife)].append(husband)

        print("-> Day " + str(day) + " result: " + str(result[day]))
        # at the night, each wife will choose the best husband (1 to capacity)
        countkick = 0
        for wife in wifeList:
            # foreach husband in the wife preference list
            acceptationCounter = 0
            print("-> " + wife.name + " selecting best proposals:")

            if result[day][wifeList.index(wife)] is not None:
                # remove the worst husband from the list
                index = len(wife.preferenceList) - 1
                while len(result[day][wifeList.index(wife)]) > wife.capacity:
                    worstHusband = wife.preferenceList[index]
                    if worstHusband in result[day][wifeList.index(wife)]:
                        print("      x " + wife.name + " kicked " + worstHusband.name)
                        countkick += 1
                        result[day][wifeList.index(wife)].remove(worstHusband)
                        # don't come back to the same husband
                        worstHusband.preferenceList.remove(wife)
                    index -= 1
        if countkick == 0:
            Moreproposals = 0
        print("-> Night " + str(day) + " result: " + str(result[day]))
        day += 1


choix = ""
scenario = ""
while choix != "3":
    choix, scenario = displayMenu()
    stableMariage(choix, scenario)
