import socket
import os

import s_des

# Generate RSA key pair
def generate_key_pair():
    # Generate a new RSA key pair with a key size of 2048 bits
    key_pair = RSA.generate(2048)
    
    # Extract the private key and public key from the key pair
    private_key = key_pair.export_key()  # Export the private key
    public_key = key_pair.publickey().export_key()  # Export the public key
    
    return private_key, public_key

def rsa_encrypt(plain_text, public_key):
    # Import the public key
    key = RSA.import_key(public_key)
    
    # Create a cipher object
    cipher = PKCS1_OAEP.new(key)
    
    # Encrypt the plaintext
    cipher_text = cipher.encrypt(plain_text.encode())
    
    return cipher_text

def rsa_decrypt(cipher_text, private_key):
    # Import the private key
    key = RSA.import_key(private_key)
    
    # Create a cipher object
    cipher = PKCS1_OAEP.new(key)
    
    # Decrypt the ciphertext
    decrypted_text = cipher.decrypt(cipher_text)
    
    return decrypted_text.decode()

def sha1(data):
    return hashlib.sha1(data).digest()

# Generate HMAC using SHA256
def generate_hmac(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()
    

def ssl_handshake_client(client_sock, HOST, PORT):
    client_sock.connect((HOST, PORT))

    #1.1:Sending "I'm alive" message to server 
    client_hello = "SDES-SHA1"
    client_sock.send(client_hello.encode())

    #2.1 Receive public key and information from server
    server_hello = client_socket.recv(1024).decode()

    #2.2 Verify Certificate from server

    #3.1 Create own keys, encrypt with server public key, and send to server
    client_private_key, client_public_key = rsa_gen()
    client_sock.send(client_public_key.encode())

    # 4.2 Receive shared secret
    encrypted_shared_secret = client_sock.recv(1024).decode()
    shared_secret = rsa_decrypt(encrypted_shared_secret, client_private_key)

    return shared_secret

def ssl_handshake_server(server_sock):
    server_sock.bind((HOST, PORT))
    server_sock.listen(1)
    print(f"Bank server listening on {HOST}:{PORT}")

    client_sock, client_address = server_sock.accept()
    print(f"Client connected: {client_address}")

    #1.2:Receives "I'm alive message" from client 
    client_hello = client_sock.recv(1024).decode()

    #1.3 Sends server public key and decyrption
    server_hello = f"SDES-SHA1"
    client_sock.send(server_hello.encode())

    #3.2 Receive public key from client and d
    client_public_key = client_sock.recv(1024).decode()
    
    # 4.1 Define shared secret as the key from Simple DES
    client_sock.send(rsa_encrypt(shared_secret, client_public_key).encode())

    return client_sock, shared_secret