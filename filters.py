"""
filters.py — 照片滤镜模块
提供：复古、黑白、暖色、冷色四种滤镜
"""
from PIL import Image, ImageEnhance


def grayscale(img: Image.Image) -> Image.Image:
    """黑白滤镜：去色 + 加对比度模拟胶片质感"""
    img = img.convert("L")          # L 模式 = 灰度（去掉所有颜色）
    img = img.convert("RGB")        # 转回 RGB，不然不能和彩色图混用
    img = ImageEnhance.Contrast(img).enhance(1.3)  # 加对比，让黑白更有力
    return img


def vintage(img: Image.Image) -> Image.Image:
    """复古滤镜：暖色调 + 降低饱和度 + 加黄"""
    from PIL import ImageOps
    # 1. 降低饱和度 50%（颜色褪一半，像老照片）
    img = ImageEnhance.Color(img).enhance(0.5)
    # 2. 调暖：加点黄色和红色
    r, g, b = img.split()
    r = r.point(lambda p: min(255, int(p * 1.15)))   # 红色通道提 15%
    g = g.point(lambda p: min(255, int(p * 1.05)))   # 绿色微提
    b = b.point(lambda p: min(255, int(p * 0.8)))    # 蓝色减 20%（减蓝=加黄）
    img = Image.merge("RGB", (r, g, b))
    # 3. 加对比，显旧
    img = ImageEnhance.Contrast(img).enhance(1.2)
    return img


def warm(img: Image.Image) -> Image.Image:
    """暖色滤镜：提升色温，照片偏暖"""
    r, g, b = img.split()
    r = r.point(lambda p: min(255, int(p * 1.2)))    # 红色 +20%
    g = g.point(lambda p: min(255, int(p * 1.1)))    # 绿色 +10%
    b = b.point(lambda p: min(255, int(p * 0.7)))    # 蓝色 -30%
    return Image.merge("RGB", (r, g, b))


def cool(img: Image.Image) -> Image.Image:
    """冷色滤镜：降低色温，照片偏冷"""
    r, g, b = img.split()
    r = r.point(lambda p: min(255, int(p * 0.8)))    # 红色 -20%
    g = g.point(lambda p: min(255, int(p * 1.05)))   # 绿色微提
    b = b.point(lambda p: min(255, int(p * 1.25)))   # 蓝色 +25%
    return Image.merge("RGB", (r, g, b))


# 滤镜注册表：名字 → 函数，app.py 用这个查滤镜
FILTERS = {
    "grayscale": grayscale,
    "vintage":   vintage,
    "warm":      warm,
    "cool":      cool,
}
