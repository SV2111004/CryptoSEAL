import socket, pickle

HOST = "127.0.0.1"
PORT = 5051

def send_file(file_bytes, signature):
    try:
        sock = socket.socket()
        sock.connect((HOST, PORT))

        data = pickle.dumps({"file": file_bytes, "signature": signature})
        sock.send(data)

        msg = sock.recv(1024).decode()
        sock.close()
        return msg
    
    except Exception as e:
        return f"❌ Failed: {e}"