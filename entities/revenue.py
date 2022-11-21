from flask import Blueprint, jsonify, request
from database import Suppliers, db, convert_dict, Categories, Orders

revenue = Blueprint("revenue", __name__, url_prefix="/api/v1/resources/revenue")

#! GET
@revenue.get("/start_end_year")
def calculate_revenue_per_year():
    start_year = request.args.get("start_year")
    end_year = request.args.get("end_year")
    if start_year is None or end_year is None:
        return jsonify({"error": "year empty"}), 404

    if int(start_year) > int(end_year):
        return jsonify({"error": "year not valid"}), 404

    query = """
    SELECT SUM(Total) as Tong FROM (
    SELECT SUM(od.Quantity * p.Price) as Total, strftime('%Y', o.OrderDate) as ByYear FROM orderdetails od 
    Join orders o on od.OrderID = o.OrderID 
    JOIN products p on p.ProductID = od.ProductID 
    GROUP BY od.OrderID 
    HAVING CAST(ByYear as int) BETWEEN :s AND :e
    )
    """
    result = db.engine.execute(query, s=start_year, e=end_year)
    total_revenue = [row[0] for row in result][0]
    return jsonify({"Total Revenue": total_revenue})


@revenue.get("/supplier/<int:SupplierID>")
def calculate_revenue_supplier_by_id(SupplierID):

    if SupplierID is None:
        return jsonify({"error": "not param"})

    supplier = db.session.query(Suppliers).filter_by(SupplierID=SupplierID).first()

    if supplier is None:
        return jsonify({"error": "not found supplier"})

    query = """
    SELECT SUM(p.Unit * p.Price) as ToTal FROM orderdetails od 
    join products p on od.ProductID = p.ProductID 
    WHERE p.SupplierID = :id
    """

    result = db.engine.execute(query, id=SupplierID)
    total_revenue = [row[0] for row in result][0]
    return jsonify({"Total Revenue": total_revenue})


@revenue.get("/supplier")
def calculate_revenue_per_supplier():
    query = """
    SELECT p.SupplierID , s.SupplierName  ,SUM(p.Price * od.Quantity) as Total FROM orderdetails od
    join products p on p.ProductID = od.ProductID 
    JOIN suppliers s on s.SupplierID = p.SupplierID 
    GROUP BY p.SupplierID , s.SupplierName 
    """
    result = db.engine.execute(query)
    list_supplier = [row for row in result]
    list_dict = []
    if len(list_supplier) == 0:
        return jsonify({"Total Revenue": "empty"})

    for i in range(len(list_supplier)):
        supplier = list_supplier[i]
        list_dict.append(
            {
                "SupplierID": supplier[0],
                "SupplierName": supplier[1],
                "Total": supplier[2],
            }
        )
    return jsonify({"Total Revenue": list_dict})


@revenue.get("/category/<int:CategoryID>")
def calculate_revenue_category_by_id(CategoryID):

    if CategoryID is None:
        return jsonify({"error": "not param"})

    category = db.session.query(Categories).filter_by(CategoryID=CategoryID).first()

    if category is None:
        return jsonify({"error": "not found category"})

    query = """
        SELECT SUM(p.Price * od.Quantity) as Total  FROM orderdetails od
        join products p on p.ProductID = od.ProductID 
        WHERE p.CategoryID = :id
    """
    result = db.engine.execute(query, id=CategoryID)
    total_revenue = [row[0] for row in result][0]
    return jsonify({"Total Revenue": total_revenue})


@revenue.get("/category")
def calculate_revenue_per_category():
    query = """
    SELECT p.CategoryID  , c.CategoryName  , SUM(p.Price * od.Quantity) as Total FROM orderdetails od
    join products p on p.ProductID = od.ProductID 
    JOIN categories c  on c.CategoryID = p.CategoryID 
    GROUP BY c.CategoryID , c.CategoryName 
    """
    result = db.engine.execute(query)
    list_category = [row for row in result]
    list_dict = []
    if len(list_category) == 0:
        return jsonify({"Total Revenue": "empty"})

    for i in range(len(list_category)):
        category = list_category[i]
        list_dict.append(
            {
                "CategoryID": category[0],
                "CategoryName": category[1],
                "Total": category[2],
            }
        )
    return jsonify({"Total Revenue": list_dict})


@revenue.get("/order/<int:OrderID>")
def calculate_total_price_order_by_id(OrderID):
    if OrderID is None:
        return jsonify({"error": "not param"})

    order = db.session.query(Orders).filter_by(OrderID=OrderID).first()

    if order is None:
        return jsonify({"error": "not found order"})

    query = """
    SELECT SUM(p.Price * od.Quantity) as Total FROM orderdetails od
    join orders o on o.OrderID = od.OrderID 
    JOIN products p on p.ProductID = od.ProductID
    where o.OrderID = :id
    """
    result = db.engine.execute(query, id=OrderID)
    total_revenue = [row[0] for row in result][0]
    return jsonify({"Total Revenue": total_revenue})


@revenue.get("/order")
def calculate_revenue_per_order():
    query = """
    SELECT o.OrderID , SUM(p.Price * od.Quantity) as Total FROM orderdetails od
    join orders o on o.OrderID = od.OrderID 
    JOIN products p on p.ProductID = od.ProductID
    GROUP BY o.OrderID 
    """
    result = db.engine.execute(query)
    list_order = [row for row in result]
    list_dict = []
    if len(list_order) == 0:
        return jsonify({"Total Revenue": "empty"})

    for i in range(len(list_order)):
        order = list_order[i]
        list_dict.append(
            {
                "OrderID": order[0],
                "Total": order[1],
            }
        )
    return jsonify({"Total Revenue": list_dict})
