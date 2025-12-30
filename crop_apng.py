from apng import APNG
from PIL import Image
import io

# Load APNG
apng = APNG.open('output.png')

# Get all frames
frames = []
for png, control in apng.frames:
    # Convert PNG chunk to PIL Image
    img_data = png.to_bytes()
    img = Image.open(io.BytesIO(img_data))
    frames.append((img, control))

# Calculate crop box for 1:1 (center crop)
# Original: 640x360, target: 360x360 (use height as base)
width, height = frames[0][0].size
new_size = min(width, height)  # 360
left = (width - new_size) // 2  # 140
top = 0
right = left + new_size  # 500
bottom = new_size  # 360

print(f"Original size: {width}x{height}")
print(f"Crop box: ({left}, {top}, {right}, {bottom})")
print(f"New size: {new_size}x{new_size}")

# Crop each frame
cropped_frames = []
for img, control in frames:
    cropped = img.crop((left, top, right, bottom))
    cropped_frames.append((cropped, control))

# Save as new APNG
new_apng = APNG()
for img, control in cropped_frames:
    # Save frame to bytes
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    # Get delay from original control
    delay = control.delay if control else 100
    delay_den = control.delay_den if control and control.delay_den else 1000
    
    new_apng.append_file(buf, delay=delay, delay_den=delay_den)

new_apng.save('avatar.png')
print("Saved to avatar.png!")
