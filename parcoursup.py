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
    print("Choose the sheet of the xlsx file:")
    print("1. sc-1")
    print("2. sc-2")
    print("3. sc-3")
    print("4. Other")
    print("")
    print("Enter your choice: ", end="")
    sheetName = input()
    if sheetName == "1":
        sheetName = "sc-1"
    elif sheetName == "2":
        sheetName = "sc-2"
    elif sheetName == "3":
        sheetName = "sc-3"
    elif sheetName == "4":
        print("Enter the sheet name: ", end="")
        sheetName = input()
    return choix, sheetName


def stableMariage(choix, sheetName="sc-1"):
    # Parse the Excel file
    studentList, schoolList = parsing.parse_xlsx("input.xlsx", sheetName, 0)
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

    while currentAssignationNumber < assignationNumber:

        print("--------------------------------------------------")
        print("Day " + str(day))

        # at the day one, each husband will propose to his capacity wife(s)
        for husband in husbandList:
            for i in range(husband.capacity):
                wife = husband.preferenceList[i]
                # fill result[day][len(wifeList)] with a empty list
                if result[day][wifeList.index(wife)] is None:
                    result[day][wifeList.index(wife)] = []
                print(husband.name + " propose to " + wife.name)
                result[day][wifeList.index(wife)].append(husband)

        # at the night, each wife will choose the best husband (1 to capacity)
        for wife in wifeList:
            # foreach husband in the wife preference list
            acceptationCounter = 0
            for husband in wife.preferenceList:
                # if the husband is in the result list
                if result[day][wifeList.index(wife)] is not None and husband in result[day][wifeList.index(wife)]:

                    # if the wife.assignedList is full, then we need to replace the worst husband in the list by the current husband
                    # and if the wife.assignedList is not full (ie wife.capacity not 0) then just add the husband to the assigned list
                    CurrentHusbandRank = wife.preferenceList.index(husband)
                    if len(wife.assignedList) == wife.capacity:  # if the wife.assignedList is full
                        for assignedHusband in wife.assignedList:
                            assignedHusbandRank = wife.preferenceList.index(assignedHusband)
                            if CurrentHusbandRank < assignedHusbandRank:
                                print(wife.name + " kicked " + assignedHusband.name + " for " + husband.name)
                                wife.assignedList.remove(assignedHusband)  # remove the worst husband from the list
                                break
                    else:  # if the wife.assignedList is not full
                        print(wife.name + " accept " + husband.name)
                        # remove the husband from husbandList
                        husbandList.remove(husband)
                        # add the husband to the assigned list of the wife
                        wife.assignedList.append(husband)
                        currentAssignationNumber += 1
                        acceptationCounter += 1
                        if acceptationCounter == wife.capacity:
                            break
        day += 1


choix = ""
sheetName = ""
while (choix != "3"):
    choix, sheetName = displayMenu()
    stableMariage(choix, sheetName)

# LA liste des eleves pour une école elle est triée dans
# L'ordre de préference des eleves non ?
