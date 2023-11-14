import socket 
import threading  
import os 
 
SERVER_HOST = "0.0.0.0" 
SERVER_PORT = 6000
BUFFER_SIZE = 4096
 
def send_file(conn, addr, filename):
    filesize = os.path.getsize(filename)
    conn.send(str(filesize).encode())
    response = conn.recv(BUFFER_SIZE)
    if response == b"OK":
        with open(filename, "rb") as f:
            data = f.read(BUFFER_SIZE)
            while data:
                conn.send(data)
                data = f.read(BUFFER_SIZE)
    conn.close()
 
def wait_for_connection(server_socket):
    while True:
        conn, addr = server_socket.accept()
        print(f"[+] {addr[0]}:{addr[1]} is connected.")
        filename = conn.recv(BUFFER_SIZE).decode()
        print(f"[-] {filename} is requested by {addr[0]}:{addr[1]}.")
        if os.path.exists(filename):
            conn.send(b"OK")
            t = threading.Thread(target=send_file, args=(conn, addr, filename))
            t.start()
        else:
            conn.send(b"ERR")
            conn.close()
 
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")
    wait_for_connection(server_socket)
 
if __name__ == "__main__":
    main()
