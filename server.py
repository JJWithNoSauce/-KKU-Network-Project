import socket
import select

HEADER_LENGTH = 10

# สร้าง socket object สำหรับ server และกำหนดค่า
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# รับชื่อโฮสต์และ IP address ของเครื่องเซิร์ฟเวอร์
host_name = socket.gethostname()
IP = socket.gethostbyname(host_name)
PORT = 1234

# ผูก server socket กับ IP address และ port
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]

# สร้างข้อมูลสำหรับเก็บข้อมูลของเซิร์ฟเวอร์
serverUser = {
    'data':'Server'.encode('utf-8') ,
    'header': f"{len("Server"):<{HEADER_LENGTH}}".encode('utf-8')
}

# เก็บข้อมูลของผู้ใช้ที่เชื่อมต่อและประวัติข้อความที่ถูกส่ง
clients = {}
history = []

print(f'Listening for Client join on IP = {IP} at PORT = {PORT}')

# ฟังก์ชันรับข้อความจาก client
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False

# ฟังก์ชันส่งข้อความไปยังทุก client
def broadcast(sender,messager):
    history.append({
        'sender':sender,
        'message':messager
    })
    
    for client_socket in clients:
        if client_socket != notified_socket:
            client_socket.send(
                sender['header'] + sender['data'] + messager['header'] + messager['data'])

#ส่งประวัติข้อความไปยัง client ที่เพิ่ง join
def sendHistory(user):
    for log in history:
        sender = log['sender']
        message = log['message']
        
        user.send(sender['header'] + sender['data'] + message['header'] + message['data'])





while True:
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list)

    # วนลูปตรวจสอบ socket ที่ได้รับการแจ้งเตือน
    for notified_socket in read_sockets:
        # ถ้าเป็นserver socket แสดงว่ามีการเชื่อมต่อใหม่เข้ามา
        if notified_socket == server_socket:
            # รับข้อมูลของ client ใหม่ที่เชื่อมต่อเข้ามา
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            
            # เพิ่ม client ใหม่ลงในระบบ
            sockets_list.append(client_socket)
            clients[client_socket] = user
            
            print('Accepted new connection from {}:{}, username: {}'.format(
                *client_address, user['data'].decode('utf-8')))
            
            joining = {
                'data':f'{user['data'].decode('utf-8')} has join.'.encode('utf-8') ,
                'header': f"{len(f'{user['data'].decode('utf-8')} has join.'):<{HEADER_LENGTH}}".encode('utf-8')
            }
            
            # ส่งประวัติให้ client ใหม่และบอกทุก client ถึงการเข้ามา
            sendHistory(client_socket)
            broadcast(serverUser,joining)

        else:
         # ถ้าไม่ใช่ server socket ก็แสดงว่าเป็นข้อความ 
            message = receive_message(notified_socket)
            
             # ถ้า client disconnet ลบclients ออกจากระบบ
            if message is False:
                print('Closed connection from: {}'.format(
                    clients[notified_socket]['data'].decode('utf-8')))

                sockets_list.remove(notified_socket)
                del clients[notified_socket]

                continue
            user = clients[notified_socket]

            print(
                f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # ส่งข้อความไปยังทุกๆ client
            broadcast(user,message)

