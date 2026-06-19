# Photo Booth Processor

自助照相机图像处理器 —— 照片滤镜、水印、拼接、打印，一条命令跑全流程。

## 功能

| 模块 | 说明 |
|------|------|
| **滤镜** | 黑白 / 复古 / 暖色 / 冷色 |
| **水印** | 文字叠加、Logo 贴图、时间戳 |
| **拼接** | 横向一行、纵向一列、网格矩阵 |
| **打印** | CUPS 打印 / PDF 预览 |

## 环境要求

- Python 3.10+
- Pillow (PIL)
- Linux / macOS / Windows
- CUPS（打印功能需要）

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 图片加复古滤镜 + 水印
python3 app_v2.py photo.jpg --filter=vintage --watermark="Photo Booth"

# 3. 四张图拼接成一条
python3 app_v2.py 1.jpg 2.jpg 3.jpg 4.jpg --collage=vertical -o strip.jpg

# 4. 全流程：滤镜 + 水印 + 时间戳 + 打印预览
python3 app_v2.py photo.jpg --filter=warm --watermark="Chalkak" --timestamp --preview -o result.jpg
```

## 项目结构

```
photo-booth/
├── app_v2.py        ← 主入口，命令行调度
├── filters.py       ← 滤镜模块（黑白/复古/暖色/冷色）
├── watermark.py     ← 水印模块（文字/Logo/时间戳）
├── collage.py       ← 拼接模块（横向/纵向/网格）
├── printer.py       ← 打印模块（CUPS/PDF预览）
├── requirements.txt ← 依赖清单
└── README.md        ← 项目说明
```

## 模块说明

### filters.py — 滤镜

```python
from filters import grayscale, vintage, warm, cool

img = Image.open("photo.jpg")
grayscale(img).save("gray.jpg")   # 黑白
vintage(img).save("vintage.jpg")  # 复古
warm(img).save("warm.jpg")        # 暖色
cool(img).save("cool.jpg")        # 冷色
```

### watermark.py — 水印

```python
from watermark import add_text, add_timestamp

img = Image.open("photo.jpg")
add_text(img, "Studio Name", "bottom-right", 36, (255,255,255,180)).save("wm.jpg")
add_timestamp(img).save("ts.jpg")  # 自动加时间戳
```

### collage.py — 拼接

```python
from collage import vertical, grid

# 纵向拼接
vertical([img1, img2, img3, img4], gap=8).save("strip.jpg")

# 2×2 网格
grid([img1, img2, img3, img4], cols=2, gap=10).save("grid.jpg")
```

### printer.py — 打印

```python
from printer import print_photo, print_preview, printer_status, print_multiple

# 查打印机状态
status = printer_status()
print(f"打印机：{status['printers']}，队列：{status['jobs']}")

# 出 PDF 预览（不实际打印）
print_preview("photo.jpg", "preview.pdf")

# 发送到打印机
print_photo("photo.jpg", copies=2, media="4x6")  # 2 张 4×6

# 批量打印多个文件
results = print_multiple(["a.jpg", "b.jpg", "c.jpg"], copies=1)
```

## 许可证

MIT
