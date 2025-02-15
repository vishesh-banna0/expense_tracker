import json
CREDIT = True
DEBIT = False
FILE_NAME = "tracker.json"
from datetime import datetime


def get_date():
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ")
        try:
            # Validate and convert to a date object
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            return date_obj.strftime("%Y-%m-%d")  # Return as a formatted string
        except ValueError:
            print("Invalid date format! Please enter in YYYY-MM-DD format.")


def load_ledger():
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {"ledger": []}
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return {"ledger": []}


def save_expenses(data):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Failed to save tasks: {e}")



def get_expense_type():
    while True:
        print("Enter Your Choice: \n"
              "1. Credit\n"
              "2. Debit")
        try:
            exp_type = int(input("Choice: "))  # Taking input safely
            if exp_type == 1:
                return True  # Credit -> Function exits
            elif exp_type == 2:
                return False  # Debit -> Function exits
            else:
                print("Please enter a valid option (1 or 2).")
        except ValueError:
            print("Invalid input! Please enter a number (1 or 2).")



def view_entries(data):
    print("Your Expense list: ")
    expense_list = data["ledger"]

    if not expense_list:
        print("Expense List is Empty")
    else:
        for idx, expense in enumerate(expense_list,start=1):
            expense_type = "[CREDIT]" if expense["type"] else "[DEBIT]"
            print(f"{idx}. Amount:                 {expense["amount"]}\n"
                           f"   Expense Description:    {expense["category"]}\n"
                           f"   Date of Transaction:    {expense["date"]} \n"
                           f"   Transaction Type:       {expense_type}")
            print("-" * 80)




def add_entry(data):
    try:
        expense_amount = int(input("Enter Expense amount: "))
        expense_description = input("Enter Description of Expense: ").strip()
        expense_date = get_date()
        expense_type = get_expense_type()  # Can be True (CREDIT) or False (DEBIT)

        # Ensure all values are valid (except expense_type, which can be False)
        if expense_amount > 0 and expense_description and expense_date is not None:
            data["ledger"].append({
                "amount": expense_amount,
                "category": expense_description,
                "date": expense_date,
                "type": expense_type  # Can be True (Credit) or False (Debit)
            })
            print("Expense added successfully!")
        else:
            print("Invalid input or unable to add entry. Please try again.")

    except ValueError:
        print("Invalid input! Please enter a valid number for the amount.")




def delete_entry(data):
    view_entries(data)
    try:
        del_number = int(input("Enter the number of entry you want to delete: "))
        if  1 <= del_number <= len(data["ledger"]):
            del data["ledger"][del_number - 1]
            save_expenses(data)
            print("Entry is deleted successfully")
        else:
            print("Invalid Entry")
    except Exception as e:
        print(f"Error {e}")


def monthly_expenses(data, month, year):
    """Calculate and display the monthly income, expenses, and balance."""
    expense_list = data["ledger"]
    credit_amount = 0
    debit_amount = 0

    for expense in expense_list:
        # Convert string date to datetime object
        expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")

        # Filter by selected month and year
        if expense_date.month == month and expense_date.year == year:
            if expense["type"] == CREDIT:
                credit_amount += expense["amount"]
            elif expense["type"] == DEBIT:
                debit_amount += expense["amount"]


    month_name = datetime(year=year, month=month, day=1).strftime('%B %Y')

    # Display results
    print(f"Monthly Summary - {month_name}")
    print(f"Total Income/Earnings: ₹{credit_amount}")
    print(f"Total Expenses/Spends: ₹{debit_amount}")

    net_income = credit_amount - debit_amount
    if net_income > 0:
        print(f"Profit: ₹{net_income}")
    elif net_income < 0:
        print(f"Loss: ₹{-net_income}")
    else:
        print("No Profit, No Loss. Net Income: ₹0")



def option_list():
    print('''Welcome to Your Personal Expense Tracker!  
                 Choose an option:  
                 1. Add Expense  
                 2. View All Expenses  
                 3. View Monthly Summary  
                 4. Delete an Expense  
                 5. Exit  
                 ''')
def main():
    ledger = load_ledger()
    option_list()

    print("- " * 80)
    while True:
        try:
            user_choice = int(input("Enter your option number from above to proceed: "))

            if user_choice == 1:
                add_entry(ledger)
                save_expenses(ledger)  # Save after adding an entry
                option_list()

            elif user_choice == 2:
                view_entries(ledger)
                option_list()

            elif user_choice == 3:
                # Get month and year input from the user
                try:
                    year = int(input("Enter Year (YYYY): "))
                    month = int(input("Enter Month (1-12): "))
                    if 1 <= month <= 12:
                        monthly_expenses(ledger, month, year)
                    else:
                        print("Invalid month! Please enter a number between 1 and 12.")
                except ValueError:
                    print("Invalid input! Please enter a valid year and month.")

                option_list()

            elif user_choice == 4:
                delete_entry(ledger)
                save_expenses(ledger)  # Save after deleting an entry
                option_list()

            elif user_choice == 5:
                print("Exiting Expense Tracker. Goodbye!")
                break

            else:
                print("Invalid Entry. Please try again.")

        except ValueError:
            print("Invalid input! Please enter a number between 1 and 5.")

main()

