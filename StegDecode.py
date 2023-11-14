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

# Array to store extracted binary
extracted_bin = []
password = input("Enter password: ")
def decrypter(ciphertext, password):
    # Generate hash from password, convert to string
    hash = hashlib.md5(password.encode()).hexdigest()
    # Fernet key must be 32 bytes and urlsafe base 64 encoded
    key = urlsafe_b64encode(hash.encode())
    token = Fernet(key)
    plaintext = token.decrypt(ciphertext.encode())
    return plaintext.decode()

# Open the image and determine size
with Image.open("dyr_secret.png") as img:
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

# Chop off first byte, and convert it from binary to integer
data_len = str(bitarray(extracted_bin[:16]))
converted_len = int(data_len[10:-2], 2)

# Debug statement
print("The message is " + str(converted_len) + " characters.")

# Print only the necessary information
print(data[7:converted_len+7]) #255 characters max?

print(decrypter(data[7:converted_len+7], password))