"""
printer.py — 打印模块
功能：照片打印、预览、打印队列查询
基于 CUPS（Common Unix Printing System）
"""
import subprocess
import os


def print_photo(
    file_path: str,
    copies: int = 1,
    media: str = "4x6",
    fit_to_page: bool = True,
) -> bool:
    """
    打印照片
    media: 纸张尺寸，4x6/5x7/a6 是照相馆常用
    fit_to_page: 自动缩放填满纸张
    """
    if not os.path.exists(file_path):
        print(f"文件不存在：{file_path}")
        return False

    # 构建 lp 命令（lp = line printer，CUPS 的打印命令）
    cmd = ["lp"]

    if copies > 1:
        cmd.extend(["-n", str(copies)])  # -n 份数

    if media:
        cmd.extend(["-o", f"media={media}"])  # -o 打印选项

    if fit_to_page:
        cmd.extend(["-o", "fit-to-page"])  # 自动缩放填充

    cmd.append(file_path)

    # subprocess.run() — 在 Python 里执行系统命令
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        # CUPS 成功时返回 "request id is xxx-xxx"
        print(f"已发送到打印机 → {result.stdout.strip()}")
        return True
    else:
        print(f"打印失败：{result.stderr.strip()}")
        return False


def print_preview(
    file_path: str,
    output_pdf: str = "preview.pdf",
) -> str:
    """
    打印预览：生成 PDF 文件（不实际打印）
    适合开发时测试打印效果
    """
    if not os.path.exists(file_path):
        print(f"文件不存在：{file_path}")
        return ""

    # 用 ImageMagick 的 convert 转 PDF
    # 如果没有 ImageMagick，用 Pillow 直接存 PDF
    try:
        from PIL import Image

        img = Image.open(file_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_pdf, "PDF", resolution=300)
        print(f"预览 PDF 已生成 → {output_pdf}")
        return output_pdf
    except Exception as e:
        print(f"生成预览失败：{e}")
        return ""


def printer_status() -> dict:
    """
    查询打印机状态和打印队列
    """
    status = {"printers": [], "jobs": []}

    # lpstat -p：列出所有打印机
    result = subprocess.run(
        ["lpstat", "-p"], capture_output=True, text=True
    )
    if result.stdout:
        status["printers"] = [
            line.strip() for line in result.stdout.split("\n") if line.strip()
        ]

    # lpstat -o：列出等待中的打印任务
    result = subprocess.run(
        ["lpstat", "-o"], capture_output=True, text=True
    )
    if result.stdout:
        status["jobs"] = [
            line.strip() for line in result.stdout.split("\n") if line.strip()
        ]

    return status


def print_multiple(files: list, copies: int = 1) -> dict:
    """
    批量打印多张照片，返回每张的结果
    """
    results = {}
    for f in files:
        name = os.path.basename(f)
        results[name] = print_photo(f, copies=copies)
    return results
