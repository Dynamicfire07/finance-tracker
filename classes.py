import json
import sqlite3
from datetime import datetime
import math
import csv


class UserTransaction:
    def __init__(self):
        self.data_file = 'user_data.json'

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"balance": 0, "password": ""}

    def save_data(self, data):
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

    def check_existence(self):
        data = self.load_data()
        if data['password']:
            print("Thank you for returning. Your current balance is: ", data['balance'])
        else:
            print("No existing account found. Please register a new account.")
            self.register_account()

    def register_account(self):
        data = self.load_data()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM money")
        connection.commit()
        connection.close()
        balance = int(input("Enter your initial balance: "))
        password = input("Enter your password: ")
        password_checks = {1:False,2:False,3:False}
        if len(password) >= 8:
            password_checks[1] = True

        def has_nums(inputString):
            return any(char.isdigit() for char in inputString)
        def has_upper(inputString):
            return any(char.isupper() for char in inputString)
        password_checks[2] = has_nums(password)
        password_checks[3] = has_upper(password)
        
        if all(value == True for value in password_checks.values()):
                
           
            data = {"balance": balance, "password": password}
            self.save_data(data)
            print("Account registered. Your current balance is:", balance)
        else:
            print('''your password must have the following requirements:
                    1. Has atleast 8 characters
                    2. Has Letters and Numbers
                    3. Has atleast 1 capital letter
                    ''')
            self.register_account()


    def check_balance(self):
        data = self.load_data()
        print("Your current balance is: ", data['balance'])

    def add_money(self, amount):
        data = self.load_data()
        data['balance'] += amount
        self.save_data(data)
        print("Amount added successfully. New balance is:", data['balance'])

    def addTransactions(self,name,amount,date):
        data = self.load_data()
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        if amount> (20/100)*data['balance']:
            print("You are trying to spend a lot of money in one go please authenticate the purchase before spending")
            password = input('Enter your password: ')
            if password == data['password']:
                        
                cursor.execute("INSERT INTO money  VALUES (?, ?, ?)",
                (name, amount, date))
                connection.commit()
                connection.close()
                
                balance = data['balance'] - amount
                data = {'balance':balance,'password':password}
                self.save_data(data=data)
                print('Transaction was recorded successfully!')
            else:
                print("Password is incorrect! Try again")
        else:
            data = self.load_data()
            password = data['password']
            cursor.execute("INSERT INTO money  VALUES (?, ?, ?)",
                (name, amount, date))
            connection.commit()
            connection.close()
            
            balance = data['balance'] - amount
            data = {'balance':balance,'password':password}
            self.save_data(data=data)
            print('Transaction was recorded successfully!')
    
    def showTransactions(self):
        conneciton = sqlite3.connect('data.db')
        cursor = conneciton.cursor()
        cursor.execute("SELECT * FROM money")
        rows = cursor.fetchall()
        print(rows)
        print('NAME  | ',"AMOUNT  |"," Date and Time  |")
        for row in rows:
            print(f"{row[0]}|{row[1]}|{row[2]}|")
            print(50*"-")
    
    def changePassword(self):
        old_password = input('enter your old password: ')
        data = self.load_data()
        if old_password == data['password']:
            print("password was correct! Insert your new password now:")
            new_password = input("Enter your password: ")
            password_checks = {1:False,2:False,3:False}
            if len(new_password) >= 8:
                password_checks[1] = True

            def has_nums(inputString):
                return any(char.isdigit() for char in inputString)
            def has_upper(inputString):
                return any(char.isupper() for char in inputString)
            password_checks[2] = has_nums(new_password)
            password_checks[3] = has_upper(new_password)
           
            if all(value == True for value in password_checks.values()):
                    
                data['password'] = new_password
                data = {'balance':data['balance'],'password':new_password}
                self.save_data(data)
                print("Password was changed successfully!")
            else:
                print('''your password must have the following requirements:
                      1. Has atleast 8 characters
                      2. Has Letters and Numbers
                      3. Has atleast 1 capital letter
                      ''')
                self.changePassword()
            
    def loanRepayment(self,principle,interest,type,years):
        if type == "SI":
            total_amount = (principle*interest*years)/100
            per_month = (total_amount+principle)/(12*years)
            return per_month
        if type == "CI":
            amount = principle*(1+interest/100)**years
            per_month = amount/(12*years)
            return per_month
    
    def exportTransaction(self):
        filename = 'output.csv'
        conneciton = sqlite3.connect('data.db')
        cursor = conneciton.cursor()
        cursor.execute("SELECT * FROM money")
        rows = cursor.fetchall()
        with open(filename,'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Transaction Name','Amount','Date and Time'])
            writer.writerows(rows)


        

   
if __name__ == '__main__':
    
    transaction = UserTransaction()
    print("""
    ****************************
    *    Welcome to the Bank   *
    ****************************

    Please choose an option:
    1. Check balance
    2. Register account or check existing
    3. Add money
    4. Add Transaction
    5. Show all transactions
    6. Change Password
    7. Check how much owe per month to a person whom u owe a loan
    """)
    while True:

        usr_response = input('Enter your choice: ')
        if usr_response == '1':
            transaction.check_balance()
        elif usr_response == '2':
            transaction.check_existence()
        elif usr_response == '3':
            amount = int(input("Enter the amount to add: "))
            transaction.add_money(amount)
        elif usr_response == '4':
            transaction_name = input('Enter transaction name: ')
            amount = int(input("Enter transaction amount: "))
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transaction.addTransactions(name=transaction_name,amount=amount,date=date)

        
        elif usr_response =='5':
            transaction.showTransactions()
        
        elif usr_response == '6':
            transaction.changePassword()

        elif usr_response == '7':
            prinicple = int(input("Enter the prinicple: "))
            type = input("is it compound interest type CI, if simple interest type SI: ")
            time = int(input("Time in years: "))
            interest = int(input("Rate of interest per annum: "))
            print(transaction.loanRepayment(interest=interest,type=type,years=time,principle=prinicple))
        
        elif usr_response == '8':
            transaction.exportTransaction()
            print('transaction is exported successfully')
        else:
            print("Invalid choice. Please enter a valid option.")
