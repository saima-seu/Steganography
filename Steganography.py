import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def encode_message(image_path, message):
    # Open the image
    image = Image.open(image_path)
    encoded = image.copy()
    
    width, height = image.size
    pixels = encoded.load()

    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Delimiter to mark the end of the message

    message_index = 0
    for row in range(height):
        for col in range(width):
            pixel = list(pixels[col, row])
            for n in range(3):  # Modify RGB values one by one
                if message_index < len(binary_message):
                    pixel[n] = pixel[n] & ~1 | int(binary_message[message_index])
                    message_index += 1
            pixels[col, row] = tuple(pixel)

            if message_index >= len(binary_message):
                break
        if message_index >= len(binary_message):
            break

    encoded.save("encoded_image.png")
    return "encoded_image.png"

def decode_message(image_path):
    image = Image.open(image_path)
    binary_message = ""
    
    width, height = image.size
    pixels = image.load()

    for row in range(height):
        for col in range(width):
            pixel = list(pixels[col, row])
            for n in range(3):  # Extract LSB from each RGB value
                binary_message += str(pixel[n] & 1)

    # Split binary message into 8-bit chunks
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]

    decoded_message = ""
    for char in chars:
        if char == '11111110':  # Stop at the delimiter
            break
        decoded_message += chr(int(char, 2))

    return decoded_message

def encode_button_clicked():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    message = text_box.get("1.0", "end-1c")
    if not message:
        messagebox.showwarning("Warning", "Please enter a message to encode.")
        return

    try:
        encoded_image_path = encode_message(file_path, message)
        messagebox.showinfo("Success", f"Message encoded and saved to {encoded_image_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decode_button_clicked():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    try:
        decoded_message = decode_message(file_path)
        messagebox.showinfo("Decoded Message", decoded_message)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Image Steganography")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

encode_button = tk.Button(frame, text="Encode Message", command=encode_button_clicked)
encode_button.grid(row=0, column=0, padx=5, pady=5)

decode_button = tk.Button(frame, text="Decode Message", command=decode_button_clicked)
decode_button.grid(row=0, column=1, padx=5, pady=5)

text_box = tk.Text(frame, height=5, width=50)
text_box.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
