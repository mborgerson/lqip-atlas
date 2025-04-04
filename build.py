# /// script
# dependencies = ["pillow"]
# ///

import json
import math
import os

from PIL import Image

# Expected image size
full_width = 256
full_height = 366

# Scaled down size of image placed into atlas
tiny_width = 16
tiny_height = math.ceil(tiny_width / (full_width / full_height))

images_per_row = 50
output_atlas = "atlas.jpg"
output_map = "atlas_map.json"

# Collect images
images = []
for root, dirs, files in os.walk("images"):
    images.extend(os.path.join(root, file) for file in files if file.endswith(".jpg"))

# Calculate atlas size
rows = (len(images) + images_per_row - 1) // images_per_row
atlas_width = images_per_row * tiny_width
atlas_height = rows * tiny_height

# Create empty atlas
atlas = Image.new("RGB", (atlas_width, atlas_height))
mapping = {}

for index, image_path in enumerate(images):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((tiny_width, tiny_height), Image.LANCZOS)

    col = index % images_per_row
    row = index // images_per_row
    x = col * tiny_width
    y = row * tiny_height

    atlas.paste(img, (x, y))

    # We provide the coordinates of the thumbnail for simplicity, but could calculate it based on the index
    mapping[image_path] = {"x": x, "y": y}

# Save outputs
atlas.save(output_atlas, quality=50)
with open(output_map, "w") as f:
    json.dump(mapping, f, indent=2)

print(f"Tiny image size: {tiny_width}x{tiny_height} (1/{full_width/tiny_width})")
print(f"Saved atlas to {output_atlas} and map to {output_map}")
