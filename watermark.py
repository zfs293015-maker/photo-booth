"""
watermark.py — 水印与文字叠加模块
功能：在照片上叠加文字水印、日期戳、Logo 图标
"""
from PIL import Image, ImageDraw, ImageFont
import os


def add_text(
    img: Image.Image,
    text: str,
    position: str = "bottom-right",
    font_size: int = 36,
    color: tuple = (255, 255, 255, 180),
    padding: int = 20,
) -> Image.Image:
    """
    在图片上叠加文字水印
    position: "bottom-right" | "bottom-left" | "top-right" | "top-left" | "center"
    color: (R, G, B, A) — A 是透明度，255=不透明，128=半透明
    """
    # 复制原图，避免修改原始对象（好的做法）
    img = img.copy().convert("RGBA")

    # 创建文字图层（透明画布，和原图一样大）
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))

    # 创建绘图对象（就像拿了一支笔）
    draw = ImageDraw.Draw(txt_layer)

    # 尝试加载字体，加载不到就用默认的
    font = _load_font(font_size)

    # 计算文字的宽高（用 bbox 取包围盒）
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]   # 文字宽度
    text_h = bbox[3] - bbox[1]   # 文字高度

    # 根据 position 计算放置坐标
    x, y = _calc_position(position, img.size, text_w, text_h, padding)

    # 把文字画到透明图层上
    draw.text((x, y), text, font=font, fill=color)

    # 合并文字图层和原图
    img = Image.alpha_composite(img, txt_layer)

    return img.convert("RGB")


def add_logo(
    img: Image.Image,
    logo_path: str,
    position: str = "top-left",
    scale: float = 0.15,
    padding: int = 20,
) -> Image.Image:
    """
    在图片上叠加 Logo 图标
    scale: Logo 占图片宽度的比例，0.15 = 15%
    """
    if not os.path.exists(logo_path):
        print(f"Logo 文件不存在：{logo_path}")
        return img

    logo = Image.open(logo_path).convert("RGBA")
    img = img.copy().convert("RGBA")

    # 按比例缩放 Logo
    logo_w = int(img.size[0] * scale)
    ratio = logo_w / logo.size[0]
    logo_h = int(logo.size[1] * ratio)
    logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

    # 计算位置
    x, y = _calc_position(position, img.size, logo_w, logo_h, padding)

    # 把 Logo 贴到图上（alpha_composite 保留透明通道）
    img.paste(logo, (x, y), logo)

    return img.convert("RGB")


def add_timestamp(img: Image.Image) -> Image.Image:
    """
    在右下角叠加时间戳（拍照日期，自动取当前时间）
    """
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return add_text(img, now, position="bottom-right", font_size=28, color=(255, 255, 255, 160))


# ═══════════════════════════════════
# 内部辅助函数（外部不需要知道的）
# ═══════════════════════════════════

def _load_font(size: int) -> ImageFont.FreeTypeFont:
    """尝试加载系统字体，失败则用 PIL 默认字体"""
    import sys
    if sys.platform == "linux":
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
        ]
        for path in candidates:
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _calc_position(
    pos: str, img_size: tuple, elem_w: int, elem_h: int, padding: int
) -> tuple:
    """根据位置字符串计算元素的 (x, y) 坐标"""
    w, h = img_size
    positions = {
        "top-left":     (padding, padding),
        "top-right":    (w - elem_w - padding, padding),
        "bottom-left":  (padding, h - elem_h - padding),
        "bottom-right": (w - elem_w - padding, h - elem_h - padding),
        "center":       ((w - elem_w) // 2, (h - elem_h) // 2),
    }
    return positions.get(pos, positions["bottom-right"])
