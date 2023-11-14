# StegEncode.py
# AUTHORS: Johnathan Alford, Dylan Lemon, Jack Long
# DATE: 10/6/23
# PURPOSE: Recover a message from inside the least significant bit(s) of a given image.

# Import statements
from PIL import Image
from ast import literal_eval
from bitarray import bitarray
from cryptography.fernet import Fernet
import hashlib
from base64 import urlsafe_b64encode

# Hello. Is it me you're looking for?
extracted_bin = []

def decrypter(ciphertext, password):
    # Generate hash from password, convert to string
    hash = hashlib.md5(password.encode()).hexdigest()
    # Ciphertext has a b prepended when extracted. Remove or decryption fails.
    print(ciphertext)
    # Fernet key must be 32 bytes and urlsafe base 64 encoded
    key = urlsafe_b64encode(hash.encode())
    token = Fernet(key)
    plaintext = token.decrypt(ciphertext.encode())
    return plaintext.decode()

# Open the image and determine size
with Image.open("steganography/dyr_secret.png") as img:
    width, height = img.size

    # Nested loop to target every pixel in the image
    for x in range(0, width):
        for y in range(0, height):

            # Grab the RGB values at each location
            pixel = list(img.getpixel((x, y)))
            for n in range(0,3):
                # &1 is a bitmask so that only the last pixel is allowed through
                extracted_bin.append(pixel[n]&1)

# Get the extracted binary into a string
data = str(bitarray(extracted_bin).tobytes())

# Chop off first byte, and convert it from hex to integer
data_len = data[4:6] + data[8:10]
converted_len = int(data_len, 16)

# Debug statement
print("The message is " + str(converted_len) + " characters.")

# Print only the necessary information
print(data[7:converted_len]) #255 characters max?