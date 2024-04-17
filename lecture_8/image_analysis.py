import os
from PIL import Image, ImageFilter
from collections import Counter

def most_common_color(image_path):
    image = Image.open(image_path)
    pixels = list(image.getdata())
    most_common = Counter(pixels).most_common(1)
    return most_common[0][0]

print(most_common_color('data/scene.jpg'))

def find_edges(image_path):
    image = Image.open(image_path)
    image = image.convert('L')
    edges = image.filter(ImageFilter.FIND_EDGES)
    edges.save('/tmp/edges.jpg')
    os.system('feh /tmp/edges.jpg')

#find_edges('data/scene.jpg')

def blur_image(image_path):
    image = Image.open(image_path)
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))
    blurred_path = '/tmp/blurred_image.jpg'  # Save to temporary file
    blurred_image.save(blurred_path)
    os.system(f'feh {blurred_path}')  # Open with feh

def sharpen_image(image_path):
    image = Image.open(image_path)
    sharpened_image = image.filter(ImageFilter.UnsharpMask())
    sharpened_path = '/tmp/sharpened_image.jpg'  # Save to temporary file
    sharpened_image.save(sharpened_path)
    os.system(f'feh {sharpened_path}')  # Open with feh

# Example usage
blur_image('data/scene.jpg')
sharpen_image('data/scene.jpg')

