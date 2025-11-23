import rsa
import os

def generate_keys():
    public_key, private_key = rsa.newkeys(2048)

    if not os.path.exists("keys"):
        os.makedirs("keys")

    with open("keys/private.pem", "wb") as f:
        f.write(private_key.save_pkcs1())

    with open("keys/public.pem", "wb") as f:
        f.write(public_key.save_pkcs1())

    return private_key, public_key

def load_keys():
    with open("keys/private.pem", "rb") as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read())
    with open("keys/public.pem", "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    return private_key, public_key