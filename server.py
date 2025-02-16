import socket
import threading

# 用來儲存所有連線的客戶端
clients = []

# 客戶端名稱
client_names = {}

# 處理每個客戶端連線的函式
def handle_client(client_socket, addr):
    client_socket.send("請輸入您的名稱: ".encode('utf-8'))
    name = client_socket.recv(1024).decode('utf-8')
    client_names[client_socket] = name
    print(f"新連線: {name} ({addr})")
    broadcast(f"{name} 加入聊天室!".encode('utf-8'), client_socket)

    # 持續接收訊息並轉發
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"{name}: {message.decode('utf-8')}")
            broadcast(f"{name}: {message.decode('utf-8')}".encode('utf-8'), client_socket)
        except:
            break

    print(f"{name} 斷線")
    clients.remove(client_socket)
    del client_names[client_socket]
    broadcast(f"{name} 離開聊天室!".encode('utf-8'), client_socket)
    client_socket.close()

# 廣播訊息給所有客戶端
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close() # 若發送失敗（如客戶端斷線），則關閉該連線
                clients.remove(client)

# 建立socket後綁定
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5555))

server.listen(5)
print("server已啟動，等待client端連線...")

# 接受連線並處理
while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
