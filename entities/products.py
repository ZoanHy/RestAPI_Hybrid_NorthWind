from flask import Blueprint, jsonify, request
from database import Products, db, convert_dict

products = Blueprint("products", __name__, url_prefix="/api/v1/resources/products")

#! GET
@products.get("/get_all")
def get_all_suppliers():
    query = """
    SELECT p.ProductID , p.ProductName , s.SupplierName , c.CategoryName , p.Unit , p.Price  FROM products p 
    join suppliers s on s.SupplierID = p.SupplierID 
    JOIN categories c on c.CategoryID = p.CategoryID 
    """
    result = db.engine.execute(query)
    list_product = [row for row in result]
    list_dict = []
    if len(list_product) == 0:
        return jsonify({"products": "empty"})

    for i in range(len(list_product)):
        product = list_product[i]
        list_dict.append(
            {
                "ProductID": product[0],
                "ProductName": product[1],
                "SupplierName": product[2],
                "CategoryName": product[3],
                "Unit": product[4],
                "Price": product[5],
            }
        )
    return jsonify({"products": list_dict})


@products.get("/")
def get_product_by_id():
    ProductID = request.args.get("ProductID")
    if not ProductID:
        return jsonify({"error": "not param"})

    query = """
    SELECT p.ProductID , p.ProductName , s.SupplierName , c.CategoryName , p.Unit , p.Price  FROM products p 
    join suppliers s on s.SupplierID = p.SupplierID 
    JOIN categories c on c.CategoryID = p.CategoryID 
    WHERE p.ProductID = :id
    """
    result = db.engine.execute(query, id=ProductID)
    prodcut_found = [row for row in result]

    for row in result:
        for i in range(len(row)):
            prodcut_found.append(row[i])

    if not prodcut_found:
        return jsonify({"error": "not found"})

    product_dict = {
        "ProductID": prodcut_found[0][0],
        "ProductName": prodcut_found[0][1],
        "SupplierName": prodcut_found[0][2],
        "CategoryName": prodcut_found[0][3],
        "Unit": prodcut_found[0][4],
        "Price": prodcut_found[0][5],
    }

    return jsonify({"products": product_dict})


#! POST
@products.post("/add")
def add_a_product():
    new_product = Products(
        SupplierID=request.form.get("SupplierID"),
        ProductName=request.form.get("ProductName"),
        CategoryID=request.form.get("CategoryID"),
        Unit=request.form.get("Unit"),
        Price=request.form.get("Price"),
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(response={"success": "Add successfully"})


#! PUT, PATCH
@products.patch("/update/<int:product_id>")
@products.put("/update/<int:product_id>")
def update_product(product_id):
    product = db.session.query(Products).filter_by(ProductID=product_id).first()
    if not product:
        return jsonify({"error: ": "not found product"}), 404

    if request.method == "PUT":
        if not (
            request.form.get("ProductName")
            and request.form.get("SupplierID")
            and request.form.get("CategoryID")
            and request.form.get("Unit")
            and request.form.get("Price")
        ):
            return jsonify({"error": "not param"})

        product.ProductName = request.form.get("ProductName")
        product.SupplierID = request.form.get("SupplierID")
        product.CategoryID = request.form.get("CategoryID")
        product.Unit = request.form.get("Unit")
        product.Price = request.form.get("Price")

        db.session.commit()
        return jsonify(response={"success": "update successfullly"})
    else:
        check = False
        if request.form.get("ProductName"):
            product.ProductName = request.form.get("ProductName")
            db.session.commit()
            check = True

        if request.form.get("SupplierID"):
            product.SupplierID = request.form.get("SupplierID")
            db.session.commit()
            check = True
        if request.form.get("CategoryID"):
            product.CategoryID = request.form.get("CategoryID")
            db.session.commit()
            check = True

        if request.form.get("Unit"):
            product.Unit = request.form.get("Unit")
            db.session.commit()
            check = True
        if request.form.get("Price"):
            product.Price = request.form.get("Price")
            db.session.commit()
            check = True

        if check == True:
            return jsonify(response={"success": "Update successfully"}), 200
        else:
            return jsonify(response={"error": "not param"}), 404


#! DELETE
