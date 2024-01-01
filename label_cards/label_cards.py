import os
import json
import tkinter as tk
from PIL import Image, ImageTk

# Map card suits to their numerical values
suit_values = {'hearts': 100, 'diamonds': 200, 'clubs': 300, 'spades': 400}
# Map card values to their numerical values
card_values = {'7': 7, '8': 8, '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13, 'ace': 1}

def create_or_load_json(json_file):
    if not os.path.exists(json_file):
        with open(json_file, 'w') as file:
            json.dump({}, file)
    with open(json_file, 'r') as file:
        return json.load(file)

def update_json(selected_image, category, json_file):
    json_data = create_or_load_json(json_file)
    if selected_image not in json_data:
        json_data[selected_image] = category
        with open(json_file, 'w') as file:
            json.dump(json_data, file)

def display_gui(camera_images_dir, json_file):
    root = tk.Tk()
    root.title("Card Image Labeling")
    
    frame_top = tk.Frame(root, height=200, bg="blue")
    frame_top.pack(fill=tk.BOTH, expand=True)

    frame_bottom = tk.Frame(root, height=600, bg="red")
    frame_bottom.pack(fill=tk.BOTH, expand=True)

    # in our picture, we have 4 lines of 13 cards
    playing_cards_img = Image.open("label_icons/playing-cards.png")
    card_width, card_height = playing_cards_img.width / 13, playing_cards_img.height / 4
    cards = []

    # Create 32 small images for each card
    for y in range(4):
        for x in [0,6,7,8,9,10,11,12]:
            card = playing_cards_img.crop((x * card_width, y * card_height, (x + 1) * card_width, (y + 1) * card_height))
            card.thumbnail((150, 100))
            img = ImageTk.PhotoImage(card)
            cards.append(img)

    json_data = create_or_load_json(json_file)
    image_index = 0

    def select_card(event, selected_card):
        nonlocal image_index
        #x, y = event.x // card_width, event.y // card_height
        #selected_suit = ['hearts', 'diamonds', 'clubs', 'spades'][y]
        #selected_value = ['ace', '7', '8', '9', '10', 'jack', 'queen', 'king'][x]

        #selected_card = f'{suit_values[selected_suit] + card_values[selected_value]:03d}'
        update_json(camera_images[image_index], selected_card, json_file)
        image_index += 1
        if image_index < len(camera_images):
            load_camera_image(image_index)
        else:
            root.destroy()

    def load_camera_image(index):
        img_path = camera_images[index]
        img = Image.open(img_path)
        img.thumbnail((400, 300))
        img = ImageTk.PhotoImage(img)

        label = tk.Label(frame_top, image=img)
        label.image = img
        label.grid(row=0, column=0, columnspan=1, padx=10, pady=10)

    load_camera_image(image_index)

    for i, card_img in enumerate(cards):
        row, col = divmod(i, 8)
        label = tk.Label(frame_bottom, image=card_img)
        label.image = card_img
        label.grid(row=row + 1, column=col, padx=2, pady=2)
        label_value = [1,7,8,9,10,11,12,13]
        label.bind(f"<Button-1>", lambda event, selected_card = (row+1) * 100 + label_value[col]: select_card(event, selected_card)) 

    root.mainloop()

camera_images_directory = 'camera_output/'
json_file = 'labelled_images.json'

camera_images = [os.path.join(camera_images_directory, f) for f in os.listdir(camera_images_directory) if f.endswith('.png')]
camera_images.sort()

display_gui(camera_images, json_file)
