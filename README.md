#!/usr/bin/python3
#
# 修改说明：
# - 修复缩进错误
# - 优化GPIO触发逻辑
# - 添加异常处理
# - 明确目标类别ID

import Jetson.GPIO as GPIO
import time
import jetson.inference
import jetson.utils
import argparse
import sys

# 初始化GPIO（使用物理引脚编号）
GPIO.setmode(GPIO.BOARD)
relay_pin = 13  # 物理引脚13（BCM 27）
GPIO.setup(relay_pin, GPIO.OUT, initial=GPIO.LOW)  # 初始化为低电平

# 设置目标检测类别ID（需根据模型标签文件修改！）
target_class_id = 1  # 默认是人，例如杯子=42

# 命令行参数解析
parser = argparse.ArgumentParser(
    description="Real-time object detection with GPIO control",
    formatter_class=argparse.RawTextHelpFormatter,
    epilog=jetson.inference.detectNet.Usage() +
    jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage()
)

parser.add_argument("input_URI", type=str, default="/dev/video0", nargs='?',
                    help="URI of the input stream (default: /dev/video0)")
parser.add_argument("output_URI", type=str, default="display://0", nargs='?',
                    help="URI of the output stream (default: display://0)")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2",
                    help="pre-trained model to load")
parser.add_argument("--overlay", type=str, default="box,labels,conf",
                    help="detection overlay flags")
parser.add_argument("--threshold", type=float, default=0.5,
                    help="minimum detection threshold")

try:
    opt = parser.parse_known_args()[0]
except:
    parser.print_help()
    sys.exit(0)

# 创建视频输入输出对象
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

# 加载检测模型
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

try:
    while True:
        # 捕获帧
        img = input.Capture()

        # 执行检测
        detections = net.Detect(img, overlay=opt.overlay)
        
        # GPIO控制逻辑
        target_detected = False
        for detection in detections:
            print(f"[DEBUG] ClassID: {detection.ClassID}, Confidence: {detection.Confidence:.2f}")
            if detection.ClassID == target_class_id:
                target_detected = True
                break  # 检测到目标即触发

        # 控制继电器（单次脉冲）
        if target_detected:
            GPIO.output(relay_pin, GPIO.HIGH)
            time.sleep(0.1)  # 触发时间缩短为0.1秒
            GPIO.output(relay_pin, GPIO.LOW)
        else:
            GPIO.output(relay_pin, GPIO.LOW)

        # 渲染输出
        output.Render(img)
        output.SetStatus(f"{opt.network} | FPS: {net.GetNetworkFPS():.1f}")

        # 退出条件
        if not input.IsStreaming() or not output.IsStreaming():
            break

except KeyboardInterrupt:
    print("\nInterrupted by user")
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    GPIO.cleanup()  # 确保GPIO资源释放
    print("GPIO resources released")
