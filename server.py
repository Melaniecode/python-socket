import socket

# 1. 創建一個 socket，這是商店的電話
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 把電話號碼（IP 和端口）綁定到商店
server_socket.bind(('localhost', 6666))

# 3. 開始等待來自顧客的電話
server_socket.listen(5)

print("Server is listening for connections...")

# 4. 接聽顧客來的電話
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# 5. 接收顧客的要求
data = client_socket.recv(1024)
print(f"Received from client: {data.decode()}")

# 6. 回應顧客
client_socket.sendall(b'Hello, Client!')

# 7. 結束通話
client_socket.close()
