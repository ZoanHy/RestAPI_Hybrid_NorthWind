from flask import Blueprint, jsonify, request
from database import Suppliers, db, convert_dict

suppliers = Blueprint("suppliers", __name__, url_prefix="/api/v1/resources/suppliers")

#! GET
@suppliers.get("/get_all")
def get_all_suppliers():
    supplier_database = db.session.query(Suppliers).all()
    list_suppliers = [convert_dict(supplier) for supplier in supplier_database]
    return jsonify({"suppliers": list_suppliers})


@suppliers.get("/")
def get_employee_by_id():
    SupplierID = request.args.get("SupplierID")
    if not (SupplierID):
        return jsonify({"error": "empty param"})
    supplier = db.session.query(Suppliers).filter_by(SupplierID=SupplierID).first()
    return jsonify({"suppliers": convert_dict(supplier)})


#! POST
@suppliers.post("/add")
def add_a_supplier():
    new_supplier = Suppliers(
        SupplierName=request.form.get("SupplierName"),
        ContactName=request.form.get("ContactName"),
        Address=request.form.get("Address"),
        City=request.form.get("City"),
        PostalCode=request.form.get("PostalCode"),
        Country=request.form.get("Country"),
        Phone=request.form.get("Phone"),
    )
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify(response={"success": "Add successfully"})


#! PUT, PATCH
@suppliers.patch("/update/<int:supplier_id>")
@suppliers.put("/update/<int:supplier_id>")
def update_supplier(supplier_id):
    supplier = db.session.query(Suppliers).filter_by(SupplierID=supplier_id).first()
    if not supplier:
        return jsonify({"error: ": "not found supplier"}), 404

    if request.method == "PUT":
        if not (
            request.form.get("SupplierName")
            and request.form.get("ContactName")
            and request.form.get("Address")
            and request.form.get("City")
            and request.form.get("PostalCode")
            and request.form.get("Country")
            and request.form.get("Phone")
        ):
            return jsonify({"error": "not param"})

        supplier.SupplierName = request.form.get("SupplierName")
        supplier.ContactName = request.form.get("ContactName")
        supplier.Address = request.form.get("Address")
        supplier.City = request.form.get("City")
        supplier.PostalCode = request.form.get("PostalCode")
        supplier.Country = request.form.get("Country")
        supplier.Phone = request.form.get("Phone")

        db.session.commit()
        return jsonify(response={"success": "update successfullly"})
    else:
        check = False
        if request.form.get("SupplierName"):
            supplier.SupplierName = request.form.get("SupplierName")
            db.session.commit()
            check = True

        if request.form.get("ContactName"):
            supplier.ContactName = request.form.get("ContactName")
            db.session.commit()
            check = True
        if request.form.get("Address"):
            supplier.Address = request.form.get("Address")
            db.session.commit()
            check = True

        if request.form.get("City"):
            supplier.City = request.form.get("City")
            db.session.commit()
            check = True
        if request.form.get("PostalCode"):
            supplier.PostalCode = request.form.get("PostalCode")
            db.session.commit()
            check = True

        if request.form.get("Country"):
            supplier.Country = request.form.get("Country")
            db.session.commit()
            check = True
        if request.form.get("Phone"):
            supplier.Phone = request.form.get("Phone")
            db.session.commit()
            check = True

        if check == True:
            return jsonify(response={"success": "Update successfully"}), 200
        else:
            return jsonify(response={"error": "not param"}), 404


#! DELETE
