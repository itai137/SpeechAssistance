# --------------- Speech Assistance - Stocks ----------------- #

# Imports
from Classes import Stock
import pyrebase
from datetime import datetime


#   ---- Data Base Methods ----


def check_stock_portfolio(firebase_database, ticker):
    open_transaction = firebase_database.child("Portfolio").child(ticker).get()
    if open_transaction.val() is None:
        return False
    return True


def check_total(firebase_database):
    open_transaction = firebase_database.child("Total").child("Total").get()
    if open_transaction.val() is None:
        return False
    return True


def delete_stock_from_protfolio(firebase_database, stock_transaction):
    firebase_database.child("Portfolio").child(stock_transaction["Ticker"]).delete()


def add_to_portfolio(firebase_database, stock_transaction):
    firebase_database.child("Portfolio").child(stock_transaction["Ticker"]).set(stock_transaction)


def add_to_record(firebase_database, stock_transaction):
    firebase_database.child("Records").child(stock_transaction["Date"]).set(stock_transaction)


def set_portfolio_total(firebase_database):
    total = {"Total": 0}
    firebase_database.child("Total").child("Total").set(total)


def update_position(firebase_database, new_record_dic):
    database_record_dic = firebase_database.child("Portfolio").child(new_record_dic["Ticker"]).get().val()
    database_get_total = firebase_database.child("Total").child("Total").get().val()
    current_ticker = new_record_dic["Ticker"]

    if new_record_dic["Status"] == "buy":
        update_amount = database_record_dic["Amount"] + new_record_dic["Amount"]
        total_cost = new_record_dic["TotalInvest"] + database_record_dic["TotalInvest"]
        avg_cost = total_cost / update_amount
        all_total_invest = database_record_dic["TotalInvest"] + new_record_dic["TotalInvest"]

        firebase_database.child("Portfolio").child(current_ticker).update(
            {"Amount": update_amount, "Price": avg_cost, "TotalInvest": all_total_invest})

    if new_record_dic["Status"] == "sell":
        change_in_profit = new_record_dic["Amount"] * database_record_dic['Price']
        calculate_gross_profit = new_record_dic["TotalInvest"] - change_in_profit + database_get_total["Total"]

        firebase_database.child("Total").child("Total").update({"Total": calculate_gross_profit})

        if new_record_dic["Amount"] == database_record_dic["Amount"]:
            delete_stock_from_protfolio(firebase_database,current_ticker)
        else:
            new_amount = database_record_dic["Amount"] - new_record_dic["Amount"]
            new_total_invest = new_amount * database_record_dic["Price"]
            update_part_sell = {"Amount": new_amount, "TotalInvest": new_total_invest}

            firebase_database.child("Portfolio").child(current_ticker).update(update_part_sell)

    
        

# function which will update total when stocks sold
# method update_total (firebase_database, total)

# def update_total(firebase_database,total ):


#   ---- End Base Methods ----


#  ---- Create Stock Methods ----


def get_current_data_time():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


#  ---- End Stocks Methods ----

# Firebase attributes


config = {
    "apiKey": "AIzaSyCBSL6sXHQz7Ou1j5ZzMTskFvLCRVOeHUI",
    "authDomain": "speechstockassistance.firebaseapp.com",
    "projectId": "speechstockassistance",
    "storageBucket": "speechstockassistance.appspot.com",
    "messagingSenderId": "937221386442",
    "appId": "1:937221386442:web:df5bf18006a62f51800433",
    "measurementId": "G-ES7N1JJMTW",
    "databaseURL": "https://speechstockassistance-default-rtdb.firebaseio.com/"
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()
#  End Firebase attributes


# Main Commands

# create new stock name,price,date,amount
new_stock = Stock.OrderFromUser("Soxl", "Semiconductor Bull 3X Shares", 15, get_current_data_time(), 300, "buy")
new_stock2 = Stock.OrderFromUser("Soxl", "Semiconductor Bull 3X Shares", 20, get_current_data_time(), 250, "sell")

stock_dic = {
    "Ticker": new_stock.ticker,
    "Name": new_stock.name,
    "Price": new_stock.price,
    "Date": new_stock.date.replace("/", "-"),
    "Amount": new_stock.amount,
    "TotalInvest": new_stock.amount * new_stock.price
}
record_dic = {
    "Ticker": new_stock.ticker,
    "Name": new_stock.name,
    "Price": new_stock.price,
    "Date": new_stock.date.replace("/", "-"),
    "Amount": new_stock.amount,
    "TotalInvest": new_stock.amount * new_stock.price,
    "Status": "sell"
}

record_dic2 = {
    "Ticker": new_stock2.ticker,
    "Name": new_stock2.name,
    "Price": new_stock2.price,
    "Date": new_stock2.date.replace("/", "-"),
    "Amount": new_stock2.amount,
    "TotalInvest": new_stock2.amount * new_stock2.price,
    "Status": "sell"
}

# Push data
# אם לא קיים טבלה total
if not (check_total(database)):
    set_portfolio_total(database)

if not (check_stock_portfolio(database, "Soxl")):
    add_to_portfolio(database, stock_dic)
    add_to_record(database, record_dic)
else:
    update_position(database, record_dic2)
    add_to_record(database, record_dic2)

# speech_to_text
#between machine to api

#take recording for 10 sec and write it
#seasrch howe to add Google dialouge if there is a service.
