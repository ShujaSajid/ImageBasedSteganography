import tkinter as tk
from tkinter import ttk, INSERT, filedialog, END, messagebox
from PIL import Image
import ctypes

file_path = ""
enc_img_path = ""
img_path = ""
message = ""


def limitSizeDay(*args):
    value = dayValue.get()
    if len(value) > 4:
        dayValue.set(value[:4])


def limitSizeDay2(*args):
    value = dayValue2.get()
    if len(value) > 4:
        dayValue2.set(value[:4])


def file():
    global message
    global file_path
    path = filedialog.askopenfilename(title='Choose a text file', filetype=[
                                      ('Text Files Only', '*.txt')])
    if path != "":
        file_path = open(path, "r")
        message = file_path.read()
        mssg.delete("1.0", "end")
        mssg.insert(END, message)


def encoded_img_path():
    global enc_img_path
    enc_img_path = filedialog.askopenfilename(
        title='Choose Encoded Image', filetype=[('PNG Files Only', '*.png')])
    if enc_img_path != "":
        labelText2.set("Selected " + '✓')


def image_path():
    global img_path
    img_path = filedialog.askopenfilename(title='Choose an image', filetype=[
                                          ('JPG Files Only', '*.jpg')])
    if img_path != "":
        labelText.set("Image Selected " + '✓')


def save_file():
    if (txt.get("1.0", "end-2c")).strip() == "":
        messagebox.showwarning('Error', 'Message Box Empty!')
        return
    txt_file = open(filedialog.askdirectory(
        title='Save To') + "/saved_message.txt", "w")
    txt_file.write(txt.get("1.0", "end-2c"))
    txt_file.close()
    ctypes.windll.user32.MessageBoxW(0, "File Saved Successfully!", "Done.", 0)


def encode():
    if (mssg.get("1.0", "end")).strip() == "":
        messagebox.showwarning('Error', 'Message Box Empty!')
        return

    password = key_value.get()
    if len(password) == 4:
        if img_path == "":
            messagebox.showerror('Image Missing', 'Image Not Selected!')
            return
        msg = password + mssg.get("1.0", "end")
        bin_data = [format(ord(c), '08b') for c in list(msg)]
        bin_data_array = []
        for sets in bin_data:
            for x in sets:
                bin_data_array.append(x)
        img = Image.open(img_path, 'r')
        pixels = list(img.getdata())
        pixels_array = []
        for sets in pixels:
            for x in sets:
                pixels_array.append(x)
        if len(bin_data_array) > len(pixels_array):
            messagebox.showerror(
                'Image Error', 'Image too small for this data, try another image!')
            return
        new_pixels = []
        for i in range(0, len(msg)):
            temp_bindata = bin_data_array[:8]
            del bin_data_array[:8]
            temp_pixels = pixels_array[:9]
            del pixels_array[:9]
            for j in range(8):
                if temp_bindata[j] == '0' and temp_pixels[j] % 2 != 0:
                    temp_pixels[j] -= 1
                elif temp_bindata[j] == '1' and temp_pixels[j] % 2 == 0:
                    temp_pixels[j] -= 1
            if (i + 1) == len(msg):
                if temp_pixels[8] % 2 == 0:
                    temp_pixels[8] -= 1
            else:
                if temp_pixels[8] % 2 != 0:
                    temp_pixels[8] -= 1
            new_pixels.append(tuple(temp_pixels[0:3]))
            new_pixels.append(tuple(temp_pixels[3:6]))
            new_pixels.append(tuple(temp_pixels[6:9]))

        length = len(pixels_array)
        for x in range(0, length, 3):
            new_pixels.append(tuple(pixels_array[x:x + 3]))
        im = Image.new(img.mode, img.size)
        im.putdata(new_pixels)
        im.save(filedialog.askdirectory(
            title='Save To') + "/encoded_image.png")
        ctypes.windll.user32.MessageBoxW(
            0, "Image Encoded Successfully!", "Saved", 0)
    else:
        messagebox.showwarning('Key Error', 'Key must have 4 characters!')
        return


def decode():
    if enc_img_path == "":
        messagebox.showwarning('Image Missing', 'Image Not Selected!')
        return
    if (d_key_value.get()).strip() == "":
        ctypes.windll.user32.MessageBoxW(0, "", "Error", 0)
        messagebox.showwarning('Key Missing', 'Please Enter The Key.')
        return
    img = Image.open(enc_img_path, 'r')
    password = d_key_value.get()
    pixels = list(img.getdata())
    pixels_array = []
    for sets in pixels:
        for x in sets:
            pixels_array.append(x)
    msg2 = []
    for i in range(0, 4):
        l1 = []
        temp_pixels = pixels_array[:9]
        del pixels_array[:9]
        for j in range(8):
            if temp_pixels[j] % 2 == 0:
                l1.append('0')
            else:
                l1.append('1')
        msg2.append(chr(int((''.join(l1)), 2)))
        if temp_pixels[8] % 2 != 0:
            break
    decoded_pass = ''.join(msg2)
    if decoded_pass == password:
        msg2 = []
        for i in range(0, len(pixels_array)):
            l1 = []
            temp_pixels = pixels_array[:9]
            del pixels_array[:9]
            for j in range(8):
                if temp_pixels[j] % 2 == 0:
                    l1.append('0')
                else:
                    l1.append('1')
            msg2.append(chr(int((''.join(l1)), 2)))
            if temp_pixels[8] % 2 != 0:
                break
        decoded_msg = ''.join(msg2)
        txt.delete("1.0", "end")
        txt.insert(INSERT, decoded_msg)
    else:
        messagebox.showerror('Key Error', 'Wrong Key.')
        return


w = tk.Tk()
w.title("Image Steganography")
# configuring size of the win
wd = 312
ht = 350
ws = w.winfo_screenwidth()
hs = w.winfo_screenheight()
x = (ws / 2) - (wd / 2)
y = (hs / 2) - (ht / 2)
w.geometry('%dx%d+%d+%d' % (wd, ht, x, y))
w.resizable(0, 0)

# Create Tab Control
customed_style = ttk.Style()
customed_style.configure('Custom.TNotebook.Tab', padding=[
                         33, 4], font=('Helvetica', 14, 'bold'))
TAB_CONTROL = ttk.Notebook(w, style='Custom.TNotebook')

# Tab1
tab_style = ttk.Style()
tab_style.configure('new.TFrame', background="#1A1A1D")
TAB1 = ttk.Frame(TAB_CONTROL, style='new.TFrame')
TAB_CONTROL.add(TAB1, text='Encoder')
label1 = tk.Label(TAB1, text="Enter Your Message: ", background="#1A1A1D",
                  fg="white", font=('Helvetica', 12, 'bold')).grid(row=0, column=0)
mssg = tk.Text(TAB1, width=36, height=3, relief='ridge',
               borderwidth='4', background="#4E4E50", fg="white")
mssg.grid(row=1, column=0, padx=6)
label2 = tk.Label(TAB1, text="OR", background="#1A1A1D",
                  fg="white").grid(row=2, column=0)
line1 = tk.Label(TAB1, text="____________________________________________________________",
                 background="#1A1A1D", fg="white").place(x=0, y=120)
select_file = tk.Button(TAB1, text="Select Text File", command=lambda: file(), background="#C3073F",
                        fg="white", relief='solid', borderwidth='0', font=('Helvetica', 12)).grid(row=3, column=0)
label3 = tk.Label(TAB1, text="Create Key(4 chars):", background="#1A1A1D",
                  fg="white", font=('Helvetica', 12, 'bold')).place(x=0, y=150)
dayValue = tk.StringVar()
dayValue.trace('w', limitSizeDay)
key_value = tk.Entry(TAB1, width=22, relief='ridge', borderwidth='4',
                     background="#4E4E50", fg="white", textvariable=dayValue, show="*")
key_value.place(x=162, y=145, height=30)
select_image = tk.Button(TAB1, text='Select Image(.jpg)', width=15, height=1, command=lambda: image_path(
), background="#C3073F", fg="white", relief='solid', borderwidth='0', font=('Helvetica', 12))
select_image.place(x=85, y=180)
line2 = tk.Label(TAB1, text="____________________________________________________________",
                 background="#1A1A1D", fg="white").place(x=0, y=215)
labelText = tk.StringVar()
label4 = tk.Label(TAB1, textvariable=labelText,
                  background="#1A1A1D", fg="white")
label4.place(x=110, y=210)
encode_msg = tk.Button(TAB1, text='Encode & Save Image', width=18, height=3, command=lambda: encode(
), background="#C3073F", fg="white", relief='solid', borderwidth='0', font=('Helvetica', 12)).place(x=72, y=240)

# Tab2
TAB2 = ttk.Frame(TAB_CONTROL, style='new.TFrame')
TAB_CONTROL.add(TAB2, text='Decoder')
d_select_image = tk.Button(TAB2, text='Select Encoded Image', width=18, command=lambda: encoded_img_path(
), background="#C3073F", fg="white", relief='solid', borderwidth='0', font=('Helvetica', 12)).place(x=70, y=5)
line4 = tk.Label(TAB2, text="____________________________________________________________",
                 background="#1A1A1D", fg="white").place(x=0, y=60)
d_label1 = tk.Label(TAB2, text="Enter Key :", background="#1A1A1D",
                    fg="white", font=('Helvetica', 12, 'bold')).place(x=0, y=45)
dayValue2 = tk.StringVar()
dayValue2.trace('w', limitSizeDay2)
d_key_value = tk.Entry(TAB2, width=20, relief='ridge', borderwidth='4',
                       background="#4E4E50", fg="white", textvariable=dayValue2, show="*")
d_key_value.place(x=90, y=40, height=30)
d_decode_message = tk.Button(TAB2, text='Decode Message', width=20, height=2, command=lambda: decode(
), background="#C3073F", fg="white", relief='solid', borderwidth='0', font=('Helvetica', 12)).place(x=62, y=90)
txt = tk.Text(TAB2, relief='ridge', borderwidth='4',
              background="#4E4E50", fg="white")
txt.place(x=7, y=150, height=100, width=295)
txt.insert(INSERT, "Decoded message will appear here....")
d_save_message = tk.Button(TAB2, text='Save Message', command=lambda: save_file(), width=20, height=2,
                           background="#C3073F", fg="white", relief='solid', borderwidth='0', font=('Helvetica', 12)).place(x=63, y=258)
labelText2 = tk.StringVar()
label5 = tk.Label(TAB2, textvariable=labelText2,
                  background="#1A1A1D", fg="white")
label5.place(x=240, y=7)
TAB_CONTROL.pack(expand=1, fill="both")
w.mainloop()
