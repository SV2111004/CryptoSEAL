import socket, rsa, pickle
from crypto_module import verify_signature

HOST = "127.0.0.1"
PORT = 5051

public_key = rsa.PublicKey.load_pkcs1(open("keys/public.pem","rb").read())

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

print("✅ Receiver Server Running... Waiting for file...")

while True:
    conn, addr = server.accept()
    data = pickle.loads(conn.recv(4096))

    file_bytes = data["file"]
    signature = data["signature"]

    verified = verify_signature(file_bytes, signature, public_key)

    if verified:
        conn.send(b" Signature Verified: File is Authentic!")
        print("✅ Verified Successfully")
    else:
        conn.send(b" Signature Invalid: File Tampered!")
        print("❌ Verification Failed")

    conn.close()