import getData
import functions

#! Customers
functions.add_customers_many(list=getData.get_list_objects("dataCustomer"))

#! Employees
functions.add_employees_many(list=getData.get_list_objects("dataEmployee"))

#! Shippers
functions.add_shippers_many(list=getData.get_list_objects("dataShipper"))

#! Suppliers
functions.add_suppliers_many(list=getData.get_list_objects("dataSupplier"))

#! Categories
functions.add_categories_many(list=getData.get_list_objects("dataCategory"))

#! Products
functions.add_products_many(list=getData.get_list_objects("dataProduct"))

#! Orders
functions.add_orders_many(list=getData.get_list_objects("dataOrder"))

#! Orders Detail
functions.add_orderdetails_many(list=getData.get_list_objects("dataOrderDetail"))
