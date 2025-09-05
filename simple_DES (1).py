# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 17:14:43 2024

@author: Raphael Chung
"""
def generate_subkeys(key):
    # p10 permutation
    p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    key_p10 = [key[i - 1] for i in p10]
    
    # key split in half
    p10_left = key_p10[:5]
    p10_right = key_p10[5:]
    
    # Perform left shift
    left_1 = p10_left[1:] + [p10_left[0]]
    right_1 = p10_right[1:] + [p10_right[0]]
    
    # Combine halves
    combine_1 = left_1 + right_1
    
    # P8 permutation for new K1
    p8 = [6, 3, 7, 4, 8, 5, 10, 9]
    subkey1 = [combine_1[i - 1] for i in p8]
    
    # Perform two left shifts
    left_2 = left_1[2:] + left_1[:2]
    right_2 = right_1[2:] + right_1[:2]
    
    # Combine halves
    combine_2 = left_2 + right_2
    
    # Apply P8 permutation for new K2
    subkey2 = [combine_2[i - 1] for i in p8]
    
    return subkey1, subkey2

def encryption(plaintext, subkey1, subkey2):
    # P8 permutation for plain text
    ip = [2, 6, 3, 1, 4, 8, 5, 7]
    p_text = [plaintext[i - 1] for i in ip]

    # plaintext in half
    left_1 = p_text[:4]
    right_1 = p_text[4:]

    # First round
    left_1, right_1 = round_function(left_1, right_1, subkey1)

    # Swap halves
    left_1, right_1 = right_1, left_1

    # Second round
    left_1, right_1 = round_function(left_1, right_1, subkey2)

    # Combine halves
    combine_1 = left_1 + right_1

    # inverse permutation
    ip_inverse = [4, 1, 3, 5, 7, 2, 8, 6]
    ciphertext = [combine_1[i - 1] for i in ip_inverse]

    return ciphertext



def round_function(left_half, right_half, subkey):
    # Expansion and Permutation
    ep = [4, 1, 2, 3, 2, 3, 4, 1]
    e_right = [right_half[i - 1] for i in ep]
    
    # XOR expanded right half with subkey
    xor_result = [int(e_right[i]) ^ int(subkey[i]) for i in range(len(e_right))]
    
    # Split XOR result into two halves
    left_xor = xor_result[:4]
    right_xor = xor_result[4:]
    
    # Apply S-Box substitution
    s_result = s_box(left_xor, right_xor)
    
    # Apply P4 permutation
    p4 = [2, 4, 3, 1]
    p_result = [s_result[i - 1] for i in p4]
    
    # XOR permuted result with left half
    xor_result2 = [int(p_result[i]) ^ int(left_half[i]) for i in range(len(p_result))]
    
    return xor_result2, right_half

def s_box(left_xor, right_xor):
    s_box1 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
    ]
    
    s_box2 = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
    ]


    
    row1 = (int(left_xor[0]) << 1) | int(left_xor[3])
    col1 = (int(left_xor[1]) << 1) | int(left_xor[2])
    s_result1 = format(s_box1[row1][col1], '02b')

    row2 = (int(right_xor[0]) << 1) | int(right_xor[3])
    col2 = (int(right_xor[1]) << 1) | int(right_xor[2])
    s_result2 = format(s_box2[row2][col2], '02b')

    return s_result1 + s_result2

def decryption(ciphertext, subkey1, subkey2):
    # P8 permutation for ciphertext
    ip = [2, 6, 3, 1, 4, 8, 5, 7]
    p_text = [ciphertext[i - 1] for i in ip]

    # Ciphertext in half
    left_1 = p_text[:4]
    right_1 = p_text[4:]

    # First round 
    left_1, right_1 = round_function(left_1, right_1, subkey2)

    # Swap halves
    left_1, right_1 = right_1, left_1

    # Second round 
    left_1, right_1 = round_function(left_1, right_1, subkey1)

    # Combine halves
    combine_1 = left_1 + right_1

    # Inverse permutation
    ip_inverse = [4, 1, 3, 5, 7, 2, 8, 6]
    plaintext = [combine_1[i - 1] for i in ip_inverse]

    return plaintext



key = '1100011110'
plaintext = '00101000'

subkey1, subkey2 = generate_subkeys(key)
ciphertext = encryption(plaintext, subkey1, subkey2)
print("Subkey1:", "".join(str(c) for c in subkey1))
print("Subkey2:", "".join(str(c) for c in subkey2))
print("Ciphertext:", ''.join(str(c) for c in ciphertext))

decrypted_text = decryption(ciphertext, subkey1, subkey2)
print("Decrypted text:", ''.join(str(c) for c in decrypted_text))