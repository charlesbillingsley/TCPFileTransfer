import socket
import ipaddress
import sys

#
#	Project 1; A simple TCP client. 
#	Charles Billingsley
#

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connection_Successful = False
while not connection_Successful:
    server_Address = input("Enter an ip address: ")
    received_Valid_Address = False
    while not received_Valid_Address:
        try:
            ipaddress.ip_address(server_Address)
            received_Valid_Address = True
        except ValueError:
            server_Address = input("Invalid ip address. Try again: ")
            received_Valid_Address = False

    received_Valid_PortNumber = False
    port_Number = input("Enter a port number: ")
    while not received_Valid_PortNumber:
        if not port_Number.isdigit():
            port_Number = input("Invalid port number. Try again: ")
        else:
            received_Valid_PortNumber = True

    complete_Address = (server_Address, int(port_Number))
    connection_Result = my_socket.connect_ex(complete_Address)
    if connection_Result != 0:
        print("Connection failed. Please double check the following: ")
        print("1. Be sure the entered ip address is valid")
        print("2. Be sure the entered port number is valid")
        print("3. Be sure the server is started")
        print("Starting over...")
    else:
        print("Port opened")
        connection_Successful = True

should_exit = False
while not should_exit:
    try:
        files_requested = False
        file_Found = False
        while not file_Found:
            valid_Filename_Entered = False
            requested_File = input("Please enter a file name and extention, "
                                   "\"files\", or \"exit\": ")
            while not valid_Filename_Entered and not files_requested:
                if "." not in requested_File:
                    if requested_File == "files":
                        files_requested = True
                    elif requested_File == "exit":
                        should_exit = True
                        break
                    else:
                        requested_File = input(
                            "Filename must have extention. Try again: ")
                else:
                    valid_Filename_Entered = True
            if should_exit:
                print("disconnecting from server.")
            else:
                print("sending request for " + requested_File)
            my_socket.sendall(requested_File.encode("utf-8"))
            if should_exit:
                break
            received_data = my_socket.recv(1024)
            try:
                if "does not exist." in received_data.decode("utf-8"):
                    print(received_data.decode("utf-8"))
                else:
                    print("File(s) found.")
                    file_Found = True
                    continue
            except UnicodeDecodeError as ude:
                print("File(s) found.")
                file_Found = True
                continue
        if should_exit:
            break
        if not files_requested:
            file = open(requested_File, 'wb')
            i = 0
            while received_data:
                print("Receiving file. Please wait..." + str(i))
                i = i+1
                file.write(received_data)
                received_data = my_socket.recv(1024)
            file.close()
            print("File has been received!")
        else:
            print("\nAvailable files on server: ")
            print(received_data.decode("utf-8"))
            print("\n")
    except IOError as ioe:
        print("The following error was found: " + str(ioe))

print("closing socket")
my_socket.close()
