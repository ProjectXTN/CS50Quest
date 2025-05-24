from PIL import Image

input_path = 'assets/tiles/box_reward.png'
output_path = 'assets/tiles/box_reward_32x32.png'

img = Image.open(input_path)

img_resized = img.resize((32, 32), Image.NEAREST)

img_resized.save(output_path)

print(f"Spritesheet save in {output_path}")


