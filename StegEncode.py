# StegEncode.py
# DESCRIPTION: This script enables the concealment of a message within the least 
# significant bits of a selected image using steganography.

# Import necessary libraries
from PIL import Image  # Import the Image class from the Pillow library for image processing

# Counter variable to keep track of the message encoding
i = 0  # Initialize a counter for tracking the position in the message data

# Prompt the user for the message to be encoded
message = input("Message to encode: ")  # Get user input for the message to be hidden

# Convert the message to binary and prepend a byte(s) to indicate the message length
message_bin = "".join([format(ord(char), "08b") for char in message])  # Convert each character to 8-bit binary representation
data = bin(len(message))[2:].zfill(16) + message_bin  # Prepend a 16-bit binary representation of the message length

# Open the chosen image and determine its size
with Image.open("dyr.png") as img:  # Open the image file using the Pillow library
    width, height = img.size  # Get the dimensions of the image

    # Loop through every pixel in the image
    for x in range(width):
        for y in range(height):

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
    img.save("dyr_secret.png", "PNG")  # Save the modified image in PNG format

# Display a message indicating successful encoding
print("Message successfully encoded and saved in 'dyr_secret.png'")
