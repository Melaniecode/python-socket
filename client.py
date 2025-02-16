import socket
import threading

# 接收訊息的函式
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            print(message.decode('utf-8'))
        except:
            print("無法接收訊息")
            break

# 發送訊息的函式
def send_messages(client_socket):
    while True:
        message = input("")
        client_socket.send(message.encode('utf-8'))

# 建立socket後連線
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))

# 啟動接收訊息的線程
receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()


# 啟動發送訊息的線程
send_thread = threading.Thread(target=send_messages, args=(client,))
send_thread.start()
