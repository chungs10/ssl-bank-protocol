# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 09:39:44 2024

@author: Raphael Chung
"""

def generate_subkeys(key):
    # Apply P10 permutation
    p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    key_permuted = [key[i - 1] for i in p10]
    
    # Split into two halves
    left_half = key_permuted[:5]
    right_half = key_permuted[5:]
    
    # Perform left circular shifts
    left_shift_1 = left_half[1:] + [left_half[0]]
    right_shift_1 = right_half[1:] + [right_half[0]]
    
    # Combine halves
    combined_shift_1 = left_shift_1 + right_shift_1
    
    # Apply P8 permutation to generate first subkey
    p8 = [6, 3, 7, 4, 8, 5, 10, 9]
    subkey1 = [combined_shift_1[i - 1] for i in p8]
    
    # Perform additional left circular shifts
    left_shift_2 = left_shift_1[2:] + left_shift_1[:2]
    right_shift_2 = right_shift_1[2:] + right_shift_1[:2]
    
    # Combine halves
    combined_shift_2 = left_shift_2 + right_shift_2
    
    # Apply P8 permutation to generate second subkey
    subkey2 = [combined_shift_2[i - 1] for i in p8]
    
    return subkey1,subkey2

def encryption(plaintext, subkey1, subkey2):
    # Apply initial permutation (IP)
    ip = [2, 6, 3, 1, 4, 8, 5, 7]
    permuted_text = [plaintext[i - 1] for i in ip]
    
    # Split into two halves
    left_half = permuted_text[:4]
    right_half = permuted_text[4:]
    
    # First round
    left_half, right_half = round_function(left_half, right_half, subkey1)
    
    # Swap halves
    left_half, right_half = right_half, left_half
    
    # Second round
    left_half, right_half = round_function(left_half, right_half, subkey2)
    
    # Combine halves
    combined_halves = left_half + right_half
    
    # Apply inverse initial permutation (IP^-1)
    ip_inverse = [4, 1, 3, 5, 7, 2, 8, 6]
    ciphertext = [combined_halves[i - 1] for i in ip_inverse]
    
    return ciphertext

def round_function(left_half, right_half, subkey):
    # Expand right half using E/P permutation
    ep = [4, 1, 2, 3, 2, 3, 4, 1]
    expanded_right = [right_half[i - 1] for i in ep]
    
    # XOR expanded right half with subkey
    xor_result = [int(expanded_right[i]) ^ int(subkey[i]) for i in range(len(expanded_right))]
    
    # Split XOR result into two halves
    left_xor = xor_result[:4]
    right_xor = xor_result[4:]
    
    # Apply S-Box substitution
    s_box_result = s_box_substitution(left_xor, right_xor)
    
    # Apply P4 permutation
    p4 = [2, 4, 3, 1]
    permuted_result = [s_box_result[i - 1] for i in p4]
    
    # XOR permuted result with left half
    xor_result2 = [int(permuted_result[i]) ^ int(left_half[i]) for i in range(len(permuted_result))]
    
    return xor_result2, right_half

def s_box_substitution(left_xor, right_xor):
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
    s_box_result1 = format(s_box1[row1][col1], '02b')

    row2 = (int(right_xor[0]) << 1) | int(right_xor[3])
    col2 = (int(right_xor[1]) << 1) | int(right_xor[2])
    s_box_result2 = format(s_box2[row2][col2], '02b')
    

    return s_box_result1 + s_box_result2

key = '1100011110'
plaintext = '00101000'

subkey1, subkey2 = generate_subkeys(key)
ciphertext = encryption(plaintext, subkey1, subkey2)
print("Ciphertext:", ''.join(str(c) for c in ciphertext))
