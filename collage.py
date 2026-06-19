"""
collage.py — 照片拼接模块
功能：多张竖图横向或纵向拼接成一条
"""
from PIL import Image


def horizontal(
    images: list,
    gap: int = 10,
    bg_color: tuple = (255, 255, 255),
) -> Image.Image:
    """
    横向拼接：N 张图排成一行
    gap: 图之间的间距（像素）
    """
    if not images:
        raise ValueError("至少传入一张图片")

    # 统一高度：以第一张图的高度为准，缩放其它图
    base_h = images[0].size[1]
    resized = []
    for img in images:
        if img.size[1] != base_h:
            w = int(img.size[0] * base_h / img.size[1])
            img = img.resize((w, base_h), Image.Resampling.LANCZOS)
        resized.append(img)

    # 计算总宽度：所有图宽之和 + 间距之和
    total_w = sum(i.size[0] for i in resized) + gap * (len(resized) - 1)

    # 创建画布
    canvas = Image.new("RGB", (total_w, base_h), bg_color)

    # 逐张贴图
    x = 0
    for img in resized:
        canvas.paste(img, (x, 0))
        x += img.size[0] + gap

    return canvas


def vertical(
    images: list,
    gap: int = 10,
    bg_color: tuple = (255, 255, 255),
) -> Image.Image:
    """
    纵向拼接：N 张图排成一列（自助照相机常用，4 张竖拍拼一条）
    """
    if not images:
        raise ValueError("至少传入一张图片")

    # 统一宽度
    base_w = images[0].size[0]
    resized = []
    for img in images:
        if img.size[0] != base_w:
            h = int(img.size[1] * base_w / img.size[0])
            img = img.resize((base_w, h), Image.Resampling.LANCZOS)
        resized.append(img)

    # 计算总高度
    total_h = sum(i.size[1] for i in resized) + gap * (len(resized) - 1)

    canvas = Image.new("RGB", (base_w, total_h), bg_color)

    y = 0
    for img in resized:
        canvas.paste(img, (0, y))
        y += img.size[1] + gap

    return canvas


def grid(
    images: list,
    cols: int = 2,
    gap: int = 10,
    bg_color: tuple = (255, 255, 255),
) -> Image.Image:
    """
    网格拼接：排列成 rows × cols 的矩阵
    cols: 每行几张
    """
    if not images:
        raise ValueError("至少传入一张图片")

    # 统一所有图的大小（用第一张的尺寸）
    base_w, base_h = images[0].size
    resized = []
    for img in images:
        img = img.resize((base_w, base_h), Image.Resampling.LANCZOS)
        resized.append(img)

    # 计算行列和画布大小
    rows = (len(resized) + cols - 1) // cols  # 向上取整
    canvas_w = base_w * cols + gap * (cols - 1)
    canvas_h = base_h * rows + gap * (rows - 1)
    canvas = Image.new("RGB", (canvas_w, canvas_h), bg_color)

    # 逐行逐列贴图
    for idx, img in enumerate(resized):
        row = idx // cols
        col = idx % cols
        x = col * (base_w + gap)
        y = row * (base_h + gap)
        canvas.paste(img, (x, y))

    return canvas
