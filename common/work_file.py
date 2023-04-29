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

def encrypt(plaintext, b):
    """Encrypts the plaintext using the public key b."""
    ciphertext = 0
    for i, c in enumerate(plaintext):
        if c == '1':
            ciphertext += b[i]
    return ciphertext

def decrypt(ciphertext, u, r, m):
    """Decrypts the ciphertext using the private key u, r, and modulo m."""
    inv_r, _, _ = extended_gcd(r, m)
    s = (ciphertext * inv_r) % m
    v = []
    for ai in reversed(u):
        if ai <= s:
            v.append('1')
            s -= ai
        else:
            v.append('0')
    return ''.join(reversed(v))

# Example usage
def main():
    a = [2, 3, 6, 12, 25, 49, 98, 196]
    m = 397
    w = 35
    
    print("Select an option:")
    print("1: Encrypt a message")
    print("2: Decrypt a message")
    choice = int(input("Choice: "))
    
    if choice == 1:
        plaintext = input("Enter plaintext to encrypt: ")
        b = generate_public_key(a, m, w)
        ciphertext = encrypt(plaintext, b)
        print('Ciphertext:', ciphertext)
    elif choice == 2:
        ciphertext = int(input("Enter decrypted_text = decrypt(ciphertext, u, r, m"))
        decrypted_text = decrypt(ciphertext, u, r, m)
        print('Decrypted text:', decrypted_text)
    else:
        print("Invalid choice. Please enter 1 or 2.")
