from PIL import Image
import os

def convert():
    img_path = "assets/logo.png"
    ico_path = "assets/logo.ico"
    
    if os.path.exists(img_path):
        img = Image.open(img_path)
        # Resize to common icon sizes
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ico_path, sizes=icon_sizes)
        print(f"Successfully converted {img_path} to {ico_path}")
    else:
        print(f"Error: {img_path} not found")

if __name__ == "__main__":
    convert()
