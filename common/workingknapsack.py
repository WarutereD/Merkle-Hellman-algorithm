import random

def gcd(a, b):
    """Returns the greatest common divisor of a and b using Euclid's algorithm."""
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """Returns a tuple (r, s, t) such that a*r + b*s = gcd(a,b) using the extended Euclidean algorithm."""
    s0, s1, t0, t1 = 1, 0, 0, 1
    while b:
        q, r = divmod(a, b)
        a, b = b, r
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    return a, s0, t0

def generate_superincreasing_sequence(n):
    """Generates a superincreasing sequence of length n."""
    import random
    s = [random.randint(1, 10)]
    for i in range(1, n):
        s.append(s[i-1] + random.randint(s[i-1]+1, 2*s[i-1]))
    return s

def generate_public_key(a, m, w):
    """Generates a public key for the Merkle-Hellman Knapsack Cryptosystem given the superincreasing sequence a, modulo m, and the integer w."""
    while gcd(w, m) != 1 or any(gcd(ai, w) != 1 for ai in a):
        w = random.randint(1, m-1)
    b = [(w * ai) % m for ai in a]
    return b

def generate_private_key(a, m, w):
    """Generates a private key for the Merkle-Hellman Knapsack Cryptosystem given the superincreasing sequence a, modulo m, and the integer w."""
    while True:
        t = random.randint(2, m-1)
        if gcd(t, m) == 1:
            break
    u = [(t*ai) % m for ai in a]
    s = sum(u)
    inv_t, _, _ = extended_gcd(t, m)
    r = (w * s * inv_t) % m
    return u, r

def encrypt(plaintext, a, m, w):
    # Convert the plaintext to binary
    binary = ''.join(format(ord(i), '08b') for i in plaintext)

    # Split the binary string into chunks of length len(a)
    chunks = [binary[i:i+len(a)] for i in range(0, len(binary), len(a))]

    # Calculate the sum of the binary digits multiplied by the corresponding values in the superincreasing sequence a
    encrypted = sum(int(chunks[i][j]) * a[j] for i in range(len(chunks)) for j in range(len(a)))

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
    d = []
    for a_i in reversed(a):
        if sum_ai_di >= a_i:
            d.append(1)
            sum_ai_di -= a_i
        else:
            d.append(0)
    plaintext = ''.join(str(bit) for bit in reversed(d))
    
    # Convert the binary string to ASCII characters
    plaintext = ''.join(chr(int(plaintext[i:i+8], 2)) for i in range(0, len(plaintext), 8))
    
    return plaintext

# Example usage
a = [2, 3, 6, 12, 25, 49, 98, 196]
m = 397
w = 35
ciphertext = 14
plaintext = decrypt(ciphertext, a, m, w)
print("OUTPUT:", plaintext) 