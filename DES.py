# Initial Permutation Table (IP)
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Final Permutation Table (FP) (Inverse of IP)
FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Function to convert hex to binary
def hex_to_binary(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)

# Function to convert binary to hex
def binary_to_hex(binary_str):
    return hex(int(binary_str, 2))[2:].upper()

# Function to perform permutation
def permute(input_str, table):
    # Ensure input is padded to the correct size for permutation
    if len(input_str) < 64:
        input_str = input_str.zfill(64)  # Pad with leading zeros to ensure 64 bits
    return ''.join(input_str[i-1] for i in table)

# Function to generate subkeys (simplified, real subkey generation is more complex)
def generate_subkeys(key_binary):
    # Placeholder for key schedule logic, this should implement PC-1, PC-2, and shifts
    subkeys = ['0' * 48] * 16  # Simplified placeholder subkeys (must be 16 subkeys of 48 bits)
    return subkeys

# Feistel function (simplified)
def feistel_function(right, subkey):
    # This is a simplified version, in reality, this would involve expansion, substitution, and permutation
    return right  # Placeholder for actual feistel operation

# XOR two binary strings
def xor(a, b):
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))

# DES encryption
def des_encrypt(plaintext_hex, key_hex):
    # Convert plaintext and key from hex to binary
    plaintext_binary = hex_to_binary(plaintext_hex)
    key_binary = hex_to_binary(key_hex)

    # Perform Initial Permutation (IP)
    ip_result = permute(plaintext_binary, IP)

    # Split into Left (L) and Right (R) halves
    left, right = ip_result[:32], ip_result[32:]

    # Key schedule (Generate subkeys)
    subkeys = generate_subkeys(key_binary)

    # 16 rounds of DES
    for i in range(16):
        # Apply Feistel function (simplified here)
        temp_right = feistel_function(right, subkeys[i])
        new_left = xor(left, temp_right)
        left = new_left
        if i < 15:
            left, right = right, left  # Swap left and right for the next round

    # Combine L16 and R16 and apply Final Permutation (FP)
    combined = left + right
    fp_result = permute(combined, FP)
    return binary_to_hex(fp_result)

# DES decryption
def des_decrypt(ciphertext_hex, key_hex):
    # Similar process as encryption but with the key schedule reversed
    ciphertext_binary = hex_to_binary(ciphertext_hex)
    key_binary = hex_to_binary(key_hex)

    # Perform Initial Permutation (IP)
    ip_result = permute(ciphertext_binary, IP)

    # Split into Left (L) and Right (R) halves
    left, right = ip_result[:32], ip_result[32:]

    # Key schedule (Generate subkeys)
    subkeys = generate_subkeys(key_binary)

    # 16 rounds of DES (apply subkeys in reverse order)
    for i in range(15, -1, -1):
        temp_right = feistel_function(right, subkeys[i])
        new_left = xor(left, temp_right)
        left = new_left
        if i > 0:
            left, right = right, left  # Swap left and right for the next round

    # Combine L16 and R16 and apply Final Permutation (FP)
    combined = left + right
    fp_result = permute(combined, FP)
    return binary_to_hex(fp_result)

# Main function to take inputs and perform DES encryption and decryption
if __name__ == "__main__":
    plaintext_hex = input("Enter 64-bit plaintext (hexadecimal): ")
    key_hex = input("Enter 56-bit key (hexadecimal): ")

    # Encrypt and Decrypt
    ciphertext_hex = des_encrypt(plaintext_hex, key_hex)
    decrypted_hex = des_decrypt(ciphertext_hex, key_hex)

    # Display results
    print("\n\nCiphertext (Hex):", ciphertext_hex)
    print("Decrypted Text (Hex):", decrypted_hex)
