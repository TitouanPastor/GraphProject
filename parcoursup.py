import numpy as np

import parsing
from graphDisplay import creationGraphe


def displayWifeMenu():
    print("")
    print("------------------------")
    print("Stable mariage Algorithm")
    print("------------------------")
    print("Choose which will be the wife:")
    print("1. Student")
    print("2. School")
    print("0. Exit")
    print("")
    print("Enter your choice: ", end="")
    return input()


def displayScMenu():
    print("Choose the sheet of the xlsx file:")
    print("1. sc-1")
    print("2. sc-2")
    print("3. sc-3")
    print("4. sc-4")
    print("5. sc-5")
    print("0. Other")
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
        sheet = "sc-4"
    elif sheet == "5":
        sheet = "sc-5"
    elif sheet == "0":
        print("Enter the sheet name: ", end="")
        sheet = input()
    else:
        print("Invalid choice, please enter a valid choice")
        return displayScMenu()
    return sheet

def askForDebugging():
    print("Do you want to show each day logs? (default: 0)")
    print("1. Yes")
    print("0. No")
    print("")
    print("Enter your choice: ", end="")
    input = input()
    if input != "1" or input != "0":
        return "0"


def stableMariage(choix, sc="sc-1", debugging=0):
    # Parse the Excel file
    studentList, schoolList = parsing.parse_xlsx("input.xlsx", sc, 0)

    # associate list to wife or husband
    wifeList = []
    husbandList = []
    if choix == "1":
        wifeList = studentList
        husbandList = schoolList
    elif choix == "2":
        wifeList = schoolList
        husbandList = studentList

    # a tuple list composed by two list in each cell to store the result for each day
    result = [[None] * len(wifeList) for _ in range(10)]  # foreach wife, fill result [0][i] with the wife index
    for i in range(len(wifeList)):
        result[0][i] = wifeList[i]

    day = 1
    Moreproposals = 1
    while Moreproposals:
        # at day, each husband will propose to his capacity wife(s)
        countProposals = 0
        for husband in husbandList:
            for i in range(husband.capacity):
                if i < len(husband.preferenceList):
                    wife = husband.preferenceList[i]
                    # fill result[day][len(wifeList)] with a empty list
                    if result[day][wifeList.index(wife)] is None:
                        result[day][wifeList.index(wife)] = []
                    if debugging:
                        print(husband.name + " propose to " + wife.name)
                    result[day][wifeList.index(wife)].append(husband)
                    husband.capacity -= 1
                    countProposals += 1
        if countProposals == 0:
            Moreproposals = 0
            print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("┃         DAY " + str(day) + " result          ┃")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            for wife in result[0]:
                print("\t-> " + wife.name + " assigned to : " + str(result[day][wifeList.index(wife)]))
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

            # now make a matrix to show with networkx and pyplot
            # Number of wives (number of columns)
            n = len(wifeList)
            # number of husbands (number of lines)
            m = len(husbandList)

            # Initialiser une matrice de n x n avec des infinis
            M = np.full((n, m), float('inf'))

            for wife in result[0]:
                for husband in result[day][wifeList.index(wife)]:
                    M[wifeList.index(wife)][husbandList.index(husband)] = 1

            print("M: ", M)
            # Afficher le graphe
            creationGraphe(M, wifeList, husbandList)

        else:
            if debugging:
                print("--------------------------------------------------")
                print("-> Day " + str(day) + " result: " + str(result[day]))
            for wife in wifeList:
                # foreach husband in the wife preference list
                acceptationCounter = 0
                if debugging:
                    print("-> " + wife.name + " selecting best proposals:")

                if result[day][wifeList.index(wife)] is not None:
                    # remove the worst husband from the list
                    index = len(wife.preferenceList) - 1
                    while len(result[day][wifeList.index(wife)]) > wife.capacity:
                        worstHusband = wife.preferenceList[index]
                        if worstHusband in result[day][wifeList.index(wife)]:
                            if debugging:
                                print("      x " + wife.name + " kicked " + worstHusband.name)
                            result[day][wifeList.index(wife)].remove(worstHusband)
                            # don't come back to the same husband
                            # if was previously selected by the wife, we already remove the wife from the husband preference list
                            if wife in worstHusband.preferenceList:
                                worstHusband.preferenceList.remove(wife)
                            worstHusband.capacity += 1
                        index -= 1
                    # save the husband that are accepted for the next day
                    result[day + 1][wifeList.index(wife)] = result[day][wifeList.index(wife)]
                    # foreach husband, if this is the first time the husband is selected, remove the wife from his preference list
                    for husband in result[day][wifeList.index(wife)]:
                        if wife in husband.preferenceList:
                            if debugging:
                                print("      + " + wife.name + " accepted " + husband.name)
                            husband.preferenceList.remove(wife)
            if debugging:
                print("-> Night " + str(day) + " result: " + str(result[day]))

        day += 1


choix = ""
scenario = ""
while 1:
    scenario = displayScMenu()
    choix = displayWifeMenu()
    if choix == "0":
        break
    debugging = askForDebugging()
    stableMariage(choix, scenario, int(debugging))
