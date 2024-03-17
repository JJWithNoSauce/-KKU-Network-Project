import socket
import sys
import errno
import asyncio
import aioconsole as aioconsole

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

# สร้าง socket object สำหรับ client และตั้งค่าเป็น non-blocking mode
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setblocking(False)

# รับข้อความจากเซิร์ฟเวอร์
async def receive_messages(client_socket, my_username):
    while True:
        try:
            # รับข้อความเกี่ยวกับชื่อผู้ใช้และข้อความ
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

             # แสดงข้อความที่รับได้บนหน้าจอ
            if username != my_username:
                print()
            print(f'{username} > {message}')

        except IOError as e:
            # จัดการข้อผิดพลาดที่เกิดขึ้นในการอ่านข้อมูล
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            continue

        except Exception as e:
            print('Reading error: '.format(str(e)))
            sys.exit()


# ส่งข้อความไปยังเซิร์ฟเวอร์
async def send_message(client_socket):
    while True:
        # รับข้อความจากผู้ใช้
        message = await aioconsole.ainput()
        
        # ส่งข้อความผ่าน socket
        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            await loop.sock_sendall(client_socket, message_header + message)



async def main():
    # รับ IP ของเซิร์ฟเวอร์
    ip = await aioconsole.ainput("Enter chatroom ip to join : ")
    if ip : IP = ip
    
    # รับ username และเชื่อมต่อ
    my_username = await aioconsole.ainput("Username: ")
    await loop.sock_connect(client_socket, (IP, PORT))

    # ส่งข้อมูล user ไปยังเซิร์ฟเวอร์
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    await loop.sock_sendall(client_socket, username_header + username)

    # เริ่มต้นการรับและส่งข้อความ
    receive_task = asyncio.create_task(receive_messages(client_socket, my_username))
    send_task = asyncio.create_task(send_message(client_socket))
    await asyncio.gather(receive_task, send_task)

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
except KeyboardInterrupt:
    print("KeyboardInterrupt: Closing client connection.")
    client_socket.close()
