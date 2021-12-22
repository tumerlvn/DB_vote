import random
import primitive_root_algo as prime


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


def generatenapandg():
    p = 61
    g = prime.findPrimitive(p)
    return p, g


def generatekeys(p, g):
    message = p-10  # m
    e = random.randint(1, p - 1)  # a-
    d = (g ** e) % p  # a+
    digitalsign = (message ** e) % p  # <m>(s, a)
    return message, e, d, digitalsign


# Функции для отправки и получения сообщений для подтверждения цифровой подписи или ее опровержения
def receive(a, b = 0):
    return a, b


def receive(t: bool):
    return t


def send(a, b = 0):
    pass


def check(z):
    p, g = generatenapandg()
    M, e, d, S = generatekeys(p, g)

    u, v = 13, 17
    y = ((M ** u) * (g ** v)) % p

    w = 19
    h1 = (y * (g ** w)) % p
    h2 = (h1 ** e) % p
    # send(h1, h2)

    # receive(u, v)
    if prime.eqmod(e, (M ** u) * (g ** v), p):
        send(w)

    if prime.eqmod(h1, y * (g ** w), p) and prime.eqmod(h2, (S ** u) * (d ** (v + w)), p):
        print("Confirmed")
    else:
        print("Not Confirmed")


if __name__ == '__main__':
    check(5)
