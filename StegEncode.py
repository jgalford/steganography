# StegEncode.py
# DESCRIPTION: This script enables the concealment of a message within the least 
# significant bits of a selected image using steganography.

# Import statements
from PIL import Image
from cryptography.fernet import Fernet
import hashlib
from base64 import urlsafe_b64encode
import sys #for taking command line arguments

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

if(len(sys.argv)<2):


    print('''
    
  /$$$$$$  /$$$$$$$$ /$$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$$ 
 /$$__  $$|__  $$__/| $$_____/ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$| $$__  $$
| $$  \__/   | $$   | $$      | $$  \__/| $$  \ $$| $$  \__/| $$  \ $$| $$  \ $$
|  $$$$$$    | $$   | $$$$$   | $$ /$$$$| $$$$$$$$|  $$$$$$ | $$  | $$| $$$$$$$/
 \____  $$   | $$   | $$__/   | $$|_  $$| $$__  $$ \____  $$| $$  | $$| $$__  $$
 /$$  \ $$   | $$   | $$      | $$  \ $$| $$  | $$ /$$  \ $$| $$  | $$| $$  \ $$
|  $$$$$$/   | $$   | $$$$$$$$|  $$$$$$/| $$  | $$|  $$$$$$/|  $$$$$$/| $$  | $$
 \______/    |__/   |________/ \______/ |__/  |__/ \______/  \______/ |__/  |__/
                                                                                
                                                                                
    
    Welcome to STEGASOR the stenography tool encoder
    This program can also be run by inputing the target file, the destination file, and the message to encode after calling the program
    EG.
    python3 StegDecode.py /Path/To/Target/File.png /Path/To/Destination/File.png "secret message"
''')



    # Prompt the user for the inputs 
    source = input("What file do you want to encode too: ")
    dest = input("What do you want to name the file with the encoded message: ")
    message = input("What message are you encrypting: ")
    password = input("Password to encrypt: ")

else:
    if(len(sys.argv)<4):
        print("uhh ohh looks like you are missing some inputs remember your command should look like")
        print("python3 StegDecode.py /Path/To/Target/File.png /Path/To/Destination/File.png 'secretMessage'")
        quit()
    else:
        source = sys.argv[1]
        dest = sys.argv[2]
        message = sys.argv[3]
        #prompt the user for the password
        password = input("Password to encrypt: ")


# Encrypt message
cipher_message = encrypter(message, password)

# Convert the message to binary and add a byte(s) at the beginning to indicate how long the message is
message_bin = "".join([format(ord(i), "08b") for i in cipher_message])
data = bin(int(len(cipher_message)))[2:].zfill(16) + message_bin

# Open the image and determine size
with Image.open(source) as img:
    width, height = img.size

    # Nested loop to target every pixel in the image 
    for x in range(0, width):
        for y in range(0, height):

            # Obtain the RGB values at each location
            pixel = list(img.getpixel((x, y)))

            # If there is still data to inject, add the data to the least significant bit of each color channel
            for n in range(3):
                if i < len(data):
                    # ~1 is masking off the last bit, and | injects the data into the pixel
                    pixel[n] = pixel[n] & ~1 | int(data[i])
                    i += 1  # Move to the next bit in the data

            # Place the new pixel into the correct location
            img.putpixel((x, y), tuple(pixel))

    # Save the newly encoded image
    img.save(dest, "PNG")  # Save the modified image in PNG format

# Display a message indicating successful encoding
print("I'm in! ¯\_( ͡° ͜ʖ ͡°)_/¯")
