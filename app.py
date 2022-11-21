from flask import Flask
from database import db
from entities.customers import customers
from entities.employees import employees
from entities.shippers import shippers
from entities.orders import orders
from entities.orderdetails import orderdetails
from entities.suppliers import suppliers
from entities.categories import categories
from entities.products import products
from entities.revenue import revenue
import os


def create_app():

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    )

    db.init_app(app)

    app.register_blueprint(customers)
    app.register_blueprint(employees)
    app.register_blueprint(shippers)
    app.register_blueprint(orders)
    app.register_blueprint(orderdetails)
    app.register_blueprint(suppliers)
    app.register_blueprint(categories)
    app.register_blueprint(products)
    app.register_blueprint(revenue)

    @app.route("/")
    def home():
        # with app.app_context():
        #     db.create_all()
        return "<h1 style='text-align:center;'>Welcome to NorthWind API</h1>"

    return app
