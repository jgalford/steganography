# StegEncode.py
# AUTHORS: Johnathan Alford, Dylan Lemon, Jack Long
# DATE: 10/6/23
# PURPOSE: Hide a message inside the least significant bit(s) of a desired image.

# Import statements
from PIL import Image
from cryptography.fernet import Fernet
import hashlib
from base64 import urlsafe_b64encode

def encrypter(plaintext, password):
    # Generate hash from password, convert to string
    hash = hashlib.md5(password.encode()).hexdigest()
    # Fernet key must be 32 bytes and urlsafe base 64 encoded
    key = urlsafe_b64encode(hash.encode())
    token = Fernet(key)
    ciphertext = token.encrypt(plaintext.encode())
    #print(ciphertext)
    return ciphertext.decode()

# Counter variable
i=0

# Prompt the user for the message 
message = input("Message to encode: ")
password = input("Password to encrypt: ")

# Encrypt message
cipher_message = encrypter(message, password)

# Convert the message to binary and add a byte(s) at the beginning to indicate how long the message is
message_bin = "".join([format(ord(i), "08b") for i in cipher_message])
data = bin(int(len(cipher_message)))[2:].zfill(16) + message_bin
print(cipher_message)

# Open the image and determine size
with Image.open("dyr.png") as img:
    width, height = img.size

    # Nested loop to target every pixel in the image 
    for x in range(0, width):
        for y in range(0, height):

            # Grab the RGB values at each location
            pixel = list(img.getpixel((x, y)))
            for n in range(0,3):
                if(i < len(data)): # If there is still data to inject, add the data
                    # ~1 is masking off the last bit so that | will inject the data into the pixel
                    pixel[n] = pixel[n] & ~1 | int(data[i])
                    i+=1

            # Place the new pixel into the correct location
            img.putpixel((x,y), tuple(pixel))
            
    # Save the image
    img.save("dyr_secret.png", "PNG")

