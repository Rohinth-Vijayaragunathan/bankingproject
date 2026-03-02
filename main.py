import pymysql

connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "1234",
    database = "Bank"
)

cursor = connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Bank")
print("database created successfully")

cursor.execute("CREATE TABLE IF NOT EXISTS Account_info(account_no INT PRIMARY KEY,name VARCHAR(30),balance INT DEFAULT 0)")
print("table created successfully")
connection.commit()

def create_account(account_no, name):
    sql = "INSERT INTO Account_info(account_no,name) VALUES(%s,%s)"
    values = (account_no,name)
    cursor.execute(sql,values)
    connection.commit()
    print("details add successfully")

def to_deposit(account_no,amount):
    sql = "UPDATE Account_info SET balance = balance + %s WHERE account_no = %s"
    values = (amount,account_no)
    cursor.execute(sql,values)
    connection.commit()
    print("amount deposited successfully")

def show_balance(account_no):
    sql = "SELECT account_no, name ,balance FROM Account_info WHERE account_no = %s"
    cursor.execute(sql,(account_no,))
    data = cursor.fetchone()

    if data:
        print(f"account no : {data[0]}, name : {data[1]}, balance : {data[2]}")
    else:
        print("account not found")

def to_withdrawal(account_no,amount):
    cursor.execute("SELECT balance FROM Account_info WHERE account_no = %s",(account_no,))
    result = cursor.fetchone()

    if not result:
        print("account not found")
        return

    balance = result[0]

    if amount > balance:
        print("insufficient fund")
    else:
        sql = "UPDATE Account_info SET balance = balance - %s WHERE account_no = %s"
        values = (amount, account_no)
        cursor.execute(sql, values)
        connection.commit()
        print("cash withdrawn successfully")

def to_delete(account_no):
    sql = "DELETE FROM Account_info WHERE Account_no = %s"
    cursor.execute(sql,(account_no,))
    connection.commit()
    print("account details deleted successfully")

while True:
    print("\n1.create account \n2.deposit \n3.balance \n4.withdrawal \n5.delete account \n6.Exit")
    choice = int(input("enter your choice:"))

    if choice == 1:
        account_no = int(input("enter your account no: "))
        name = input("enter your name: ")
        create_account(account_no,name)

    elif choice == 2:
        account_no = int(input("enter account no to deposit the amount: "))
        amount = int(input("enter the amount to deposit:"))
        if amount > 0:
            to_deposit(account_no,amount)
        else:
            print("amount is cannot be less than zero")

    elif choice == 3:
        account_no = int(input("enter your account no to check balance: "))
        show_balance(account_no)

    elif choice == 4:
        amount = int(input("enter amount to be withdrawn: "))
        account_no = int(input("enter your account no: "))
        to_withdrawal(account_no,amount)

    elif choice == 5:
        account_no = int(input("enter account no to delete account: "))
        to_delete(account_no)

    elif choice == 6:
        print("your exiting program")
        break
