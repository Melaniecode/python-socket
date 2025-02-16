import socket
import select
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setblocking(False)  # 設定非阻塞
client.connect_ex(("127.0.0.1", 5555))  # 非阻塞連線，避免卡住

print("連線到伺服器成功，輸入訊息開始聊天 (輸入 'exit' 離開)")

while True:
    sockets_list = [sys.stdin, client]  # 監聽鍵盤輸入 & 伺服器訊息
    read_sockets, _, _ = select.select(sockets_list, [], [])

    for notified_socket in read_sockets:
        if notified_socket == client:
            try:
                message = client.recv(1024)
                if not message:
                    print("伺服器已斷線")
                    sys.exit()
                print("來自伺服器: " + message.decode())

            except BlockingIOError:
                pass

        else:
            message = sys.stdin.readline().strip()
            if message.lower() == "exit":
                print("關閉連線")
                client.close()
                sys.exit()
            client.send(message.encode())
