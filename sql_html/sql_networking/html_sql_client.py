__author__ = 'ModifiedAuthor'

import socket
import threading
from tcp_by_size import send_with_size, recv_by_size
import protocol as proto
import pickle
import table_viewer

ORDER_RECORDS = 'order_data'
CUSTOMER_RECORDS = 'customer_data'

def process_server_reply(reply):
    code = reply[:7]

    if type(code) != str:
        code = code.decode()

    payload = reply[8:]
    try:
        fields = payload.split('~')
    except:
        fields = payload.split(b'~')

    if code in [proto.GET_ORDER_RESPONSE, proto.GET_ORDERS_RESPONSE]:
        content = pickle.loads(fields[0])
        table_viewer.data_to_html(pickle.loads(content[0]), pickle.loads(content[1]), ORDER_RECORDS)

    elif code in [proto.GET_MENU_RESPONSE, proto.INSERT_TO_MENU_RESPONSE, proto.EDIT_MENU_RESPONSE]:
        content = pickle.loads(fields[0])
        table_viewer.data_to_html(pickle.loads(content[0]), pickle.loads(content[1]), 'menu')

    elif code == proto.GET_EXP_ORDERS_RESPONSE:
        content = pickle.loads(fields[0])
        table_viewer.data_to_html(pickle.loads(content[0]), pickle.loads(content[1]), 'Top Orders')

    elif code == proto.GET_CUS_ID_RESPONSE:
        content = pickle.loads(fields[0])
        table_viewer.data_to_html(pickle.loads(content[0]), pickle.loads(content[1]), 'Customer Search')

def show_menu():
    print(f"1. Create New Order\n"
          f"2. Add New Customer\n"
          f"3. Find Orders by Customer Name\n"
          f"4. Find Order by Order ID\n"
          f"5. Fetch All Orders\n"
          f"6. View Menu\n"
          f"7. Add Item to Menu\n"
          f"8. View Top 5 Orders by Price\n"
          f"9. Fetch Customer ID by Phone\n"
          f"10. Update Menu Item Price\n"
          f"15. Exit\n\n>")

    selection = input("Choose Option > ")

    if selection == "15":
        return "exit"

    elif selection == "1":
        items = input("Enter items (comma-separated) > ").replace(' ', '')
        customer_id = input("Enter Customer ID > ")
        payment_method = input("Enter Payment Method > ")
        return proto.create_client_request('create order', items, customer_id, payment_method)

    elif selection == "2":
        first_name = input("First Name > ")
        last_name = input("Last Name > ")
        phone = input("Phone Number > ")
        email = input("Email > ")
        return proto.create_client_request("insert customer", first_name, last_name, phone, email)

    elif selection == "3":
        first_name = input("Enter First Name > ")
        last_name = input("Enter Last Name > ")
        return proto.create_client_request("get order", first_name, last_name)

    elif selection == "4":
        order_id = input("Enter Order ID > ")
        return proto.create_client_request("get order", order_id)

    elif selection == "5":
        return proto.create_client_request("get orders")

    elif selection == "6":
        return proto.create_client_request("get menu")

    elif selection == "7":
        item_data = input("Enter items and price (item:price, comma-separated) > ").replace(' ', '')
        return proto.create_client_request("menu add", item_data)

    elif selection == "8":
        return proto.create_client_request("pricey orders")

    elif selection == "9":
        phone = input("Enter Customer Phone Number > ")
        return proto.create_client_request("get cus id", phone)

    elif selection == "10":
        item_name = input("Enter Item Name > ")
        new_price = input("Enter New Price > ")
        return proto.create_client_request("edit menu", item_name, new_price)

    else:
        return "invalid"

client_socket = socket.socket()
client_socket.connect(("127.0.0.1", 33445))

while True:
    client_data = show_menu()

    if client_data == "exit":
        break
    send_with_size(client_socket, client_data)

    response = recv_by_size(client_socket)
    if not response:
        print("Server Disconnected")
        break
    print(f"Response Received: {response}")
    process_server_reply(response)
