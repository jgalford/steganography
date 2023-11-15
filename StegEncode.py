# StegEncode.py
# AUTHORS: Johnathan Alford, Dylan Lemon, Jack Long
# DATE: 10/6/23
# PURPOSE: Hide a message inside the least significant bit(s) of a desired image.

# Import statements
from PIL import Image
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()

with open("public_key.pem", "wb") as public_key_file:
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key_file.write(public_key_bytes)

with open("private_key.pem", "wb") as private_key_file:
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    private_key_file.write(private_key_bytes)


# Counter variable
i=0

# Prompt the user for the message 
message = input("Message to encode: ")
message_bytes = message.encode("utf-8")

ciphertext = public_key.encrypt(
    message_bytes,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )
)

# Convert the message to binary and add a byte(s) at the beginning to indicate how long the message is
data_bin = "".join([format(byte, "08b") for byte in ciphertext])
data = bin(len(ciphertext))[2:].zfill(16) + data_bin


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

