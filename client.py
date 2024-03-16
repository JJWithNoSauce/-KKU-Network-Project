import socket
import sys
import errno
import asyncio
import aioconsole as aioconsole

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setblocking(False)

async def receive_messages(client_socket, my_username):
    while True:
        try:
            # Receive messages from the server
            username_header = await loop.sock_recv(client_socket, HEADER_LENGTH)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = await loop.sock_recv(client_socket, username_length)
            username = username.decode('utf-8')

            message_header = await loop.sock_recv(client_socket, HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = await loop.sock_recv(client_socket, message_length)
            message = message.decode('utf-8')

            if username != my_username:
                print()
            print(f'{username} > {message}')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            continue

        except Exception as e:
            print('Reading error: '.format(str(e)))
            sys.exit()


async def send_message(client_socket):
    while True:
        message = await aioconsole.ainput()
        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            await loop.sock_sendall(client_socket, message_header + message)

async def main():
    ip = await aioconsole.ainput("Enter chatroom ip to join : ")
    if ip : IP = ip
    
    my_username = await aioconsole.ainput("Username: ")
    await loop.sock_connect(client_socket, (IP, PORT))

    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

    await loop.sock_sendall(client_socket, username_header + username)

    receive_task = asyncio.create_task(receive_messages(client_socket, my_username))
    send_task = asyncio.create_task(send_message(client_socket))
    await asyncio.gather(receive_task, send_task)

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
except KeyboardInterrupt:
    print("KeyboardInterrupt: Closing client connection.")
    client_socket.close()
