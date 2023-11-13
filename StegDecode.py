# StegDecode.py
# DESCRIPTION: This script utilizes steganography to extract a concealed message 
# from the least significant bits of an image. Steganography is the practice of 
# hiding information within a medium, in this case, subtly altering the RGB values 
# of pixels in an image. 

# Import necessary libraries
from PIL import Image  # Pillow library for image processing
from bitarray import bitarray  # Efficient manipulation of binary data

# Array to store the extracted binary data
extracted_bin = []

# Open the image and determine its size
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

# Print only the necessary part of the hidden message
print(data[10 : 10 + converted_len])  # The hidden message (up to 255 characters)
