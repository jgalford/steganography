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

# Array to store extracted binary
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
with Image.open("dyr_secret.png") as img:
    width, height = img.size

    # Loop through each pixel in the image
    for x in range(width):
        for y in range(height):

            # Get the RGB(Red Green Blue) values at the current pixel
            pixel = list(img.getpixel((x, y)))

            # Extract the least significant bit from each RGB value
            for n in range(3):
                # Using a bitmask (&1) to isolate the last bit
                extracted_bin.append(pixel[n] & 1)

# Convert the extracted binary data into a string
data = str(bitarray(extracted_bin).tobytes())

# Extract the length of the hidden message from specific positions in the data
data_len = data[4:6] + data[8:10]
converted_len = int(data_len, 16)

# Display the length of the hidden message for debugging purposes
print("The message is " + str(converted_len) + " characters.")

# Print only the necessary information
print(data[7:converted_len]) #255 characters max?