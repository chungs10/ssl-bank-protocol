# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 20:54:13 2024

@author: Raphael Chung

Tried to get everything running, but failed as DDT was coming out weird. 
Worked with others on it.

s_0 = [[1,0,2,3],
       [3,1,0,2],
       [2,0,3,1],
       [1,3,2,0]]
s_1 = [[0,3,1,2],
       [3,2,0,1],
       [1,0,3,2],
       [2,1,3,0]]

"""
s_0 = [[1,0,3,2],
       [3,2,1,0],
       [0,2,1,3],
       [3,1,3,2]]
s_1 = [[0,1,2,3],
       [2,0,1,3],
       [3,0,1,0],
       [2,1,0,3]]
def reduce_candidate_keys(differential_table, threshold=8):
    candidate_keys = []

    for key in range(16):
        count = sum(differential_table[key])
        if count >= threshold:
            candidate_keys.append(key)

    return candidate_keys

def obtain_key_bits(candidate_keys, bit_position):
    key_bits = [key >> bit_position & 1 for key in candidate_keys]
    return key_bits

def obtain_key(key_bits, bit_position):
    full_key = 0
    for i, bit in enumerate(key_bits):
        full_key |= (bit << i)
    return full_key

def generate_subkeys(key):
    key_binary = f"{key:010b}"  # Convert key to binary string
    # p10 permutation
    p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    key_p10 = [key_binary[i - 1] for i in p10]
    
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

    return ''.join(map(str, subkey1)), ''.join(map(str, subkey2))



def sbox(s, i):
    i_proc = tuple(map(lambda x: int(x), '{:04b}'.format(i)))
    idx_1 = 2 * i_proc[0] + i_proc[3]
    idx_2 = 2 * i_proc[1] + i_proc[2]
    return s[idx_1][idx_2]

ddt_0 = [[0] * 4 for _ in range(16)]


ddt_1 = [[0] * 4 for _ in range(16)]


for p1 in range(16):
    for p2 in range(16):
        xor_in = p1 ^ p2
        xor_out = sbox(s_0, p1) ^ sbox(s_0, p2)
        ddt_0[xor_in][xor_out] += 1

# Compute DDT for S-Box s_1
for p1 in range(16):
    for p2 in range(16):
        xor_in = p1 ^ p2
        xor_out = sbox(s_1, p1) ^ sbox(s_1, p2)
        ddt_1[xor_in][xor_out] += 1

# Print out DDT for S-Box s_0
print("DDT for S-Box s_0:")
for row in ddt_0:
    print(row)

# Print out DDT for S-Box s_1
print("\nDDT for S-Box s_1:")
for row in ddt_1:
    print(row)


# Reduce candidate keys based on the differential tables
candidate_0 = reduce_candidate_keys(ddt_0)
candidate_1 = reduce_candidate_keys(ddt_1)

# Obtain key bits for the specified bit position
bit_position = 3  # Change this to the desired bit position
key_bit_0 = obtain_key_bits(candidate_0, bit_position)
key_bit_1 = obtain_key_bits(candidate_1, bit_position)

# Obtain the full key for each S-Box
key_0 = obtain_key(key_bit_0, bit_position)
key_1 = obtain_key(key_bit_1, bit_position)

print("\nReduced Candidate Keys for S-Box 0:", candidate_0)
print("Reduced Candidate Keys for S-Box 1:", candidate_1)

print("\nObtained Key Bits for S-Box 0:", key_bit_0)
print("Obtained Key Bits for S-Box 1:", key_bit_1)

print("\nFull Key for S-Box 0:", key_0)
print("Full Key for S-Box 1:", key_1)

print("\nFull Key for S-Box 1:", bin(key_0))
print("Full Key for S-Box 2:", bin(key_1))

# Remove the '0b' prefix and pass the binary strings to generate_subkeys function
subkey1, subkey2 = generate_subkeys(key_0), generate_subkeys(key_1)
print("Subkey1:", subkey1)
print("Subkey2:", subkey2)