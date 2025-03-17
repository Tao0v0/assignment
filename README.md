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
