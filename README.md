# Custom TLS Implementation & Peer Security Assessment

A two-phase academic project involving the development of a custom cryptographic protocol and a penetration test against a peer team's implementation.

## Phase 1: White Hat - Protocol Development
Our team designed and built a custom TLS-like handshake and secure communication channel for a client-server banking application.

**My Key Contributions (White Hat):**
*   Developed the core SSL/TLS handshake logic in Python, facilitating key negotiation.
*   Implemented the RSA key generation and exchange mechanism.
*   Integrated the custom S-DES and SHA-1 implementations for encrypted and authenticated messaging.
*   architected the HMAC-based message authentication system to ensure integrity.

**Tech Stack (White Hat):** Python, Sockets (Networking), RSA, S-DES, SHA-1, HMAC

## Phase 2: Black Hat - Penetration Test & Analysis
We performed a security assessment on a peer team's implementation of the same protocol specification. My analysis focused on their cryptographic primitives.

**My Key Contributions (Black Hat):**
*   **Cryptanalysis:** Identified and documented critical vulnerabilities, including:
    *   **Insufficient Key Space:** 10-bit S-DES keys vulnerable to brute-force attacks.
    *   **Use of Hardcoded Keys:** Complete compromise of confidentiality if keys are extracted.
    *   **Theoretical Attack Vectors:** Susceptibility to timing attacks and cryptanalysis (linear, differential).
*   **Report Writing:** Authored a formal security assessment report detailing the findings, their impact on the CIA triad, and potential mitigations.

## Project Documentation
*   [**White Paper: Our Implementation**](./White_Hat_SSL_Bank_Protocol.pdf)
*   [**Black Hat Report: Peer Assessment**](./Black_Hat_Cryptanalysis_Report.pdf)

## Disclaimer
This project uses **deprecated and custom-built cryptographic algorithms (S-DES, custom SHA-1)** for educational purposes only. These should never be used in production systems.
