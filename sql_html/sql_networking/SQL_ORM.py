import sqlite3
import pickle

DB_PATH = 'data.db'
ORDERS_TABLE = 'orders'
CUSTOMERS_TABLE = 'customers'
MENU_TABLE = 'menu'

def pickle_data(rows, columns):
    return pickle.dumps((pickle.dumps(rows), pickle.dumps(columns)))

class Order:
    def __init__(self, items_list, customer_id, payment_method):
        self.items = items_list
        self.customer_id = customer_id
        self.payment_method = payment_method
        self.total = 0
        self.order_id = None

class Customer:
    def __init__(self, first_name, last_name, phone_number, email):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.customer_id = None

class OrdersCustomersORM:
    def __init__(self):
        pass

    def open_db(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def get_all_orders(self):
        self.open_db()
        query = f"SELECT * FROM {ORDERS_TABLE}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        data = pickle_data(result, columns)
        self.close_db()
        return data

    def get_order_by_name(self, first_name, last_name):
        self.open_db()
        id_query = f"SELECT id FROM {CUSTOMERS_TABLE} WHERE first_name = '{first_name}' AND surname = '{last_name}'"
        self.cursor.execute(id_query)
        customer_ids = [item[0] for item in self.cursor.fetchall()]
        orders = []
        for cust_id in customer_ids:
            order_query = f"SELECT * FROM {ORDERS_TABLE} WHERE customer_id = {cust_id}"
            self.cursor.execute(order_query)
            orders.extend(self.cursor.fetchall())
        columns = [desc[0] for desc in self.cursor.description]
        data = pickle_data(orders, columns)
        self.close_db()
        return data

    def get_order_by_id(self, order_id):
        self.open_db()
        query = f"SELECT * FROM {ORDERS_TABLE} WHERE id = {order_id}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        data = pickle_data(result, columns)
        self.close_db()
        return data

    # Other methods for menu, top orders, etc.

    def create_order(self, order):
        self.open_db()
        self.cursor.execute(f"SELECT MAX(id) FROM {ORDERS_TABLE}")
        try:
            new_order_id = self.cursor.fetchone()[0] + 1
        except:
            new_order_id = 1
        order.total = sum([self.get_item_price(item) for item in order.items])
        insert_query = f"INSERT INTO {ORDERS_TABLE} (id, items, customer_id, total, payment_method) VALUES ({new_order_id}, '{', '.join(order.items)}', {order.customer_id}, {order.total}, '{order.payment_method}')"
        self.cursor.execute(insert_query)
        self.commit()
        self.close_db()
        return True

    def get_item_price(self, item):
        query = f"SELECT price FROM {MENU_TABLE} WHERE item = '{item}'"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def insert_customer(self, customer):
        self.open_db()
        self.cursor.execute(f"SELECT MAX(id) FROM {CUSTOMERS_TABLE}")
        try:
            new_customer_id = self.cursor.fetchone()[0] + 1
        except:
            new_customer_id = 1
        insert_query = f"INSERT INTO {CUSTOMERS_TABLE} (id, first_name, surname, phone_num, email) VALUES ({new_customer_id}, '{customer.first_name}', '{customer.last_name}', '{customer.phone_number}', '{customer.email}')"
        self.cursor.execute(insert_query)
        self.commit()
        self.close_db()
        return True

