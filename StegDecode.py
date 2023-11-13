# StegDecode.py
# AUTHORS: Johnathan Alford, Dylan Lemon, Jack Long, Tai Van Dam
# DATE: 10/6/23
# PURPOSE: Recover a message from inside the least significant bit(s) of a given image.

# Import statements
from PIL import Image
from ast import literal_eval
from bitarray import bitarray
import sys #for reading cli inputs

# Array to store extracted binary
extracted_bin = []

#Initialize Variables

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
                                                                                
                                                                                
    
    Welcome to STEGASOR the stenography tool decoder
    This program can also be run by inputing the target file to decode after calling the program
    EG.
    python3 StegDecode.py /Path/To/Target/File.png
''')
    source = input("What file do you want to decode: ")
else:
   source = sys.argv[1];



#Open the image and determine size
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

# Chop off first byte, and convert it from hex to integer
data_len = data[4:6] + data[8:10]
converted_len = int(data_len, 16)

# Debug statement
print("The message is " + str(converted_len) + " characters.")

# Print only the necessary information
print(data[10:10+converted_len]) #255 characters max?
