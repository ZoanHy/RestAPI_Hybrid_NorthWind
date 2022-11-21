from flask import Blueprint, jsonify, request
from database import Shippers, db, convert_dict

shippers = Blueprint("shippers", __name__, url_prefix="/api/v1/resources/shippers")

#! GET
@shippers.get("/get_all")
def get_all_shippers():
    shipper_database = db.session.query(Shippers).all()
    list_shippers = [convert_dict(shipper) for shipper in shipper_database]
    return jsonify({"shippers": list_shippers})


@shippers.get("/")
def get_employee_by_id():
    ShipperID = request.args.get("ShipperID")

    if not (ShipperID):
        return jsonify({"error": "empty param"})
    shipper = db.session.query(Shippers).filter_by(ShipperID=ShipperID).first()
    return jsonify({"shippers": convert_dict(shipper)})


#! POST
@shippers.post("/add")
def add_a_shipper():
    new_shipper = Shippers(
        ShipperName=request.form.get("ShipperName"), Phone=request.form.get("Phone")
    )
    db.session.add(new_shipper)
    db.session.commit()
    return jsonify(response={"success": "Add successfully"})


#! PUT, PATCH
@shippers.patch("/update/<int:shipper_id>")
@shippers.put("/update/<int:shipper_id>")
def update_shipper(shipper_id):
    shipper = db.session.query(Shippers).filter_by(ShipperID=shipper_id).first()
    if not shipper:
        return jsonify({"error: ": "not found shipper"}), 404

    if request.method == "PUT":
        if not (request.form.get("ShipperName") and request.form.get("Phone")):
            return jsonify({"error": "not param"})

        shipper.ShipperName = request.form.get("ShipperName")
        shipper.Phone = request.form.get("Phone")

        db.session.commit()
        return jsonify(response={"success": "update successfullly"})
    else:
        check = False
        if request.form.get("ShipperName"):
            shipper.ShipperName = request.form.get("ShipperName")
            db.session.commit()
            check = True

        if request.form.get("Phone"):
            shipper.Phone = request.form.get("Phone")
            db.session.commit()
            check = True

        if check == True:
            return jsonify(response={"success": "Update successfully"}), 200
        else:
            return jsonify(response={"error": "not param"}), 404


#! DELETE
