from pynput import keyboard
from pynput.keyboard import KeyCode
import datetime
import os

class KeyboardRecorder:
    def __init__(self):
        self.recording = False
        self.log_file = "d:\\keyboard_record.txt"
        
        # 定义热键组合
        self.START_COMBINATION = {keyboard.Key.alt_l, KeyCode.from_char('s')}
        self.QUIT_COMBINATION = {keyboard.Key.alt_l, KeyCode.from_char('q')}
        self.current_keys = set()

    def on_press(self, key):
        # 记录当前按下的键
        self.current_keys.add(key)

        # 检查热键组合
        if self.current_keys == self.START_COMBINATION:
            self.recording = not self.recording
            status = "开始" if self.recording else "暂停"
            print(f"记录{status}")
            return

        if self.current_keys == self.QUIT_COMBINATION:
            print("退出程序")
            return False

        # 如果正在记录，则写入文件
        if self.recording:
            try:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(self.log_file, "a", encoding="utf-8") as f:
                    if hasattr(key, 'char'):
                        if key.char:
                            f.write(f"{timestamp}: {key.char}\n")
                    else:
                        f.write(f"{timestamp}: {str(key)}\n")
            except Exception as e:
                print(f"写入文件时出错: {e}")

    def on_release(self, key):
        try:
            self.current_keys.remove(key)
        except KeyError:
            pass

    def start(self):
        print("键盘记录程序已启动")
        print("按 Alt+S 开始/暂停记录")
        print("按 Alt+Q 退出程序")
        
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        ) as listener:
            listener.join()

if __name__ == "__main__":
    recorder = KeyboardRecorder()
    recorder.start()
