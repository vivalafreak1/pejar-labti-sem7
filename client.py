import socket
import os
 
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6000
BUFFER_SIZE = 4096
 
def receive_file(conn, filename):
    with open(filename, "wb") as f:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            f.write(data)
    conn.close()
 
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"[*] Connected to {SERVER_HOST}:{SERVER_PORT}")
    filename = input("[+] Enter filename: ")
    client_socket.send(filename.encode())
    response = client_socket.recv(BUFFER_SIZE).decode()
    if response == "OK":
        filesize = int(client_socket.recv(BUFFER_SIZE).decode())
        print(f"[-] File size: {filesize} bytes.")
        client_socket.send(b"OK")
        receive_file(client_socket, filename)
        print(f"[-] {filename} received successfully.")
    else:
        print(f"[!] {filename} does not exist on the server.")
    client_socket.close()
 
if __name__ == "__main__":
    main()
