"""测试打印模块"""
from printer import print_preview, printer_status, print_photo

print("=== 打印机状态 ===")
status = printer_status()
print(f"打印机数量：{len(status['printers'])}")
for p in status["printers"]:
    print(f"  {p}")
print(f"等待中任务：{status['jobs'] or '无'}")

print("\n=== 生成打印预览 ===")
# 把输出照片转成 PDF（模拟打印输出）
print_preview("output.jpg", "photo_preview.pdf")
print_preview("photo_strip.jpg", "strip_preview.pdf")

print("\n=== 模拟打印 ===")
# 实际环境中接上 USB 打印机就会真的打印
result = print_photo("output.jpg")
print(f"打印结果：{'成功' if result else '失败（无打印机是正常的）'}")
