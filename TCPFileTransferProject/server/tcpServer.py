import socket
import os.path

def tcp_server():
    continue_looping = True
    while continue_looping:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_number = input("Enter a port number: ")

        if not str(port_number).isdigit():
            print("Invalid port number. Must be a number.")
            continue
        try:
            print("Starting server at port: " + port_number)
            my_socket.bind(('', int(port_number)))
            my_socket.listen(10)
            continue_looping = False
        except IOError as ioe:
            if ioe.errno == 13:
                print("You do not have permission to use that port number")
                continue
            else:
                print("The following error was found: " + str(ioe))
                continue
        except ValueError as ve:
            print("There was an issue with the entered port number: " + str(ve))
            continue

    while True:
        try:
            while True:
                print("Waiting for connection")
                connection, client_address = my_socket.accept()
                print("Client has been connected")

                stay_connected_and_try_again = True
                while stay_connected_and_try_again:
                    received_data = connection.recv(4096)
                    received_data = received_data.decode("utf-8")
                    if received_data:
                        print("Client has requested the following file: "
                              + received_data)

                        if not os.path.isfile(received_data):
                            print(received_data
                                  + " was not found. \nAlerting client."
                                    " \nWaiting for new request")
                            failure_notice = received_data + " does not exist."
                            connection.sendall(failure_notice.encode("utf-8"))
                        else:
                            stay_connected_and_try_again = False
                file = open(received_data, 'rb')
                outgoing_data = file.read(1024)
                while outgoing_data:
                    print("Sending file please wait...")
                    connection.sendall(outgoing_data)
                    outgoing_data = file.read(1024)
                connection.shutdown(socket.SHUT_WR)
                file.close()
                print("File was sent!")
        except IOError as ioe:
            print("The following error was found: " + str(ioe))
            continue
    return

def tcp_server_thread:



