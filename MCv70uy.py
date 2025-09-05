import socket

import ssl_ctx
import s_des

HOST = '127.0.0.1'
PORT = 8000

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        shared_secret = ssl_ctx.ssl_handshake_client(client_socket, HOST, PORT)

        while True:
            print("1) Deposit\n2) Withdraw\n3) Balance\n4) Quit")

            choice = input("Enter your choice (1-4): ")

            match choice:
                case 1:
                    account = input("Please enter your account number")
                    amount = input("Enter deposit amount: ")
                    message = f"D {account} {amount}"
                case 2:
                    account = input("Please enter your account number")
                    amount = input("Enter deposit amount: ")
                    pin = input("Enter PIN: ")
                    message = f"W {account} {pin} {amount}"
                case 3:
                    account = input("Please enter your account number")
                    pin = input("Enter PIN: ")
                    message = f"B {account} {pin}"
                case 4:
                    print("Goodbye!")
                    break
                case _:
                    print("Invalid choice; try again")

            encrypted_message = s_des.encrypt(f"{message} | {ssl_ctx.hmac(message, shared_secret)}", shared_secret)
            client_socket.send(encrypted_message.encode())

            encrypted_request = client_socket.recv(1024).decode().strip()
            response, hmac = s_des.decrypt(encrypted_request, shared_secret).split(' | ')

            if hmac != ssl_ctx.hmac(response, shared_secret):
                print("Response corrupted; please try again")
            else:
                print(response)
