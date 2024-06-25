from datetime import datetime
from classes import UserTransaction

print("""
****************************
*    Welcome to the Bank    *
****************************

Please choose an option:
1. Check balance
2. Add a transaction
3. Add Balance
4. View Transactions
""")
while True:
    usr_response = input('Enter your choice: ')
    transaction = UserTransaction()

    if usr_response == '1':
        transaction.check_balance()
    elif usr_response == '2':
        transaction.check_existence()
        name = input("Enter your name: ")
        amount = int(input("Enter the transaction amount: "))
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction.transaction(name, amount, date)

    elif usr_response == '3':
        amount = int(input("Enter the transaction amount: "))
        transaction.addMoney(amount)

    else:
        print("Invalid choice. Please enter 1 or 2.")
