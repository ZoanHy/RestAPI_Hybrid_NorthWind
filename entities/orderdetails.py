from flask import Blueprint, jsonify, request
from database import OrderDetails, db, convert_dict

orderdetails = Blueprint(
    "orderdetails", __name__, url_prefix="/api/v1/resources/orderdetails"
)

#! GET
@orderdetails.get("/get_all")
def get_all_orderdetails():
    query = """
    SELECT od.OrderDetailID , c.CustomerName , e.LastName || ' ' || e.FirstName as EmployeeName, s.ShipperName  , p.ProductName , od.Quantity , p.Unit , p.Price, o.OrderDate  FROM orderdetails od
    join orders o on od.OrderID = o.OrderID 
    join products p on p.ProductID = od.ProductID
    JOIN customers c on o.CustomerID = c.CustomerID 
    JOIN employees e on e.EmployeeID = o.EmployeeID 
    JOIN shippers s on s.ShipperID = o.ShipperID 
    """
    result = db.engine.execute(query)
    list_orderdetail = [row for row in result]
    list_dict = []
    if len(list_orderdetail) == 0:
        return jsonify({"orders": "empty"})

    for i in range(len(list_orderdetail)):
        orderdetail = list_orderdetail[i]
        list_dict.append(
            {
                "OrderDetailID": orderdetail[0],
                "CustomerName": orderdetail[1],
                "EmployeeName": orderdetail[2],
                "ShipperName": orderdetail[3],
                "ProductName": orderdetail[4],
                "Quantity": orderdetail[5],
                "Unit": orderdetail[6],
                "Price": orderdetail[7],
                "OrderDate": orderdetail[8],
            }
        )

    return jsonify({"orderdetails": list_dict})


@orderdetails.get("/")
def get_orderdetail_by_id():
    OrderDetailID = request.args.get("OrderDetailID")
    if not OrderDetailID:
        return jsonify({"error": "not param"})

    query = """
    SELECT od.OrderDetailID , c.CustomerName , e.LastName || ' ' || e.FirstName as EmployeeName, s.ShipperName  , p.ProductName , od.Quantity , p.Unit , p.Price, o.OrderDate  FROM orderdetails od
    join orders o on od.OrderID = o.OrderID 
    join products p on p.ProductID = od.ProductID
    JOIN customers c on o.CustomerID = c.CustomerID 
    JOIN employees e on e.EmployeeID = o.EmployeeID 
    JOIN shippers s on s.ShipperID = o.ShipperID 
    WHERE od.OrderDetailID = :id
    """
    result = db.engine.execute(query, id=OrderDetailID)
    orderdetail_found = [row for row in result]

    for row in result:
        for i in range(len(row)):
            orderdetail_found.append(row[i])

    if not orderdetail_found:
        return jsonify({"error": "not found"})

    orderdetail_dict = {
        "OrderDetailID": orderdetail_found[0][0],
        "CustomerName": orderdetail_found[0][1],
        "EmployeeName": orderdetail_found[0][2],
        "ShipperName": orderdetail_found[0][3],
        "ProductName": orderdetail_found[0][4],
        "Quantity": orderdetail_found[0][5],
        "Unit": orderdetail_found[0][6],
        "Price": orderdetail_found[0][7],
        "OrderDate": orderdetail_found[0][8],
    }
    return jsonify({"orderdetails": orderdetail_dict})


#! POST


@orderdetails.post("/add")
def add_a_orderdetail():
    new_orderdetail = OrderDetails(
        OrderID=request.form.get("OrderID"),
        ProductID=request.form.get("ProductID"),
        Quantity=request.form.get("Quantity"),
    )
    db.session.add(new_orderdetail)
    db.session.commit()
    return jsonify(response={"success": "Add successfully"})


#! PUT, PATCH
@orderdetails.patch("/update/<int:orderdetail_id>")
@orderdetails.put("/update/<int:orderdetail_id>")
def update_(orderdetail_id):
    orderdetail = (
        db.session.query(OrderDetails).filter_by(OrderDetailID=orderdetail_id).first()
    )
    if not orderdetail:
        return jsonify({"error: ": "not found orderdetail"}), 404

    if request.method == "PUT":
        if not (
            request.form.get("OrderID")
            and request.form.get("ProductID")
            and request.form.get("Quantity")
        ):
            return jsonify({"error": "not param"})

        orderdetail.OrderID = request.form.get("OrderID")
        orderdetail.ProductID = request.form.get("ProductID")
        orderdetail.Quantity = request.form.get("Quantity")

        db.session.commit()
        return jsonify(response={"success": "update successfullly"})
    else:
        check = False
        if request.form.get("OrderID"):
            orderdetail.OrderID = request.form.get("OrderID")
            db.session.commit()
            check = True

        if request.form.get("ProductID"):
            orderdetail.ProductID = request.form.get("ProductID")
            db.session.commit()
            check = True

        if request.form.get("Quantity"):
            orderdetail.Quantity = request.form.get("Quantity")
            db.session.commit()
            check = True

        if check == True:
            return jsonify(response={"success": "Update successfully"}), 200
        else:
            return jsonify(response={"error": "not param"}), 404


#! DELETE
