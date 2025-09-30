import socket
import random
import hashlib
import crypto_utils

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_prime(size):
    """Generate a random prime number with a specified number of bits."""
    while True:
        n = random.getrandbits(size)
        if is_prime(n):
            return n

def rsa_gen(size = 2048):
    """Generate an RSA key pair with a specified number of bits."""
    p = generate_prime(size // 2)
    q = generate_prime(size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)
    return (n, d), (n, e)

def rsa_encrypt(p, k):
    return pow(p, k[1]) % k[0]

def rsa_decrypt(c, k):
    return pow(c, k[1]) % k[0]

def sha1(data):
    return hashlib.sha1(data).digest()

def hmac(key, message):
    # Handle different types of key input
    if isinstance(key, int):
        key = str(key)
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # Handle different types of message input  
    if isinstance(message, int):
        message = str(message)
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    block_size = 64
    
    if len(key) > block_size:
        key = sha1(key)
    
    if len(key) < block_size:
        key = key + b'\x00' * (block_size - len(key))

    o_key_pad = bytes((x ^ 0x5c) for x in key)
    i_key_pad = bytes((x ^ 0x36) for x in key)

    inner_hash = sha1(i_key_pad + message)
    outer_hash = sha1(o_key_pad + inner_hash).hex()
    
    return outer_hash


def ssl_handshake_client(client_sock, HOST, PORT):
    client_sock.connect((HOST, PORT))

    #1.1:Sending "I'm alive" message to server
    client_hello = "SDES-SHA1"
    client_sock.send(client_hello.encode())

    #2.1 Receive public key and information from server
    server_hello = client_sock.recv(1024).decode()

    #2.2 Verify Certificate from server

    #3.1 Create own keys, encrypt with server public key, and send to server
    client_private_key, client_public_key = rsa_gen(16)
    sent_key = f"{client_public_key[0]}|{client_public_key[1]}"
    client_sock.send(sent_key.encode())

    # 4.2 Receive shared secret
    encrypted_shared_secret = int(client_sock.recv(1024).decode())
    shared_secret = rsa_decrypt(encrypted_shared_secret, client_private_key)

    return shared_secret

def ssl_handshake_server(server_sock, HOST, PORT):
    server_sock.bind((HOST, PORT))
    server_sock.listen(1)
    print(f"Bank server listening on {HOST}:{PORT}")

    client_sock, client_address = server_sock.accept()
    print(f"Client connected: {client_address}")

    #1.2:Receives "I'm alive message" from client
    client_hello = client_sock.recv(1024).decode()
    print("Cient hello received")

    #1.3 Sends server public key and decyrption
    server_hello = f"SDES-SHA1"
    client_sock.send(server_hello.encode())
    print("Server hello sent")

    #3.2 Receive public key from client and d
    formatted_public_key = client_sock.recv(1024).decode().split("|")
    client_public_key = (int(formatted_public_key[0]), int(formatted_public_key[1]))
    print("Public key received")

    # 4.1 Define shared secret as the key from Simple DES
    shared_secret = random.getrandbits(10)
    client_sock.send(str(rsa_encrypt(shared_secret, client_public_key)).encode())
    print("Shared secret sent")

    return client_sock, shared_secret
