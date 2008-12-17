import pygame
import Image

def _triplets(pil_palette):
    palette = []
    for index in range(0, len(pil_palette), 3):
        rgb = pil_palette[index:index + 3]
        palette.append(rgb)
    return palette

def _image_window(pil_image):
    window = (0, 0) + pil_image.size
    if len(pil_image.tile) > 0:
        window = pil_image.tile[0][1]
    return window
    
def _to_pygame_image(pil_image, palette):
    (x0, y0, x1, y1) = _image_window(pil_image)
    image = pygame.image.fromstring(pil_image.tostring(), pil_image.size, 'P')
    image.set_palette(palette)
    image.set_colorkey(pil_image.info['transparency'])
    new_image = pygame.Surface(pil_image.size, pygame.SRCALPHA)
    new_image.blit(image, (x0, y0), (x0, y0, x1 - x0, y1 - y0))
    return new_image

def load_gif(image_filename):
    image = Image.open(image_filename)
    palette = _triplets(image.getpalette())
    images = []
    try:
        while 1:
            images.append(_to_pygame_image(image, palette))
            image.seek(image.tell() + 1)
    except EOFError:
        pass # end of sequence
    return (image.info['duration'], images)
