from os import walk
import os
import pygame


def load_player_sprites(path, scale=1, images=None):
    if images == None:
        images = {"left": [], "right": []}

    cwd = os.getcwd()
    path = os.path.join(cwd, path)

    for filename in os.listdir(path):
        _, direction_count = filename.replace(".png", "").split("-")
        direction = "left" if "left" in direction_count else "right"

        image_path = os.path.join(path, filename)
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(
            image, (image.get_width() * scale, image.get_height() * scale))
        images[direction].append(image)

    return images