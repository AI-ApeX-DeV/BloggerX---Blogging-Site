import binascii
import hashlib
string = "data science"


def generate_hash_key(string):
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Convert the string to bytes and update the hash object
    sha256_hash.update(string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hash_key = sha256_hash.hexdigest()

    return hash_key


print(generate_hash_key(string))


def generate_short_hash(string):
    # Calculate the CRC32 hash
    crc32_hash = binascii.crc32(string.encode('utf-8'))

    # Convert the hash to a positive integer
    crc32_hash = crc32_hash & 0xffffffff

    # Convert the hash to a 5-character hexadecimal string
    short_hash = format(crc32_hash, 'x')[:5]

    return short_hash


short_hash = generate_short_hash(string)
print(short_hash)
