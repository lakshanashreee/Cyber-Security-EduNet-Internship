import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Function to encode text into an image
def encode_text(image_path, secret_text, output_path):
    img = cv2.imread(image_path)
    binary_secret = ''.join(format(ord(char), '08b') for char in secret_text) + '1111111111111110'  # End marker
    data_index = 0
    data_len = len(binary_secret)

    for row in img:
        for pixel in row:
            for i in range(3):  # RGB channels
                if data_index < data_len:
                    pixel[i] = (pixel[i] & 254) | int(binary_secret[data_index])  # Modify LSB
                    data_index += 1

    cv2.imwrite(output_path, img)
    return output_path

# Function to decode hidden text from an image
def decode_text(image_path):
    img = cv2.imread(image_path)
    binary_data = ""

    for row in img:
        for pixel in row:
            for i in range(3):  # Extracting LSB from RGB
                binary_data += str(pixel[i] & 1)

    # Convert binary to text
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    secret_text = ''.join(chr(int(byte, 2)) for byte in all_bytes)
    secret_text = secret_text.split('\xFE')[0]  # Extract text before end marker
    return secret_text

# GUI Application
def open_file():
    filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if filename:
        entry_image_path.delete(0, tk.END)
        entry_image_path.insert(0, filename)
        display_image(filename, img_label)

def save_file():
    return filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])

def encrypt_message():
    image_path = entry_image_path.get()
    secret_text = entry_message.get()
    if not image_path or not secret_text:
        messagebox.showerror("Error", "Please provide an image and message")
        return
    
    output_path = save_file()
    if not output_path:
        return
    
    encoded_image_path = encode_text(image_path, secret_text, output_path)
    display_image(encoded_image_path, img_label_output)
    messagebox.showinfo("Success", "Message successfully encoded!")

def decrypt_message():
    image_path = entry_image_path.get()
    if not image_path:
        messagebox.showerror("Error", "Please select an image")
        return
    
    decoded_text = decode_text(image_path)
    entry_decoded_message.delete(0, tk.END)
    entry_decoded_message.insert(0, decoded_text)
    messagebox.showinfo("Decoded Message", f"Extracted Message: {decoded_text}")

def display_image(image_path, label):
    img = Image.open(image_path)
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

# Create GUI Window
root = tk.Tk()
root.title("Image Steganography")
root.geometry("500x600")

# Image Selection
tk.Label(root, text="Select Image:").pack()
entry_image_path = tk.Entry(root, width=40)
entry_image_path.pack()
tk.Button(root, text="Browse", command=open_file).pack()

# Image Display
img_label = tk.Label(root)
img_label.pack()

# Message Entry
tk.Label(root, text="Enter Secret Message:").pack()
entry_message = tk.Entry(root, width=40)
entry_message.pack()

# Encrypt Button
btn_encrypt = tk.Button(root, text="Encrypt & Save", command=encrypt_message)
btn_encrypt.pack()

# Encoded Image Display
img_label_output = tk.Label(root)
img_label_output.pack()

# Decrypt Button
btn_decrypt = tk.Button(root, text="Decode Message", command=decrypt_message)
btn_decrypt.pack()

# Decoded Message Output
entry_decoded_message = tk.Entry(root, width=40)
entry_decoded_message.pack()

# Run GUI Loop
root.mainloop()
