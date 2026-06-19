from PIL import Image, ImageEnhance, ImageFilter

def process_photo(input_path, output_path="output.jpg"):
    img = Image.open(input_path)
    print(f"原图: {img.size}")
    img = ImageEnhance.Brightness(img).enhance(1.2)
    img = ImageEnhance.Contrast(img).enhance(1.1)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    img = img.convert("RGB")
    img.save(output_path, quality=95)
    print(f"已保存 -> {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python3 app.py 照片.jpg")
    else:
        process_photo(sys.argv[1])
