# SSL Bank Protocol: Development & Cryptanalysis

A two-phase security engineering project implementing both defensive and offensive roles for educational purposes. The project involved designing a simplified TLS-like protocol for a banking application, followed by conducting a security assessment of a peer team's implementation.


![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Cryptography](https://img.shields.io/badge/Cryptography-8B0000?style=for-the-badge&logo=key)
![Security](https://img.shields.io/badge/Security-32CD32?style=for-the-badge&logo=shield-check)


## Tech Stack
* **Language:** Python
* **Networking:** Socket programming
* **Cryptography:** 
    * **Encryption:** 16-bit RSA (educational only), 10-bit Simplified DES
    * **Authentication:** SHA-1 based HMAC

## Team & Project Approach
This project was developed as part of the Cryptography and Network Security curriculum at Rensselaer Polytechnic Institute. It was completed by a team of two students using a collaborative paired-programming approach.

## Phase 1: Protocol Development
Our team implemented a simplified TLS-like protocol using 16-bit RSA for key exchange, 10-bit S-DES for session key establishment, and HMAC-SHA1 for message authentication. The protocol established channels between banking clients and servers.

My technical contributions included:
* Developed SSL/TLS-like handshake logic in Python
*  ⁠Implemented 16-bit RSA key generation and exchange
* Built HMAC-based message authentication system
*  ⁠Integrated custom S-DES implementation for encrypted messaging
* Used Python's hashlib for SHA-1 operations

## Phase 2: Security Assessment & Analysis
We performed a security assessment on a peer team's implementation of the same protocol specification, with my analysis focusing on their cryptographic primitives.

Deliverables:  
- [Protocol Implementation Report](White_Hat_SSL_Bank_Protocol.pdf) - Documentation of our protocol design and implementation.
-  [Security Assessment Report](Black_Hat_Cryptanalysis_Report.pdf) - analysis of peer implementation vulnerabilities.

My analysis contributions included:
* **Cryptanalysis:** Identified and documented critical vulnerabilities including:
  * Insufficient key space: 10-bit S-DES keys vulnerable to brute-force attacks
  * Use of hardcoded keys creating complete confidentiality compromise
  * Theoretical attack vectors including timing attacks and cryptanalysis
* **Report Writing:** Authored comprehensive analysis evaluating protocol against CIA triad, with educational mitigations for each vulnerability

## Installation & Usage
1. Clone the repository:
```
    git clone https://github.com/chungs10/ssl-bank-protocol
    cd ssl-bank-protocol
 ```
2. Install dependencies:


    No external dependencies required - uses only Python standard library.

    
3. Run the banking server:
```
    python bank_server.py
```

4. In a separate terminal, run the client:
```
    python atm_client.py
```


## Project Structure
```plaintext
ssl-bank-protocol/
├── README.md # Project overview and documentation
├── bank_server.py # Main banking server implementation
├── atm_client.py # ATM client application
├── crypto_utils.py # Cryptographic utilities (S-DES, RSA, SHA-1)
├── ssl_ctx_rev.py # SSL context and protocol utilities
├── White_Hat_SSL_Bank_Protocol.pdf # White hat implementation paper
├── Black_Hat_Cryptanalysis_Report.pdf # Black hat security assessment
└── Assignment.txt # Project requirements and specifications
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Security Disclaimer 
This implementation contains intentional weaknesses for educational purposes:
* 16-bit RSA (breakable in milliseconds)
* 10-bit S-DES keys (vulnerable to brute force)
* Custom cryptographic implementations
* **DO NOT USE FOR ANY REAL SECURITY APPLICATIONS**