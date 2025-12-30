from PIL import Image
import io

# Load the original output.png APNG
# Since PIL doesn't handle APNG well, let's extract first frame and use it as static avatar
img = Image.open('output.png')

# Get size and crop to 1:1
width, height = img.size
new_size = min(width, height)
left = (width - new_size) // 2
top = 0
right = left + new_size
bottom = new_size

# Crop and convert to RGBA with white background to avoid transparency issues
cropped = img.crop((left, top, right, bottom))

# Create a white background image
result = Image.new('RGBA', (new_size, new_size), (255, 255, 255, 255))
# Paste the cropped image with its alpha channel
if cropped.mode == 'RGBA':
    result = Image.alpha_composite(result, cropped)
else:
    result = cropped.convert('RGBA')

# Save as regular PNG (static, no animation)
result.save('avatar_static.png', 'PNG')
print(f"Saved static avatar: {new_size}x{new_size}")
