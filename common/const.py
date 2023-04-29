def encrypt(plaintext, a, m, w):
    # Check if plaintext is binary or not
    if not all(char in '01' for char in plaintext):
        # Convert plaintext to binary
        plaintext = ''.join(format(ord(char), '08b') for char in plaintext)
    
    # Convert the plaintext to an integer
    plaintext_int = int(plaintext, 2)

    # Calculate the sum of the binary digits multiplied by the corresponding values in the superincreasing sequence a
    encrypted = sum(a[i] for i in range(len(a)) if (1 << i) & plaintext_int)

    # Calculate the value of r = M^-1 mod W
    r = pow(m, -1, w)

    # Calculate the ciphertext by multiplying the encrypted value by r modulo W
    ciphertext = (encrypted * r) % w

    return ciphertext



def decrypt(ciphertext, a, m, w):
    """Decrypts the ciphertext using the Merkle-Hellman Knapsack Cryptosystem."""
    
    # Compute the modular multiplicative inverse of w modulo M
    inv_w = pow(w, -1, m)
    
    # Compute the sum of a_i * d_i for i in [0, n-1], where n is the length of A
    sum_ai_di = (ciphertext * inv_w) % m
    
    # Decrypt the ciphertext by solving the subset sum problem on the superincreasing sequence A
    d = [0] * len(a)
    for i in range(len(a) - 1, -1, -1):
        if a[i] <= sum_ai_di:
            d[i] = 1
            sum_ai_di -= a[i]
    
    # Convert the binary list to a binary string
    binary_str = ''.join(str(bit) for bit in reversed(d))
    
    # Convert the binary string to ASCII characters
    plaintext = ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))
    
    return binary_str, plaintext

# Example usage
a = [2, 3, 6, 12, 25, 49, 98, 196]
m = 397
w = 35
plaintext = "YeS"
ciphertext =""
if ciphertext == "":
    ciphertext = encrypt(plaintext, a, m, w)
binary_plaintext, decrypted_plaintext = decrypt(ciphertext, a, m, w)

print("Ciphertext:", ciphertext)
print("Decrypted plaintext (binary):", binary_plaintext)
print("Decrypted plaintext (ASCII):", decrypted_plaintext)
