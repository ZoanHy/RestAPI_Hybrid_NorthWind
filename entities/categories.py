from flask import Blueprint, jsonify, request
from database import Categories, db, convert_dict

categories = Blueprint(
    "categories", __name__, url_prefix="/api/v1/resources/categories"
)

#! GET
@categories.get("/get_all")
def get_all_categories():
    category_database = db.session.query(Categories).all()
    list_categories = [convert_dict(category) for category in category_database]
    return jsonify({"categories": list_categories})


@categories.get("/")
def get_customer_by_id():
    CategoryID = request.args.get("CategoryID")

    if not (CategoryID):
        return jsonify({"error": "empty param"})
    category = db.session.query(Categories).filter_by(CategoryID=CategoryID).first()
    return jsonify({"customer": convert_dict(category)})


#! POST
@categories.post("/add")
def add_a_supplier():
    new_category = Categories(
        CategoryName=request.form.get("CategoryName"),
        Description=request.form.get("Description"),
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify(response={"success": "Add successfully"})


#! PUT, PATCH
@categories.patch("/update/<int:category_id>")
@categories.put("/update/<int:category_id>")
def update_category(category_id):
    category = db.session.query(Categories).filter_by(CategoryID=category_id).first()
    if not category:
        return jsonify({"error: ": "not found category"}), 404

    if request.method == "PUT":
        if not (request.form.get("CategoryName") and request.form.get("Description")):
            return jsonify({"error": "not param"})

        category.CategoryName = request.form.get("CategoryName")
        category.Description = request.form.get("Description")

        db.session.commit()
        return jsonify(response={"success": "update successfullly"})
    else:
        check = False
        if request.form.get("CategoryName"):
            category.CategoryName = request.form.get("CategoryName")
            db.session.commit()
            check = True

        if request.form.get("Description"):
            category.Description = request.form.get("Description")
            db.session.commit()
            check = True

        if check == True:
            return jsonify(response={"success": "Update successfully"}), 200
        else:
            return jsonify(response={"error": "not param"}), 404


#! DELETE
