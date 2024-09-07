__author__ = 'ModifiedAuthor'

import socket
import SQL_ORM as orm
import protocol as proto
import threading
from tcp_by_size import send_with_size, recv_by_size

shutdown_flag = False

def client_handler(client_socket, thread_id, db):
    global shutdown_flag
    
    print(f"Client #{thread_id} connected.")
    
    while not shutdown_flag:
        try:
            request = recv_by_size(client_socket)
            if not request:
                print("Client disconnected.")
                break
            
            response = handle_client_action(request.decode(), db)
            send_with_size(client_socket, response)

        except socket.error as err:
            print(f"Socket error {err}. Client disconnected.")
            break

        except Exception as e:
            print(f"Error occurred: {e}")
            break
    client_socket.close()

def handle_client_action(client_data, db):
    """
    Process client request and return the appropriate server response.
    """
    response_message = "Not Set"
    action = client_data[:6]
    data = client_data[7:]
    parameters = data.split('~')

    if action == proto.CREATE_ORDER_REQUEST:
        order_obj = orm.Order(parameters[0].split(','), parameters[1], parameters[2])
        if db.create_order(order_obj):
            response_message = proto.create_server_response("create order", "success")
        else:
            response_message = proto.create_server_response("create order", "failure")

    elif action == proto.INSERT_CUSTOMER_REQUEST:
        customer_obj = orm.Customer(parameters[0], parameters[1], parameters[2], parameters[3])
        if db.insert_customer(customer_obj):
            response_message = proto.create_server_response("insert customer", "success")
        else:
            response_message = proto.create_server_response("insert customer", "failure")

    # Add remaining cases here based on original actions
    return response_message

def main_server():
    global shutdown_flag
    
    db_handler = orm.OrdersCustomersORM()
    
    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", 33445))
    server_socket.listen(4)
    print("listening.....")

    threads = []
    client_id = 1
    while True:
        client_conn, addr = server_socket.accept()
        thread = threading.Thread(target=client_handler, args=(client_conn, client_id, db_handler))
        thread.start()
        client_id += 1
        threads.append(thread)
        if shutdown_flag:
            break


    for thread in threads:
        thread.join()
    
    server_socket.close()

main_server()
