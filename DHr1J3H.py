import socket

import ssl_ctx
import s_des

HOST = '127.0.0.1'
PORT = 8000

accounts = {
    '123456789': {
        'pin': '1234',
        'balance': 1000
    },
    '987654321': {
        'pin': '4321',
        'balance': 500
    }
}

# Bank server logic
def handle_request(client_socket, shared_secret):
    # Receive request from the client
    encrypted_request = client_socket.recv(1024).decode().strip()
    request, hmac = s_des.decrypt(encrypted_request, shared_secret).split(' | ')

    if hmac != ssl_ctx.hmac(request, shared_secret):
        response = "Message corrupted; please try again"

    elif request.startswith('D'):
        # Parse deposit request
        _, account_number, amount = request.split()
        amount = float(amount)

        # Update account balance
        accounts[account_number]['balance'] += amount

        # Send response to the client
        response = f"Deposited {amount} to account {account_number}"

    elif request.startswith('W'):
        # Parse withdrawal request
        _, account_number, pin, amount = request.split()
        amount = float(amount)

        # Verify PIN
        if accounts[account_number]['pin'] == pin:
            # Check if sufficient balance
            if accounts[account_number]['balance'] >= amount:
                # Update account balance
                accounts[account_number]['balance'] -= amount

                # Send response to the client
                response = f"Withdrew {amount} from account {account_number}"
            else:
                response = "Insufficient balance"
        else:
            response = "Invalid PIN"

    elif request.startswith('B'):
        # Parse balance request
        _, account_number, pin = request.split()

        # Verify PIN
        if accounts[account_number]['pin'] == pin:
            # Send account balance to the client
            response = f"Balance of account {account_number}: {accounts[account_number]['balance']}"
        else:
            response = "Invalid PIN"

    else:
        response = "Invalid request"

    encrypted_message = s_des.encrypt(f"{response} | {ssl_ctx.hmac(response, shared_secret)}", shared_secret)
    client_socket.send(encrypted_message.encode())

    return

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        client_socket, shared_secret = ssl_ctx.ssl_handshake_server(server_socket, HOST, PORT)

        while True:
            handle_request(client_socket, shared_secret)
