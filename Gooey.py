import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image

window = tk.Tk()
window.title("Welcome to Stegosaur!")

window.rowconfigure(0, minsize=230, weight=1)
window.columnconfigure(1, minsize=400, weight=1)

ende = 'e'

def en_swap():
    global ende
    if ende == 'd':
        ende = 'e'
        lbl_depassword.grid_forget()
        ent_password.grid_forget()
        btn_go.grid_forget()
        lbl_encode.grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)
        txt_message.grid(row = 0, column = 1, padx = 5, pady = 5)
        lbl_enpassword.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)
        ent_password.grid(row = 1, column = 1, sticky = "ew", padx = 5, pady = 5)
        btn_go.grid(row = 2, column = 1, padx = 5, pady = 10)

    else:
        pass

def de_swap():
    global ende
    if ende == 'e':
        ende = 'd'
        lbl_encode.grid_forget()
        lbl_enpassword.grid_forget()
        txt_message.grid_forget()
        ent_password.grid_forget()
        lbl_depassword.grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)
        ent_password.grid(row = 0, column = 1, sticky = "ew", padx = 5, pady = 5)
        btn_go.grid(row = 1, column = 1, padx = 5, pady = 10)
    else:
        pass

frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
lbl_menu = tk.Label(frm_buttons, text = "Menu")
btn_open = tk.Button(frm_buttons, text="Open")
btn_encode = tk.Button (frm_buttons, text = "Encode", command = en_swap)
btn_decode = tk.Button (frm_buttons, text = "Decode", command = de_swap)
btn_save = tk.Button(frm_buttons, text="Save As...")
btn_help = tk.Button(frm_buttons, text = "Help!")

lbl_menu.grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)
btn_open.grid(row= 1, column=0, sticky="ew", padx=5, pady=10)
btn_encode.grid(row = 2, column = 0, sticky = "ew", padx = 5, pady = 10)
btn_decode.grid(row = 3, column = 0, sticky = "ew", padx = 5, pady = 10)
btn_save.grid(row = 4, column = 0, sticky = "ew", padx = 5, pady = 10)
btn_help.grid(row = 5, column = 0, sticky = "ew", padx = 5, pady = 10)

frm_secrets = tk.Frame(window, relief = tk.RIDGE, bd = 2)
lbl_encode = tk.Label (frm_secrets, text = "Enter text to encode: ")
lbl_enpassword = tk.Label(frm_secrets, text = "Enter password to encrypt: ")
lbl_depassword = tk.Label(frm_secrets, text = "Enter password to decode: ")
txt_message = tk.Text(frm_secrets, height = 5, width = 50)
ent_password = tk.Entry(frm_secrets, width = 50)
btn_go = tk.Button(frm_secrets, text = "Run", padx = 10, pady = 5)

lbl_encode.grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)
txt_message.grid(row = 0, column = 1, padx = 5, pady = 5)
lbl_enpassword.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)
ent_password.grid(row = 1, column = 1, sticky = "ew", padx = 5, pady = 5)

btn_go.grid(row = 2, column = 1, padx = 5, pady = 10)

frm_buttons.grid(row=0, column=0, sticky="ns", )
frm_secrets.grid(row = 0, column = 1, sticky = "ns", padx = 20, pady = 50)


window.mainloop()
