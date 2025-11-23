import rsa

def sign_file(data, private_key):
    return rsa.sign(data, private_key, "SHA-256")

def verify_signature(data, signature, public_key):
    try:
        rsa.verify(data, signature, public_key)
        return True
    except:
        return False