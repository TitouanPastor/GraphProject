
def displayBootMenu():
    # do me a beautiful menu with Stable Marriage title and other stuff, be creative
    null = 0


def displayWifeMenu():
    print("")
    print("Choose which will be the wife:")
    print("1. Student")
    print("2. School")
    print("0. Exit")
    print("")
    print("Enter your choice: ", end="")
    value = input()
    if value != "1" and value != "2" and value != "0":
        print("Invalid choice, please enter a valid choice")
        return displayWifeMenu()
    return value


def displayScMenu(df):
    print("Choose the sheet of the xlsx file:")
    sheet_names = list(df.keys())
    for i, sheet_name in enumerate(sheet_names, start=1):
        print(f"{i}. {sheet_name}")
    print("0. Exit")
    print("")
    print("Enter your choice: ", end="")
    choice = input()
    if choice == "0":
        return None
    elif choice.isdigit() and 1 <= int(choice) <= len(sheet_names):
        print("You selected: " + sheet_names[int(choice) - 1])
        return df[sheet_names[int(choice) - 1]]
    else:
        print("Invalid choice, please enter a valid choice")
        return displayScMenu(df)


def askForDebugging():
    print("Do you want to show each day logs? (default: 0)")
    print("1. Yes")
    print("0. No")
    print("")
    print("Enter your choice: ", end="")
    value = input()
    if value != "1" or value != "0":
        return 0
    return int(value)


def displayResult(day, result, wifeList):
    print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃         DAY " + str(day) + " result          ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    for wife in result[0]:
        print("\t-> " + wife.name + " assigned to : " + str(result[day][wifeList.index(wife)]))
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
