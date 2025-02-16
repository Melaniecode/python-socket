import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)  # 設定為非阻塞
server.bind(("0.0.0.0", 5555))
server.listen()

sockets_list = [server]  # 追蹤所有的 socket 連線
clients = {}  # 追蹤客戶端 {socket: addr}

print("伺服器啟動，等待連線...")

while True:
    # 使用 select 檢測可讀的 socket
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        # 有新客戶端連線
        if notified_socket == server:
            client_socket, client_address = server.accept()
            client_socket.setblocking(False)  # 設定新連線為非阻塞
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"新客戶端連線: {client_address}")

        # 接收客戶端的訊息
        else:
            try:
                message = notified_socket.recv(1024)
                if not message:
                    print(f"客戶端 {clients[notified_socket]} 斷線")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue

                print(f"收到來自 {clients[notified_socket]} 的訊息: {message.decode()}")
                
                # 廣播訊息給其他客戶端
                for client in clients:
                    if client != notified_socket:
                        client.send(message)

            except BlockingIOError:
                pass

    # 移除發生異常的 socket
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
