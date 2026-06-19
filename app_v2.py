"""
Photo Booth v2.0 — 自助照相机图像处理器
功能：滤镜 + 水印 + 拼接 + 打印，一条命令跑全流程
"""
import argparse
from PIL import Image

from filters import FILTERS
from watermark import add_text, add_timestamp
from collage import vertical, horizontal, grid
from printer import print_photo, print_preview


def main():
    parser = argparse.ArgumentParser(
        description="Photo Booth — 自助照相机图像处理器"
    )
    # 输入图片
    parser.add_argument(
        "input", nargs="+", help="要处理的照片路径（支持多张）"
    )
    # 滤镜
    parser.add_argument(
        "--filter",
        choices=list(FILTERS.keys()),
        help="滤镜：grayscale / vintage / warm / cool",
    )
    # 水印文字
    parser.add_argument(
        "--watermark", type=str, help="水印文字内容"
    )
    # 时间戳
    parser.add_argument(
        "--timestamp", action="store_true", help="添加拍摄时间戳"
    )
    # 拼接
    parser.add_argument(
        "--collage",
        choices=["vertical", "horizontal", "grid"],
        help="拼接方式",
    )
    # 拼接到网格的列数
    parser.add_argument(
        "--cols", type=int, default=2, help="网格拼接时每行列数"
    )
    # 打印
    parser.add_argument(
        "--print", action="store_true", help="发送到打印机"
    )
    parser.add_argument(
        "--preview", action="store_true", help="生成打印预览 PDF"
    )
    # 输出
    parser.add_argument(
        "-o", "--output", default="output.jpg", help="输出文件路径"
    )

    args = parser.parse_args()

    # 1. 读图片（支持多张）
    images = []
    for f in args.input:
        try:
            images.append(Image.open(f))
            print(f"读取：{f} ({images[-1].size[0]}×{images[-1].size[1]})")
        except Exception as e:
            print(f"无法打开 {f}：{e}")
            return

    # 2. 滤镜
    if args.filter:
        filter_func = FILTERS[args.filter]
        images = [filter_func(img) for img in images]
        print(f"滤镜：{args.filter}")

    # 3. 水印
    if args.watermark:
        images = [
            add_text(img, args.watermark, "bottom-right", 36, (255, 255, 255, 180))
            for img in images
        ]
        print(f"水印：{args.watermark}")

    if args.timestamp:
        images = [add_timestamp(img) for img in images]
        print("加时间戳完成")

    # 4. 拼接（多张时才做）
    result = images[0]
    if len(images) > 1 and args.collage:
        if args.collage == "vertical":
            result = vertical(images, gap=8)
        elif args.collage == "horizontal":
            result = horizontal(images, gap=8)
        elif args.collage == "grid":
            result = grid(images, cols=args.cols, gap=8)
        print(f"拼接：{args.collage} ({result.size[0]}×{result.size[1]})")
    else:
        result = images[0]

    # 5. 保存
    result = result.convert("RGB")
    result.save(args.output, quality=95)
    print(f"已保存 → {args.output}")

    # 6. 打印
    if args.preview:
        print_preview(args.output, args.output.replace(".jpg", ".pdf"))

    if args.print:
        print_photo(args.output)


if __name__ == "__main__":
    main()
