import socket

# 1. 創建一個 socket，這是用來發送和接收資料的網路「電話」
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 連接到伺服器，這是「撥打」連接到伺服器的電話號碼
client_socket.connect(('localhost', 6666))

# 3. 向伺服器發送一個訊息
client_socket.sendall(b'Hello, Server!')

# 4. 接收伺服器的回應，這就像你聽到商店的回應
response = client_socket.recv(1024)
print(f"Server response: {response.decode()}")

# 5. 結束這個網路通話
client_socket.close()
