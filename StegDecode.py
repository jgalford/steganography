# StegDecode.py
# DESCRIPTION: This script utilizes steganography to extract a concealed message 
# from the least significant bits of an image. Steganography is the practice of 
# hiding information within a medium, in this case, subtly altering the RGB values 
# of pixels in an image. 

# Import statements
from PIL import Image
from ast import literal_eval
from bitarray import bitarray
from cryptography.fernet import Fernet
import hashlib
from base64 import urlsafe_b64encode

# Array to store the extracted binary data
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

# Open the image and determine its size
with Image.open("dyr_secret.png") as img:
    width, height = img.size

    # Loop through each pixel in the image
    for x in range(width):
        for y in range(height):

            # Get the RGB(Red Green Blue) values at the current pixel
            pixel = list(img.getpixel((x, y)))

            # Extract the least significant bit from each RGB value and append to the array
            extracted_bin.extend(pixel[n] & 1 for n in range(3))

# Get the extracted binary into a string

data = str(bitarray(extracted_bin).tobytes())

# Chop off first byte, and convert it from binary to integer
data_len = str(bitarray(extracted_bin[:16]))

converted_len = int(data_len[10:-2], 2)

# Weird stuff be happening
if (converted_len >= 140):
    print(decrypter(data[10:converted_len+10], password))
else:
    print(decrypter(data[7:converted_len+7], password))