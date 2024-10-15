# Project

The following link contains the challenge for this project:  
[https://roadmap.sh/projects/expense-tracker](https://roadmap.sh/projects/expense-tracker)

---

# What is this?

This is a CLI project that allows users to manage their finances. With this tool, users can:  
- **Create** a budget for each month of the current year.  
- **Add** an expense with a description, amount, and category.  
- **Update** an existing expense.  
- **Delete** an expense.  
- **View** all expenses and filter them by category.  
- **View** a summary of all expenses and filter it by a specific month (ofcurrent year).  
- **Receive a warning** if their spending exceeds the defined budget (if a budget exists).  

This CLI project accepts **options that require values** (e.g., `--description` argument). Therefore, the arguments are not mandatory. The logic of the program ensures that missing arguments are handled gracefully. For example:  
- If there is no budget for October, the application will not display a warning.  
- When updating an expense, users can modify one, all, or none of the fields (description, amount, category).  

---

# How to execute this code

Once you have the `main.py` file in your local environment, you can use the following commands to interact with the application:

```sh
python3 main.py add --description argument --amount argument --category argument  
python3 main.py update --id argument --description argument --amount argument --category argument
python3 main.py delete --id argument
python3 main.py list --category argument
python3 main.py summary --month argument
python3 main.py budget month amount  
python3 main.py export  
```