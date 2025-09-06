# only decrypt plaintext
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
                                print(f"{plain[:1000]}")
                                return plain
    return None, None

if __name__ == "__main__":
    with open("flag.txt", "rb") as f:
        enc_data = f.read()

    b(enc_data)

"""
root# python3 dec.py
flag DH{cry_m3_4_r1v3r_0x04d43f}
plain b'C# is an excellent programming languag\r\nbecause it combines simplicity with power\r\n
It offers strong type safety automatic memory management through garbage collection\r\
nand excellent performance The language has rich library support seamless integration with Microsoft ecosystem and cross platform capabilities with .NET Core\r\n
Its object oriented design makes code maintainable and scalable for enterprise applications\r\nDH{cry_m3_4_r1v3r_0x04d43f}'
"""
