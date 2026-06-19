from watermark import add_text, add_timestamp
from PIL import Image
img = Image.open("test_photo.jpg")
add_text(img, "Chalkak Photo", "bottom-right", 28, (255,255,255,180)).save("watermarked.jpg")
add_timestamp(img).save("timestamped.jpg")
print("水印 OK")
