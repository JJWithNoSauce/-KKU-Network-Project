import socket
import select

HEADER_LENGTH = 10

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host_name = socket.gethostname()
IP = socket.gethostbyname(host_name)
PORT = 1234

server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]
serverUser = {
    'data':'Server'.encode('utf-8') ,
    'header': f"{len("Server"):<{HEADER_LENGTH}}".encode('utf-8')
}

clients = {}
history = []

print(f'Listening for connections on IP = {IP} at PORT = {PORT}')

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False

def broadcast(sender,messager):
    history.append({
        'sender':sender,
        'message':messager
    })
    
    for client_socket in clients:
        if client_socket != notified_socket:
            client_socket.send(
                sender['header'] + sender['data'] + messager['header'] + messager['data'])

def sendHistory(user):
    for log in history:
        sender = log['sender']
        message = log['message']
        
        user.send(sender['header'] + sender['data'] + message['header'] + message['data'])

while True:
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list)

    # Iterating over the notified sockets.
    for notified_socket in read_sockets:
        #If the notified socket is a server socket then we have a new connection, 
        # so add it using the accept() method.

        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(
                *client_address, user['data'].decode('utf-8')))
            
            joining = {
                'data':f'{user['data'].decode('utf-8')} has join.'.encode('utf-8') ,
                'header': f"{len(f'{user['data'].decode('utf-8')} has join.'):<{HEADER_LENGTH}}".encode('utf-8')
            }
            
            sendHistory(client_socket)
            broadcast(serverUser,joining)

        else:
            message = receive_message(notified_socket)

            # If no message is accepted then finish the connection.
            if message is False:
                print('Closed connection from: {}'.format(
                    clients[notified_socket]['data'].decode('utf-8')))

                # Removing the socket from the list 
                sockets_list.remove(notified_socket)
                del clients[notified_socket]

                continue

            # Getting the user by using the notified socket, so that the user can be identified.
            user = clients[notified_socket]

            print(
                f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Iterating over the connected clients and broadcasting the message.
            broadcast(user,message)

