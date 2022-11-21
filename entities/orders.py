from flask import Blueprint, jsonify, request
from database import Orders, db, convert_dict
from datetime import datetime

orders = Blueprint("orders", __name__, url_prefix="/api/v1/resources/orders")

#! GET
@orders.get("/get_all")
def get_all_orders():
    query = """
    SELECT c.CustomerName ,  e.LastName || ' ' || e.FirstName as EmployeeName, o.OrderDate , o.OrderID , s.ShipperName  FROM orders o 
    join customers c on c.CustomerID = o.CustomerID 
    join employees e on e.EmployeeID = o.EmployeeID 
    JOIN shippers s on s.ShipperID = o.ShipperID 
    """
    result = db.engine.execute(query)
    list_order = [row for row in result]
    list_dict = []
    if len(list_order) == 0:
        return jsonify({"orders": "empty"})

    for i in range(len(list_order)):
        order = list_order[i]
        list_dict.append(
            {
                "CustomerName": order[0],
                "EmployeeName": order[1],
                "OrderDate": order[2],
                "OrderID": order[3],
                "ShipperName": order[4],
            }
        )

    return jsonify({"orders": list_dict})


@orders.get("/")
def get_order_by_id():
    OrderID = request.args.get("OrderID")
    if not OrderID:
        return jsonify({"error": "not param"})

    query = """
    SELECT c.CustomerName ,  e.LastName || ' ' || e.FirstName as EmployeeName, o.OrderDate , o.OrderID , s.ShipperName  FROM orders o 
    join customers c on c.CustomerID = o.CustomerID 
    join employees e on e.EmployeeID = o.EmployeeID 
    JOIN shippers s on s.ShipperID = o.ShipperID 
    WHERE o.OrderID = :id
    """
    result = db.engine.execute(query, id=OrderID)
    order_found = [row for row in result]

    for row in result:
        for i in range(len(row)):
            order_found.append(row[i])

    if not order_found:
        return jsonify({"error": "not found"})

    order_dict = {
        "CustomerName": order_found[0][0],
        "EmployeeName": order_found[0][1],
        "OrderDate": order_found[0][2],
        "OrderID": order_found[0][3],
        "ShipperName": order_found[0][4],
    }

    return jsonify({"orders": order_dict})


#! POST
@orders.post("/add")
def add_a_order():
    now = datetime.now()
    new_order = Orders(
        CustomerID=request.form.get("CustomerID"),
        EmployeeID=request.form.get("EmployeeID"),
        ShipperID=request.form.get("ShipperID"),
        OrderDate=now.strftime("%Y-%m-%d"),
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(response={"success": "Add successfully"})


#! PUT, PATCH
@orders.patch("/update/<int:order_id>")
@orders.put("/update/<int:order_id>")
def update_order(order_id):
    order = db.session.query(Orders).filter_by(OrderID=order_id).first()
    if not order:
        return jsonify({"error: ": "not found order"}), 404

    if request.method == "PUT":
        if not (
            request.form.get("CustomerID")
            and request.form.get("EmployeeID")
            and request.form.get("OrderDate")
            and request.form.get("ShipperID")
        ):
            return jsonify({"error": "not param"})

        order.CustomerID = request.form.get("CustomerID")
        order.EmployeeID = request.form.get("EmployeeID")
        order.OrderDate = request.form.get("OrderDate")
        order.ShipperID = request.form.get("ShipperID")
        db.session.commit()
        return jsonify(response={"success": "update successfullly"})
    else:
        check = False
        if request.form.get("CustomerID"):
            order.ShipperName = request.form.get("CustomerID")
            db.session.commit()
            check = True

        if request.form.get("EmployeeID"):
            order.EmployeeID = request.form.get("EmployeeID")
            db.session.commit()
            check = True
        if request.form.get("OrderDate"):
            order.OrderDate = request.form.get("OrderDate")
            db.session.commit()
            check = True
        if request.form.get("ShipperID"):
            order.ShipperID = request.form.get("ShipperID")
            db.session.commit()
            check = True

        if check == True:
            return jsonify(response={"success": "Update successfully"}), 200
        else:
            return jsonify(response={"error": "not param"}), 404


#! DELETE
