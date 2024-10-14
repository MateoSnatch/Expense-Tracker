import os 
import json 
import argparse
from datetime import datetime
import pandas as pd
import calendar

EXPENSES_FILE = "expenses.json"
BUDGETS_FILE = "budget.json"

def load_files(path):
    if not os.path.exists(f"{path}.json"):
        return []
    with open(f"{path}.json", "r") as file:
        return json.load(file)  
    
def save_files(info, path):
    with open(f"{path}.json", "w") as file:
        json.dump(info, file, indent=2) 

def add_budget(month, amount):
    budgets = load_files('budget_file')

    if month not in range(1,13):
        print('The month must be a number between 1 and 12')
        return
    if not budgets:
        budget = {month: amount}
        budgets.append(budget)
    else:
        budgets[0][f'{month}'] = amount
    save_files(budgets, 'budget_file')
    print(f"Budget for the month {month} successfully saved")  

def summary_for_budget(expenses, month):  
    summary = [expense['amount'] if expense['amount'] is not None and datetime.strptime(expense['date'], '%Y-%m-%d').month == month else 0 for expense in expenses]
    return sum(summary)

def budget_expenses_difference(current_month, expenses):
    budgets = load_files('budget_file')

    existents_months = 0 if not budgets else budgets[0].keys()  

    if existents_months != 0:
        if f'{current_month}' in list(existents_months):
            current_budget = budgets[0][f'{current_month}']        
            total_expenses = summary_for_budget(expenses, current_month)
            if total_expenses > current_budget:
                print(f'your budget for the month {current_month} has been exceeded. Budget: {current_budget}, Total expenses: {total_expenses}')


def add_expense(description, amount, category):
    expenses = load_files('expenses_file') 
    current_month = datetime.now()
    id_expense = len(expenses)+1

    expense = {
        'id': id_expense,
        'date': current_month.strftime("%Y-%m-%d"),
        'description': description,
        'amount': amount,
        'category': category
    } 

    expenses.append(expense)
    budget_expenses_difference(current_month.month, expenses)
    save_files(expenses, 'expenses_file')
    print(f"Expense added successfully (ID: {expense['id']})")  

def exist_expense(id):
    expenses = load_files('expenses_file')
    current_state = False
    exist = any(expense['id']==id for expense in expenses)
    if exist:
        current_state = True
    return current_state     

def update_expense(id, description=None, amount=None, category=None):   
    expenses = load_files('expenses_file')
    exist = exist_expense(id)

    if not exist:
        print(f"Expense with id:{id} doesn't exist")
        return 
    
    for expense in expenses:
        if expense['id'] == id:
            expense['description'] = expense['description'] if description is None else description
            expense['amount'] = expense['amount'] if amount is None else amount
            expense['category'] = expense['category'] if category is None else category
            current_month = (datetime.strptime(expense['date'], '%Y-%m-%d').month)

    if amount is not None:
        budget_expenses_difference(current_month, expenses)
  
    save_files(expenses, 'expenses_file')
    print(f"Expense whit id:{id} updated successfully") 

def delete_expense(id):
    exist = exist_expense(id)

    if not exist:
        print(f"Expense with id:{id} dosen't exist")
        return
    
    expenses = load_files('expenses_file')
    new_expenses = [expense for expense in expenses if expense['id'] != id]
    save_files(new_expenses, 'expenses_file')
    print(f"Expense with id:{id} successfully deleted")

def view_expenses(category=None):
    expenses = load_files('expenses_file')

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
    expenses = load_files('expenses_file')

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

        months_name = calendar.month_name[month]
        print(f"Total expenses for {months_name}: ${sum(expenses_summary)}")  

def convertoexcel():
    expenses = load_files('expenses_file')
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



