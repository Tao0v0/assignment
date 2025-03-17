#!/usr/bin/python3
#
# 修改说明：
# 1. 添加默认摄像头输入（/dev/video0）
# 2. 优化GPIO控制逻辑，减少延迟
# 3. 修复GPIO清理问题
# 4. 支持自定义检测类别（修改target_class_id）

import Jetson.GPIO as GPIO
import time
import jetson.inference
import jetson.utils
import argparse
import sys

# 初始化GPIO
GPIO.setmode(GPIO.BOARD)
relay_pin = 13  # 物理引脚13（BCM编号27）
GPIO.setup(relay_pin, GPIO.OUT, initial=GPIO.LOW)

# 设置目标检测类别ID（参考模型标签文件）
target_class_id = 1  # 默认是人，改为你的目标类别ID（如杯子=42）

# 命令行参数解析
parser = argparse.ArgumentParser(
    description="Real-time object detection with GPIO control",
    formatter_class=argparse.RawTextHelpFormatter,
    epilog=jetson.inference.detectNet.Usage() +
    jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage()
)

parser.add_argument("input_URI", type=str, default="/dev/video0", nargs='?',  # 默认摄像头
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
            print(f"ClassID: {detection.ClassID}, Confidence: {detection.Confidence:.2f}")
            if detection.ClassID == target_class_id:
                target_detected = True
                break  # 检测到目标即触发

        # 控制继电器（脉冲信号）
        if target_detected:
            GPIO.output(relay_pin, GPIO.HIGH)
            time.sleep(0.1)  # 缩短触发时间
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
finally:
    GPIO.cleanup()  # 确保GPIO清理
    print("GPIO resources released")
