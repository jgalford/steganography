# Credits go here
#
#
#
#

# pip install cryptography
# pip install tkinter
# pip install pillow

# import statements
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from PIL import Image
from cryptography.fernet import Fernet
import hashlib
from base64 import urlsafe_b64encode
from bitarray import bitarray
import sys

window = tk.Tk()
window.title("Welcome to Stegosaur!")

window.rowconfigure(0, minsize=300, weight=1)
window.columnconfigure(1, minsize=400, weight=1)

ende = 'e'
filename = ''
mes = tk.StringVar()
pas = tk.StringVar()

# Change to encode mode
def en_swap():
    global ende
    if ende == 'd':
        ende = 'e'
        lbl_demode.grid_forget()
        lbl_depassword.grid_forget()
        ent_password.delete(0, 'end')
        ent_password.grid_forget()
        btn_go.grid_forget()
        lbl_enmode.grid(row = 0, column = 0, padx = 5, pady = 5)
        lbl_encode.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)
        ent_message.grid(row = 1, column = 1, padx = 5, pady = 5)
        lbl_enpassword.grid(row = 2, column = 0, sticky = "ew", padx = 5, pady = 5)
        ent_password.grid(row = 2, column = 1, sticky = "ew", padx = 5, pady = 5)
        btn_go.grid(row = 3, column = 1, padx = 5, pady = 10)

# Change to Decode Mode
def de_swap():
    global ende
    if ende == 'e':
        ende = 'd'
        lbl_enmode.grid_forget()
        lbl_encode.grid_forget()
        lbl_enpassword.grid_forget()
        ent_message.delete(0, 'end')
        ent_password.delete(0, 'end')
        ent_message.grid_forget()
        ent_password.grid_forget()
        lbl_demode.grid(row = 0, column = 0, padx = 5, pady = 5)
        lbl_depassword.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)
        ent_password.grid(row = 1, column = 1, sticky = "ew", padx = 5, pady = 5)
        btn_go.grid(row = 2, column = 1, padx = 5, pady = 10)

# Help text
def help():
    helptext = """Thanks for using Stegosaur!\n" 
    How to use:\n
    Open: Select an image to encode or decode. Must be .png\n
    Encode Mode: Encrypt a message and hide it in your image.\n
    Decode Mode: Enter the password to retrieve the hidden message.\n
    Help!: Display explanation.\n
    Exit: Quit program."""
    messagebox.showinfo(title = "Help", message = helptext, parent = window, default = 'ok')
# Open image
def open():
    global filename 
    filename = askopenfilename(
        title = 'Choose a .png image',
        filetypes=[('Image files', '*.png')]
    )
    if filename:
        messagebox.showinfo(title = 'File Opened', message = 'Opened ' + filename, parent = window, default = 'ok')
        lbl_filename.config(text = "Loaded file: " + filename)
    else:
        messagebox.showwarning(title = "Error", message = "No file selected.", parent = window, default = 'ok')

def exit():
    sys.exit()

def encrypter(plaintext, password):
    # Generate hash from password, convert to string
    hash = hashlib.md5(password.encode()).hexdigest()
    # Fernet key must be 32 bytes and urlsafe base 64 encoded
    key = urlsafe_b64encode(hash.encode())
    token = Fernet(key)
    ciphertext = token.encrypt(plaintext.encode())
    #print(ciphertext)
    return ciphertext.decode()

extracted_bin = []

def decrypter(ciphertext, password):
    try:
        # Generate hash from password, convert to string
        hash = hashlib.md5(password.encode()).hexdigest()
        # Fernet key must be 32 bytes and urlsafe base 64 encoded
        key = urlsafe_b64encode(hash.encode())
        token = Fernet(key)
        plaintext = token.decrypt(ciphertext.encode())
        return plaintext.decode()
    except:
        return

def run ():
    global filename
    global mes
    global pas
    global ende

    i=0
    message = mes.get()
    password = pas.get()
    
    # Error if no file open
    if not filename:
        messagebox.showwarning(title = "Error", message = "Open image file first.", parent = window, default = 'ok')
        return
    
    # Error if no message entered in encode mode
    if not message and ende == 'e':
        messagebox.showwarning(title = "Error", message = "No message entered.", parent = window, default = 'ok')
        return
    
    # Error if no password entered
    if not password:
        messagebox.showwarning(title = "Error", message = "No password entered.", parent = window, default = 'ok')
        return

    # Encode message
    if ende == 'e':
        # Encrypt message
        cipher_message = encrypter(message, password)

        # Convert the message to binary and add a byte(s) at the beginning to indicate how long the message is
        message_bin = "".join([format(ord(i), "08b") for i in cipher_message])
        data = bin(int(len(cipher_message)))[2:].zfill(16) + message_bin
        print(cipher_message)
        print (len(cipher_message))
        print(data[0:16])   
        with Image.open(filename) as img:
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
            savename = asksaveasfilename(title = 'Save As...', filetypes=[('Image files', '*.png')], defaultextension = '.png')
            img.save(savename)
            messagebox.showinfo(title = "Encoding complete", message = "Encoding complete. Saved to: " + savename, parent = window, default = 'ok')
            # Unload file
            filename = ''
            lbl_filename.config(text = "No file loaded")
    
    # Decode image
    else:
        with Image.open(filename) as img:
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

# Output decoded message to message box.
        dec_message = ''    
        if (converted_len >= 140):
                dec_message = decrypter(data[10:converted_len+10], password)
                if dec_message:
                    messagebox.showinfo(title = "Decoded message", message = dec_message, parent = window, default = 'ok')
                    # Unload image
                    filename = ''
                    lbl_filename.config(text = "No file loaded")    
                # Throw error if wrong password
                else:
                    messagebox.showwarning(title = "Error", message = "Incorrect password", parent = window, default = 'ok')
                    return
        else:
                dec_message = decrypter(data[7:converted_len+7], password)
                if dec_message:
                    messagebox.showinfo(title = "Decoded message", message = dec_message, parent = window, default = 'ok')
                    # Unload image
                    filename = ''
                    lbl_filename.config("No file loaded")
                # Throw error if wrong password
                else:
                    messagebox.showwarning(title = "Error", message = "Incorrect password", parent = window, default = 'ok')
                    return

    

# Elements for button sidebar
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
lbl_menu = tk.Label(frm_buttons, text = "Menu")
btn_open = tk.Button(frm_buttons, text="Open", command = open)
btn_encode = tk.Button (frm_buttons, text = "Encode Mode", command = en_swap)
btn_decode = tk.Button (frm_buttons, text = "Decode Mode", command = de_swap)
#btn_save = tk.Button(frm_buttons, text="Save As...")
btn_help = tk.Button(frm_buttons, text = "Help!", command = help)
btn_exit = tk.Button(frm_buttons, text = "Exit", command = exit)

# Load button sidebar
lbl_menu.grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)
btn_open.grid(row= 1, column=0, sticky="ew", padx=5, pady=10)
btn_encode.grid(row = 2, column = 0, sticky = "ew", padx = 5, pady = 10)
btn_decode.grid(row = 3, column = 0, sticky = "ew", padx = 5, pady = 10)
#btn_save.grid(row = 4, column = 0, sticky = "ew", padx = 5, pady = 10)
btn_help.grid(row = 4, column = 0, sticky = "ew", padx = 5, pady = 10)
btn_exit.grid(row=5, column = 0, sticky = "ew", padx = 5, pady = 10)


# Elements for encode mode and decode mode
frm_secrets = tk.Frame(window, relief = tk.RIDGE, bd = 2)
lbl_enmode = tk.Label(frm_secrets, text = "Encode Mode", font = ("Times New Roman", 15))
lbl_encode = tk.Label (frm_secrets, text = "Enter text to encode: ")
lbl_enpassword = tk.Label(frm_secrets, text = "Enter password to encrypt: ")
lbl_demode = tk.Label(frm_secrets, text = "Decode Mode", font = ("Times New Roman", 15))
lbl_depassword = tk.Label(frm_secrets, text = "Enter password to decode: ")
ent_message = tk.Entry(frm_secrets, textvariable = mes, width = 50)
ent_password = tk.Entry(frm_secrets, textvariable = pas, width = 50, show = '*')
btn_go = tk.Button(frm_secrets, text = "Run", padx = 10, pady = 5, command = run)
lbl_filename = tk.Label(frm_secrets, text = "No file loaded")

# Load elements for encode mode
lbl_enmode.grid(row = 0, column = 0, padx = 5, pady = 5)
lbl_filename.grid(row = 0, column = 1, sticky = "ew", padx = 5, pady = 5)
lbl_encode.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)
ent_message.grid(row = 1, column = 1, sticky = "ew", padx = 5, pady = 5)
lbl_enpassword.grid(row = 2, column = 0, sticky = "ew", padx = 5, pady = 5)
ent_password.grid(row = 2, column = 1, sticky = "ew", padx = 5, pady = 5)

btn_go.grid(row = 3, column = 1, padx = 5, pady = 10)

# Place sidebar and main space in window
frm_buttons.grid(row=0, column=0, sticky="ns", )
frm_secrets.grid(row = 0, column = 1, sticky = "ns", padx = 20, pady = 50)

# Start GUI
window.eval('tk::PlaceWindow . center')
window.mainloop()
