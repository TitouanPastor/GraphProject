import numpy as np
import pandas as pd
import parsing
from error_detection import check_integrity
from graphDisplay import creationGraphe, displayGraph
from menus import displayResult, displayScMenu, displayWifeMenu, askForDebugging


def stableMarriage(choix, df, debugging=0):
    # Parse the Excel file
    studentList, schoolList = parsing.parse_xlsx(df, 0)

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
            displayResult(day, result, wifeList)
            displayGraph(day, debugging, husbandList, result, wifeList)

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


file_path = "input.xlsx"
# open the xlsx file at the sheet index (scenario)
xlsx = pd.read_excel(file_path, sheet_name=None)
while 1:
    # Ask for the scenario
    scenario = displayScMenu(xlsx)
    if scenario is None:
        break
    # Ask for the wife
    choice = displayWifeMenu()
    if choice == "0":
        break

    try:
        # check the integrity of the scenario
        debugging = askForDebugging()
        check_integrity(scenario, debugging)
        # ask for debugging
        # start the stable marriage algorithm
        stableMarriage(choice, scenario, debugging)
    except ValueError as e:
        #delete terminal output
        print("⬤ An error occurred while checking the integrity of the scenario:")
        print("\t ╳ " + str(e))
    except FileNotFoundError:
        print("The file input.xlsx was not found")
