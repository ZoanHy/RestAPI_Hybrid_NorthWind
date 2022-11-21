from flask import Blueprint, jsonify, request
from database import Employees, db, convert_dict

employees = Blueprint("employees", __name__, url_prefix="/api/v1/resources/employees")

#! GET
@employees.get("/get_all")
def get_all_employees():
    employee_database = db.session.query(Employees).all()
    list_employees = [convert_dict(employee) for employee in employee_database]
    return jsonify({"employees": list_employees})


@employees.get("/")
def get_employee_by_id():
    EmployeeID = request.args.get("EmployeeID")

    if not (EmployeeID):
        return jsonify({"error": "empty param"})
    employee = db.session.query(Employees).filter_by(EmployeeID=EmployeeID).first()
    return jsonify({"employees": convert_dict(employee)})


#! POST


@employees.post("/add")
def add_a_employee():
    new_employee = Employees(
        LastName=request.form.get("LastName"),
        FirstName=request.form.get("FirstName"),
        BirthDate=request.form.get("BirthDate"),
        Photo=request.form.get("Photo"),
        Notes=request.form.get("Notes"),
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify(response={"success": "Add successfully"})


#! PUT, PATCH
@employees.patch("/update/<int:employee_id>")
@employees.put("/update/<int:employee_id>")
def update_employee(employee_id):
    employee = db.session.query(Employees).filter_by(EmployeeID=employee_id).first()
    if not employee:
        return jsonify({"error: ": "not found employee"}), 404

    if request.method == "PUT":
        if not (
            request.form.get("LastName")
            and request.form.get("FirstName")
            and request.form.get("BirthDate")
            and request.form.get("Photo")
            and request.form.get("Notes")
        ):
            return jsonify({"error": "not param"})
        employee.LastName = request.form.get("LastName")
        employee.FirstName = request.form.get("FirstName")
        employee.BirthDate = request.form.get("BirthDate")
        employee.Photo = request.form.get("Photo")
        employee.Notes = request.form.get("Notes")
        db.session.commit()
        return jsonify(response={"success": "update successfullly"})
    else:
        check = False
        if request.form.get("LastName"):
            employee.LastName = request.form.get("LastName")
            db.session.commit()
            check = True

        if request.form.get("FirstName"):
            employee.FirstName = request.form.get("FirstName")
            db.session.commit()
            check = True

        if request.form.get("BirthDate"):
            employee.BirthDate = request.form.get("BirthDate")
            db.session.commit()
            check = True

        if request.form.get("Photo"):
            employee.Photo = request.form.get("Photo")
            db.session.commit()
            check = True

        if request.form.get("Notes"):
            employee.Notes = request.form.get("Notes")
            db.session.commit()
            check = True

        if check == True:
            return jsonify(response={"success": "Update successfully"}), 200
        else:
            return jsonify(reponse={"error": "not param"}), 404


#! DELETE
