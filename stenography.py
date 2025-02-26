import cv2
import numpy as np

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
    print(f"Data encoded successfully! Saved as {output_path}")

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

    # Extract text before the end marker
    secret_text = secret_text.split('\xFE')[0]
    print(f"Decoded Text: {secret_text}")

# Example usage
image_path = "input.png"  # Input image path
output_image = "output.png"
secret_message = "Hello, this is a hidden message!"

# Encoding the secret message
encode_text(image_path, secret_message, output_image)

# Decoding the message
decode_text(output_image)
