import os 
import json 
import argparse
from datetime import datetime
import pandas as pd

EXPENSES_FILE = "expenses.json"
BUDGETS_FILE = "budget.json"

def load_file():
    if not os.path.exists("expenses.json"):
        return []
    with open("expenses.json", "r") as file:
        return json.load(file)
    
def save_expense(expense):
    with open("expenses.json", "w") as file:
        json.dump(expense, file, indent=2)

def load_file_budget():
    if not os.path.exists("budget.json"):
        return []
    with open("budget.json", "r") as file:
        return json.load(file)       
    
def save_budgets(budget):
    with open("budget.json", "w") as file:
        json.dump(budget, file)    

def add_budget(month, amount):
    budgets = load_file_budget()

    if month not in range(1,13):
        print('The month must be a number between 1 and 12')
        return
    if not budgets:
        budget = {month: amount}
        budgets.append(budget)
    else:
        budgets[0][f'{month}'] = amount
    save_budgets(budgets)
    print(f"Budget for the month {month} successfully saved")  

def summary_for_budget(expenses, month):  
    summary = [expense['amount'] if expense['amount'] is not None and datetime.strptime(expense['date'], '%Y-%m-%d').month == month else 0 for expense in expenses]
    return sum(summary)

def budget_expenses_vs(current_day, expenses):
    budgets = load_file_budget()

    existents_months = 0 if not budgets else budgets[0].keys()  

    if existents_months != 0:
        if f'{current_day}' in list(existents_months):
            current_budget = budgets[0][f'{current_day}']        
            total_expenses = summary_for_budget(expenses, current_day)
            if total_expenses > current_budget:
                print(f'your budget for the month {current_day} has been exceeded. Budget: {current_budget}, Total expenses: {total_expenses}')


def add_expense(description, amount, category):
    expenses = load_file() 
    current_day = datetime.now()

    ids_list = 1 if not expenses else [id_number['id'] for id_number in expenses]

    expense = {
        'id': 1 if ids_list == 1 else ids_list[-1]+1,
        'date': current_day.strftime("%Y-%m-%d"),
        'description': description,
        'amount': amount,
        'category': category
    } 
    expenses.append(expense)

    budget_expenses_vs(current_day.month, expenses)

    save_expense(expenses)
    print(f"Expense added successfully (ID: {expense['id']})")  

def exist_expense(id):
    expenses = load_file()
    current_state = False
    
    exist = any(expense['id']==id for expense in expenses)
    if exist:
        current_state = True

    return current_state     

def update_expense(id, description=None, amount=None, category=None):   
    expenses = load_file()
    exist = exist_expense(id)
    current_day = 0

    if not exist:
        print(f"Expense with id:{id} doesn't exist")
        return 
    
    for expense in expenses:
        if expense['id'] == id:
            expense['description'] = expense['description'] if description is None else description
            expense['amount'] = expense['amount'] if amount is None else amount
            expense['category'] = expense['category'] if category is None else category
            current_day = (datetime.strptime(expense['date'], '%Y-%m-%d').month)

    if amount is not None:
        budget_expenses_vs(current_day, expenses)
  
    save_expense(expenses)
    print(f"Expense whit id:{id} updated successfully") 

def delete_expense(id):
    exist = exist_expense(id)

    if not exist:
        print(f"Expense with id:{id} dosen't exist")
        return

    expenses = load_file()
    new_expenses = [expense for expense in expenses if expense['id'] != id]
    save_expense(new_expenses)
    print(f"Expense with id:{id} successfully deleted")

def view_expenses(category=None):
    expenses = load_file()

    if not expenses:
        print("You don't have expenses registered")
        return
    
    all_expenses = "ID  Date       Description  Amount  Category\n"

    if category == None:
        all_expenses += "\n".join([f"{expense['id']} - {expense['date']} - {expense['description']} - {expense['amount']} - {expense['category']}" for expense in expenses])
    else:
        all_expenses += "\n".join([f"{expense['id']} - {expense['date']} - {expense['description']} - {expense['amount']} - {expense['category']}" for expense in expenses if expense['category'] == category])

    print(all_expenses)

def summary(month=None):
    expenses = load_file()

    if not expenses:
        print(f"You don't have expenses registered")
        return
    
    if month == None:
        expenses_summary = [expense['amount'] for expense in expenses if expense['amount'] is not None]
        print(f"Total expenses: ${sum(expenses_summary)}")
        return
    
    if month < 1 or month > 12:
        print(f"Month incorrect, digit a month between 1 and 12")
        return
    else:    
        expenses_summary = [expense['amount'] if (datetime.strptime(expense['date'], '%Y-%m-%d').month) == month and expense['amount'] is not None else 0 for expense in expenses]

        months = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre"
        }
        print(f"Total expenses for {months[month]}: ${sum(expenses_summary)}")  

def convertoexcel():
    expenses = load_file()
    df_expenses = pd.DataFrame(expenses)
    df_expenses.to_csv('my_expenses.csv', index=False)

def main():   
    parser = argparse.ArgumentParser(description='expense tracker application to manage your finances')  
    subparsers = parser.add_subparsers(dest='command')  

    # add expense command 
    parser_add = subparsers.add_parser('add', help='add a new expense')
    parser_add.add_argument('--description', type=str, help='description of the expense done')
    parser_add.add_argument('--amount', type=int, help='amount of the expense done')
    parser_add.add_argument('--category', type=int, help='category of the expense')

    # update expense command
    parser_update = subparsers.add_parser('update', help='update an expense')
    parser_update.add_argument('--id', type=int, help='id of the expense')
    parser_update.add_argument('--description', type=str, help='description of the expense done')
    parser_update.add_argument('--amount', type=int, help='amount of the expense done')
    parser_update.add_argument('--category', type=int, help='category of the expense')

    # delete expense command
    parser_delete = subparsers.add_parser('delete', help='delete an expense')
    parser_delete.add_argument('--id', type=int, help='id of the expense to be deleted')

    # view expenses command
    parser_view = subparsers.add_parser('list', help='delete an expense')
    parser_view.add_argument('--category', type=int, help='category of the expense')

    # summary of all expenses
    parser_summary = subparsers.add_parser('summary', help='summary of all expenses')
    parser_summary.add_argument('--month', type=int, help='month of the expense')

    # budget for each month command
    parser_budget = subparsers.add_parser('budget', help='set a budget for each month')
    parser_budget.add_argument('month', type=int, help='month of the budget')
    parser_budget.add_argument('amount', type=int, help='budget of the month')

    # export expenses command
    parser_export = subparsers.add_parser('export', help='export the expenses to a csv file')

    args = parser.parse_args()

    commands = {
        'add': lambda: add_expense(args.description, args.amount, args.category),
        'update': lambda: update_expense(args.id, args.description, args.amount, args.category),
        'delete': lambda: delete_expense(args.id),
        'list': lambda: view_expenses(args.category),
        'summary': lambda: summary(args.month),
        'budget': lambda: add_budget(args.month, args.amount),
        'export': lambda: convertoexcel()
    }   

    commands_function = commands.get(args.command, lambda: parser.print_help())
    commands_function()

if __name__ == '__main__':
    main()



