import sqlite3

nameDB = "NorthWindTest_1.db"


def add_customers_many(list):
    conn = sqlite3.connect("../../BE_RestAPI_Hybrid_Nortwind/instance/" + nameDB)
    cursor = conn.cursor()
    for value in list:
        cursor.execute(
            "insert into customers (CustomerName, ContactName, Address, City, PostalCode, Country) values (?,?,?,?,?,?)",
            (value[0], value[1], value[2], value[3], value[4], value[5]),
        )
    conn.commit()
    conn.close()


def add_employees_many(list):
    conn = sqlite3.connect("../../BE_RestAPI_Hybrid_Nortwind/instance/" + nameDB)
    cursor = conn.cursor()
    for value in list:
        cursor.execute(
            "insert into employees (LastName, FirstName, BirthDate, Photo, Notes) values (?,?,?,?,?)",
            (value[0], value[1], value[2], value[3], value[4]),
        )
    conn.commit()
    conn.close()


def add_shippers_many(list):
    conn = sqlite3.connect("../../BE_RestAPI_Hybrid_Nortwind/instance/" + nameDB)
    cursor = conn.cursor()
    for value in list:
        cursor.execute(
            "insert into shippers (ShipperName, Phone) values (?,?)",
            (value[0], value[1]),
        )
    conn.commit()
    conn.close()


def add_suppliers_many(list):
    conn = sqlite3.connect("../../BE_RestAPI_Hybrid_Nortwind/instance/" + nameDB)
    cursor = conn.cursor()
    for value in list:
        cursor.execute(
            "insert into suppliers (SupplierName, ContactName, Address, City, PostalCode, Country) values (?,?,?,?,?,?)",
            (value[0], value[1], value[2], value[3], value[4], value[5]),
        )
    conn.commit()
    conn.close()


def add_categories_many(list):
    conn = sqlite3.connect("../../BE_RestAPI_Hybrid_Nortwind/instance/" + nameDB)
    cursor = conn.cursor()
    for value in list:
        cursor.execute(
            "insert into categories (CategoryName, Description) values (?,?)",
            (value[0], value[1]),
        )
    conn.commit()
    conn.close()


def add_products_many(list):
    conn = sqlite3.connect("../../BE_RestAPI_Hybrid_Nortwind/instance/" + nameDB)
    cursor = conn.cursor()
    for value in list:
        cursor.execute(
            "insert into products (Productname, SupplierID, CategoryID, Unit, Price) values (?,?,?,?,?)",
            (value[0], value[1], value[2], value[3], value[4]),
        )
    conn.commit()
    conn.close()


def add_orders_many(list):
    conn = sqlite3.connect("../../BE_RestAPI_Hybrid_Nortwind/instance/" + nameDB)
    cursor = conn.cursor()
    for value in list:
        cursor.execute(
            "insert into orders (CustomerID, EmployeeID, OrderDate, ShipperID) values (?,?,?,?)",
            (value[0], value[1], value[2], value[3]),
        )
    conn.commit()
    conn.close()


def add_orderdetails_many(list):
    conn = sqlite3.connect("../../BE_RestAPI_Hybrid_Nortwind/instance/" + nameDB)
    cursor = conn.cursor()
    for value in list:
        cursor.execute(
            "insert into orderdetails (OrderID, ProductID, Quantity) values (?,?,?)",
            (int(value[0]) - 10247, value[1], value[2]),
        )
    conn.commit()
    conn.close()
