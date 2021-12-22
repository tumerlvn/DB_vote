import random


# Regular Euclid algo
def euclid(m, n):
    if n == 0:
        return m
    else:
        r = m % n
        return euclid(n, r)


# Extended GCD
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


# Modular Inverse
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def generatenandpn():
    # Two large prime numbers p and q
    p = 61
    q = 53
    n = p * q
    Pn = (p - 1) * (q - 1)
    return n, Pn


def generatekeys(Pn):
    # Generate encryption key in range 1 < e < Pn
    key = []

    for i in range(2, Pn):
        gcd = euclid(Pn, i)
        if gcd == 1:
            key.append(i)

    # Select an encryption key from the above list
    e = random.choice(key)

    # Obtain inverse of
    # encryption key in Z_Pn
    d = modinv(e, Pn)
    print("decryption key is: ", d)

    return e, d


if __name__ == '__main__':
    n, Pn = generatenandpn()
    e, d = generatekeys(Pn)

    # Enter the message to be sent
    M = 123

    # Signature is created by Alice
    S = (M ** d) % n

    # Alice sends M and S both to Bob
    # Bob generates message M1 using the
    # signature S, Alice's public key e
    # and product n.
    M1 = (S ** e) % n

    # If M = M1 only then Bob accepts
    # the message sent by Alice.

    print(M)
    print(S)
    print(e)
    print(d)
    print(M1)

    if M == M1:
        print("As M = M1, Accept the message sent by Alice")
    else:
        print("As M not equal to M1, do not accept the message sent by Alice ")
