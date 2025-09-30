import socket
import ssl_ctx_rev
import crypto_utils

HOST = '127.0.0.1'
PORT = 8000

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        shared_secret = ssl_ctx_rev.ssl_handshake_client(client_socket, HOST, PORT)

        while True:
            print("1) Deposit\n2) Withdraw\n3) Balance\n4) Quit")
            choice = input("Enter your choice (1-4): ")

            match choice:
                case "1":
                    account = input("Please enter your account number: ")
                    amount = input("Enter deposit amount: ")
                    message = f"D {account} {amount}"
                case "2":
                    account = input("Please enter your account number: ")
                    amount = input("Enter withdrawal amount: ")
                    pin = input("Enter PIN: ")
                    message = f"W {account} {pin} {amount}"
                case "3":
                    account = input("Please enter your account number: ")
                    pin = input("Enter PIN: ")
                    message = f"B {account} {pin}"
                case "4":
                    print("Goodbye!")
                    break
                case _:
                    print("Invalid choice; try again")
                    continue

            # Convert shared_secret to 10-bit binary string
            sdes_key = format(shared_secret, '010b')
            
            hmac_value = ssl_ctx_rev.hmac(message, str(shared_secret))
            full_message = f"{message} | {hmac_value}"
            
            encrypted_message = crypto_utils.encrypt(full_message, sdes_key)
            client_socket.send(encrypted_message.encode())

            encrypted_response = client_socket.recv(1024).decode().strip()
            decrypted_data = crypto_utils.decrypt(encrypted_response, sdes_key)
            
            if ' | ' not in decrypted_data:
                print("Error: Malformed response")
                continue
            
            response, received_hmac = decrypted_data.split(' | ', 1)

            if received_hmac != ssl_ctx_rev.hmac(response, str(shared_secret)):
                print("Response corrupted; please try again")
            else:
                print(response)