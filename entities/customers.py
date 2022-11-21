from flask import Blueprint, jsonify, request
from database import Customers, db, convert_dict


customers = Blueprint("customers", __name__, url_prefix="/api/v1/resources/customers")

#! GET


@customers.get("/get_all")
def get_all_customers():
    customer_database = db.session.query(Customers).all()
    list_customers = [convert_dict(customer) for customer in customer_database]
    return jsonify({"customers": list_customers})


@customers.get("/")
def get_customer_by_id():
    CustomerID = request.args.get("CustomerID")

    if not (CustomerID):
        return jsonify({"error": "empty param"})
    customer = db.session.query(Customers).filter_by(CustomerID=CustomerID).first()
    return jsonify({"customer": convert_dict(customer)})


#! POST


@customers.post("/add")
def add_a_customer():
    new_customer = Customers(
        CustomerName=request.form.get("CustomerName"),
        ContactName=request.form.get("ContactName"),
        Address=request.form.get("Address"),
        City=request.form.get("City"),
        PostalCode=request.form.get("PostalCode"),
        Country=request.form.get("Country"),
    )

    db.session.add(new_customer)
    db.session.commit()
    return jsonify(response={"success": "Add successfully"})


#! PUT, PATCH


@customers.patch("/update/<int:customer_id>")
@customers.put("/update/<int:customer_id>")
def update_customer(customer_id):
    customer = db.session.query(Customers).filter_by(CustomerID=customer_id).first()
    if not customer:
        return jsonify({"error: ": "not found customer"}), 404

    if request.method == "PUT":
        if not (
            request.form.get("CustomerName")
            and request.form.get("ContactName")
            and request.form.get("Address")
            and request.form.get("City")
            and request.form.get("PostalCode")
            and request.form.get("Country")
        ):
            return jsonify({"error": "not param"})
        customer.CustomerName = request.form.get("CustomerName")
        customer.ContactName = request.form.get("ContactName")
        customer.Address = request.form.get("Address")
        customer.City = request.form.get("City")
        customer.PostalCode = request.form.get("PostalCode")
        customer.Country = request.form.get("Country")
        db.session.commit()
        return jsonify(response={"success": "update successfullly"})
    else:
        check = False
        if request.form.get("CustomerName"):
            customer.CustomerName = request.form.get("CustomerName")
            db.session.commit()
            check = True

        if request.form.get("ContactName"):
            customer.ContactName = request.form.get("ContactName")
            db.session.commit()
            check = True

        if request.form.get("Address"):
            customer.Address = request.form.get("Address")
            db.session.commit()
            check = True

        if request.form.get("City"):
            customer.City = request.form.get("City")
            db.session.commit()
            check = True

        if request.form.get("PostalCode"):
            customer.PostalCode = request.form.get("PostalCode")
            db.session.commit()
            check = True

        if request.form.get("Country"):
            customer.Country = request.form.get("Country")
            db.session.commit()
            check = True

        if check == True:
            return jsonify(response={"success": "Update successfully"}), 200
        else:
            return jsonify(response={"error": "not param"}), 404


#! DELETE


@customers.delete("/delete/<int:customer_id>")
def delete_a_customer(customer_id):
    customer = db.session.query(Customers).get(customer_id)
    if customer:
        # customer.
        db.session.commit()
        return jsonify(response={"success": "Delete successfully"})
    else:
        return jsonify(errors={"Not found": "ID incorect"})
