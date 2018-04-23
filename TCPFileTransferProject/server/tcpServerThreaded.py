import socket
import os
import os.path
import threading

#
#	Project 1; A simple TCP server with threading. 
#	Charles Billingsley
#

class TcpServer(object):
    def __init__(self, port_number):
        self.port_number = port_number
        self.my_socket = socket.socket(socket.AF_INET,
                                       socket.SOCK_STREAM)
        self.all_threads = []
        while True:
            try:
                self.my_socket.bind(('', int(self.port_number)))
                break
            except IOError as ioe:
                if ioe.errno == 13:
                    print("You do not have permission to use that port number")
                    self.port_number = input("Please enter a port number: ")
                    continue
                else:
                    print("The following error was found: " + str(ioe))
                    self.port_number = input("Please enter a port number: ")
                    continue
            except ValueError as ve:
                print("There was an issue with the entered port number: "
                      + str(ve))
                self.port_number = input("Please enter a port number: ")
                continue

    def listen(self):
        self.my_socket.listen(10)
        while True:
            print("Waiting for connection")
            connection, client_address = self.my_socket.accept()
            print("Client has been connected")
            current_thread = threading.Thread(target=self.get_client_data,
                                              args=(
                                              connection, client_address))
            self.all_threads.append(current_thread)
            current_thread.start()

            for thread in self.all_threads:
                if not thread.isAlive():
                    self.all_threads.remove(thread)
                    thread.join()


    def get_client_data(self, connection, client_address):
        should_exit = False
        while not should_exit:
            try:
                stay_connected_and_try_again = True
                while stay_connected_and_try_again:
                    received_data = connection.recv(4096)
                    received_data = received_data.decode("utf-8")
                    if received_data:
                        if received_data == "files":
                            available_files = [file
                                               for file in os.listdir(".")
                                               if os.path.isfile(file)
                                               and ".py" not in file
                                               ]
                            files_to_send = "\n".join(available_files)
                            print("Client has requested a list of files.")
                            print("Sending list of available files.")
                            connection.sendall(files_to_send.encode("utf-8"))
                        elif received_data == "exit":
                            print("A client has disconnected.")
                            should_exit = True
                            break
                        else:
                            print("Client has requested the following file: "
                                  + received_data)

                            if not os.path.isfile(received_data):
                                print(received_data
                                      + " was not found. \nAlerting client."
                                        " \nWaiting for new request")
                                failure_notice = received_data + " does not " \
                                                                 "exist."
                                connection.sendall(
                                    failure_notice.encode("utf-8"))
                            else:
                                stay_connected_and_try_again = False
                if should_exit:
                    connection.shutdown(socket.SHUT_WR)
                    break
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
                #print("The following error was found: " + str(ioe))
                continue


if __name__ == "__main__":
    while True:
        port = input("Enter a port number: ")
        if not str(port).isdigit():
            print("Invalid port number. Must be a digit.")
            continue
        else:
            break
    server = TcpServer(port)
    server.listen()
