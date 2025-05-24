from PIL import Image

input_path = 'assets/monsters/segfault.png'
output_path = 'assets/monsters/segfault_128x128.png'

img = Image.open(input_path)

img_resized = img.resize((128, 128), Image.NEAREST)

img_resized.save(output_path)

print(f"Spritesheet save in {output_path}")


