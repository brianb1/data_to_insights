#-----------#
# LIBRARIES #
#-----------#

import pandas as pd
import sqlite3
import os


#----------#
# RAW DATA #
#----------#

customers=pd.read_excel(
    'data/Superstore_db.xlsx', 
    sheet_name='customer',
    header=0
)

sales=pd.read_excel(
    'data/Superstore_db.xlsx', 
    sheet_name='sales',
    header=0)

orders  = pd.read_excel(
    'data/Superstore_db.xlsx', 
    sheet_name='order',
    header=0)

products  = pd.read_excel(
    'data/Superstore_db.xlsx', 
    sheet_name='product',
    header=0
)


#-----------------#
# CREATE DATABASE #
#-----------------#

db_conn = sqlite3.connect("data/superstore.db")
c = db_conn.cursor()

pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", db_conn)
#pd.read_sql("SELECT * FROM sales LIMIT 10", db_conn)


#---Add primary and foreign key constraints

c.execute('PRAGMA primary_keys = off')
c.execute('PRAGMA foreign_keys = off')
c.execute('PRAGMA unique_keys = off')

# SALES
c.execute(
    """
    CREATE TABLE sales ( 
        SalesID VARCHAR , 
        OrderID VARCHAR NOT NULL,
        ProductID VARCHAR NOT NULL, 
        CustomerID VARCHAR NOT NULL,
        Sales VARCHAR,
        Quantity SMALLINT, 
        Discount VARCHAR,
        Profit VARCHAR,
        PRIMARY KEY(SalesID),
        FOREIGN KEY(OrderID) REFERENCES orders(OrderID), 
        FOREIGN KEY(CustomerID) REFERENCES customers(CustomerID), 
        FOREIGN KEY(ProductID) REFERENCES products(ProductID) 
        );"""
)

# ORDERS
c.execute(
    """
    CREATE TABLE orders ( 
        OrderID VARCHAR,
        OrderDate DATE,
        ShipDate DATE,
        ShipMode TEXT,
        CustomerID VARCHAR ,
        PRIMARY KEY(OrderID),
        FOREIGN KEY(CustomerID) REFERENCES customers(CustomerID) 
        );
    """
)

# CUSTOMERS
c.execute(
    """
    CREATE TABLE customers ( 
        CustomerID VARCHAR PRIMARY KEY,
        CustomerName TEXT,
        Segment TEXT,
        Country TEXT,
        City TEXT,
        State TEXT,
        PostalCode VARCHAR,
        Region TEXT
        );
    """
)

# PRODUCTS
c.execute(
    """
    CREATE TABLE products ( 
        ProductID VARCHAR PRIMARY KEY,
        Category TEXT,
        SubCategory TEXT,
        ProductName TEXT
        );
    """
)

products.to_sql('products', db_conn, if_exists='append', index=False)
customers.to_sql('customers', db_conn, if_exists='append', index=False)
orders.to_sql('orders', db_conn, if_exists='append', index=False)
sales.to_sql('sales', db_conn, if_exists='append', index=False)
