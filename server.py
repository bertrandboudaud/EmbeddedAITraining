import socket
import struct
from PIL import Image
import os

# Server parameters
HOST = '0.0.0.0'  # Server IP address
PORT = 42         # Server listening port
IMAGE_WIDTH = 640   # Image width
IMAGE_HEIGHT = 480  # Image height

# Function to receive image data
def receive_image(conn):
    image_data = b''

    # Receive image data
    while len(image_data) < IMAGE_WIDTH * IMAGE_HEIGHT * 1:  # 2 bytes (RGB565) per pixel
        data = conn.recv(4096)
        if not data:
            break
        image_data += data

    return image_data

# Function to convert RGB565 data to BMP image
def save_image_rgb565(image_data, count):
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))

    # Convert RGB565 data to image pixels
    pixels = []
    for i in range(0, len(image_data), 2):
        pixel = struct.unpack('<H', image_data[i:i+2])[0]
        r = ((pixel >> 11) & 0x1F) << 3
        g = ((pixel >> 5) & 0x3F) << 2
        b = (pixel & 0x1F) << 3
        pixels.append((r, g, b))

    img.putdata(pixels)

    # File name with an incremented number
    filename = f'received_image_{count}.bmp'
    img.save(filename, 'BMP')  # Save the image as BMP
    print(f"Image received and saved as {filename}.")

def save_image_grey_scale(image_data, count):
    #img = Image.frombytes('L', (IMAGE_WIDTH, IMAGE_HEIGHT), image_data)

    img = Image.new('L', (IMAGE_WIDTH, IMAGE_HEIGHT))

    # Convertir les données en pixels de l'image
    pixels = []
    for i in range(0, len(image_data)):
        pixel = struct.unpack('>B', image_data[i:i+1])[0]  # Big-endian interpretation
        pixels.append(pixel)
    img.putdata(pixels)
    
    # Nom du fichier avec numéro incrémenté
    filename = f'received_image_{count}.bmp'
    img.save(filename, 'BMP')  # Sauvegarder l'image en BMP
    print(f"Image reçue et sauvegardée en tant que {filename}.")

# Create the server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server is listening on {HOST}:{PORT}")

    conn_count = 0  # Connection counter

    while True:
        conn, addr = server_socket.accept()
        conn_count += 1

        with conn:
            print(f"Connection established with {addr}")

            image_data = receive_image(conn)  # Receive image data
            if image_data:
                save_image_grey_scale(image_data, conn_count)  # Convert and save the image as BMP with an incremented number