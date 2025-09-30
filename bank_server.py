import socket
import ssl_ctx_rev
import crypto_utils

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
    # Convert shared_secret to 10-bit binary string for S-DES
    sdes_key = format(shared_secret, '010b')
    
    # Receive request from the client
    encrypted_request = client_socket.recv(1024).decode().strip()
    decrypted_data = crypto_utils.decrypt(encrypted_request, sdes_key)
    request, hmac_received = decrypted_data.split(' | ')

    if hmac_received != ssl_ctx_rev.hmac(request, str(shared_secret)):
        response = "Message corrupted; please try again"

    elif request.startswith('D'):
        # Parse deposit request
        _, account_number, amount = request.split()
        amount = float(amount)

        # Update account balance
        if account_number in accounts:
            accounts[account_number]['balance'] += amount
            response = f"Deposited {amount} to account {account_number}. New balance: {accounts[account_number]['balance']}"
        else:
            response = "Account not found"

    elif request.startswith('W'):
        # Parse withdrawal request
        _, account_number, pin, amount = request.split()
        amount = float(amount)

        # Verify PIN and account
        if account_number in accounts:
            if accounts[account_number]['pin'] == pin:
                # Check if sufficient balance
                if accounts[account_number]['balance'] >= amount:
                    # Update account balance
                    accounts[account_number]['balance'] -= amount
                    response = f"Withdrew {amount} from account {account_number}. New balance: {accounts[account_number]['balance']}"
                else:
                    response = "Insufficient balance"
            else:
                response = "Invalid PIN"
        else:
            response = "Account not found"

    elif request.startswith('B'):
        # Parse balance request
        _, account_number, pin = request.split()

        # Verify PIN and account
        if account_number in accounts:
            if accounts[account_number]['pin'] == pin:
                response = f"Balance of account {account_number}: {accounts[account_number]['balance']}"
            else:
                response = "Invalid PIN"
        else:
            response = "Account not found"

    else:
        response = "Invalid request"

    encrypted_message = crypto_utils.encrypt(f"{response} | {ssl_ctx_rev.hmac(response, str(shared_secret))}", sdes_key)
    client_socket.send(encrypted_message.encode())

    return

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Add socket reuse option (but don't bind here - let ssl_handshake_server do it)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        print(f"Bank server starting on {HOST}:{PORT}")
        
        # ssl_handshake_server will handle the binding
        client_socket, shared_secret = ssl_ctx_rev.ssl_handshake_server(server_socket, HOST, PORT)

        while True:
            handle_request(client_socket, shared_secret)