"""测试拼接：用四个滤镜效果图拼成一条"""
from collage import vertical, horizontal
from filters import grayscale, vintage, warm, cool
from PIL import Image

# 1. 读测试图
img = Image.open("test_photo.jpg")

# 2. 生成四张不同滤镜的图
grays  = grayscale(img)
vints  = vintage(img)
warms  = warm(img)
cools  = cool(img)

# 3. 纵向拼接（4 张竖图排一列，白底 8px 间距）
strip = vertical([grays, vints, warms, cools], gap=8)
strip.save("photo_strip.jpg")
print(f"拼接完成 → photo_strip.jpg ({strip.size[0]}×{strip.size[1]})")
