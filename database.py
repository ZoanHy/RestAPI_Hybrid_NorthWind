from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def convert_dict(entity):
    dict = {}
    for col in entity.__table__.columns:
        dict[col.name] = getattr(entity, col.name)
    return dict


#! customers
class Customers(db.Model):
    __tablename__ = "customers"
    CustomerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerName = db.Column(db.String, nullable=False)
    ContactName = db.Column(db.String)
    Address = db.Column(db.String)
    City = db.Column(db.String)
    PostalCode = db.Column(db.String)
    Country = db.Column(db.String)

    orders = db.relationship("Orders", backref="customers", lazy=True)


#! employeess
class Employees(db.Model):
    __tablename__ = "employees"
    EmployeeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    LastName = db.Column(db.String, nullable=False)
    FirstName = db.Column(db.String, nullable=False)
    BirthDate = db.Column(db.String)
    Photo = db.Column(db.String)
    Notes = db.Column(db.String)

    orders = db.relationship("Orders", backref="employees")


#! shippers
class Shippers(db.Model):
    __tablename__ = "shippers"
    ShipperID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ShipperName = db.Column(db.String, nullable=False)
    Phone = db.Column(db.String)

    orders = db.relationship("Orders", backref="shippers", lazy=True)


#! suppliers
class Suppliers(db.Model):
    __tablename__ = "suppliers"
    SupplierID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SupplierName = db.Column(db.String, nullable=True)
    ContactName = db.Column(db.String, nullable=True)
    Address = db.Column(db.String)
    City = db.Column(db.String)
    PostalCode = db.Column(db.String)
    Country = db.Column(db.String)
    Phone = db.Column(db.String)

    products_suppliers = db.relationship("Products", backref="suppliers", lazy=True)


#! categories
class Categories(db.Model):
    __tablename__ = "categories"
    CategoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CategoryName = db.Column(db.String, nullable=False)
    Description = db.Column(db.String)

    products_categories = db.relationship("Products", backref="categories", lazy=True)


#! orders
class Orders(db.Model):
    __tablename__ = "orders"
    OrderID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(
        db.Integer, db.ForeignKey("customers.CustomerID"), nullable=False
    )
    EmployeeID = db.Column(
        db.Integer, db.ForeignKey("employees.EmployeeID"), nullable=False
    )
    OrderDate = db.Column(db.String, nullable=False)
    ShipperID = db.Column(
        db.Integer, db.ForeignKey("shippers.ShipperID"), nullable=False
    )

    orderdetails = db.relationship("OrderDetails", backref="orders", lazy=True)


#! Products
class Products(db.Model):
    __tablename__ = "products"
    ProductID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProductName = db.Column(db.Integer, nullable=False)

    SupplierID = db.Column(
        db.Integer, db.ForeignKey("suppliers.SupplierID"), nullable=False
    )
    CategoryID = db.Column(
        db.Integer, db.ForeignKey("categories.CategoryID"), nullable=False
    )
    Unit = db.Column(db.String, nullable=False)
    Price = db.Column(db.Float, nullable=False)

    orderdetails = db.relationship("OrderDetails", backref="products", lazy=True)


#! OrderDetails
class OrderDetails(db.Model):
    __tablename__ = "orderdetails"
    OrderDetailID = db.Column(db.Integer, primary_key=True, nullable=False)
    OrderID = db.Column(db.Integer, db.ForeignKey("orders.OrderID"), nullable=False)
    ProductID = db.Column(
        db.Integer, db.ForeignKey("products.ProductID"), nullable=False
    )
    Quantity = db.Column(db.Integer, nullable=False)
