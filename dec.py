import hashlib
import random
import string

k = b"cry_me_a_river"

def isascii(data: bytes, length=10) -> bool:
    try:
        snippet = data[:length].decode('ascii')
    except UnicodeDecodeError:
        return False
    return all(c in string.printable for c in snippet)

def shuffle(data: bytes, k: bytes) -> bytes:
    seed = int.from_bytes(hashlib.md5(k).digest(), 'big')
    random.seed(seed)
    indices = list(range(len(data)))
    random.shuffle(indices)
    return bytes([data[i] for i in indices])

def sinv(data: bytes, k: bytes) -> bytes:
    seed = int.from_bytes(hashlib.md5(k).digest(), 'big')
    random.seed(seed)
    indices = list(range(len(data)))
    random.shuffle(indices)

    original = [0] * len(data)
    for original_pos, shuffled_pos in enumerate(indices):
        original[shuffled_pos] = data[original_pos]
    return bytes(original)

def whatisthis(data: bytes, key: bytes) -> bytes:
    key_stream = hashlib.sha256(key).digest()
    return bytes([b ^ key_stream[i % len(key_stream)] for i, b in enumerate(data)])

def decrypt(enc_data: bytes, flag: bytes) -> bytes:
    xored = whatisthis(enc_data, flag)
    plain = sinv(xored, k)
    return plain

def b(enc_data: bytes):
    pref = b"DH{cry_m3_4_r1v3r_0x"
    suff = b"}"
    hex_chars = '0123456789abcdef'

    for c1 in hex_chars:
        for c2 in hex_chars:
            for c3 in hex_chars:
                for c4 in hex_chars:
                    for c5 in hex_chars:
                        for c6 in hex_chars:
                            flag = pref + (c1+c2+c3+c4+c5+c6).encode() + suff
                            plain = decrypt(enc_data, flag)
                            if plain.startswith(b"C") and isascii(plain, length=10):
                                print(f"flag {flag.decode()}")
                                print(f"plain {plain[:1000]}")
                                return flag, plain
    return None, None

if __name__ == "__main__":
    with open("flag.txt", "rb") as f:
        enc_data = f.read()

    b(enc_data)
