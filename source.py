import os
import time
import pyocr
import pyocr.builders
import pyautogui as pgui

from PIL import Image
from logging import getLogger, StreamHandler, DEBUG, Formatter, FileHandler

class Automation(object):
    def __init__(self):
        self.path_tesseract = "C:\\Program Files\\Tesseract-OCR"
        self.width, self.height = pgui.size()
        if self.path_tesseract not in os.environ["PATH"].split(os.pathsep):
            os.environ["PATH"] += os.pathsep + self.path_tesseract
        self.tools = pyocr.get_available_tools()
        self.tool = self.tools[0]
        self.configure_logger()

    def configure_logger(self):
        # log.txtがなかったら作成する。
        folder_name = "log"
        file_name = "log.txt"
        file_path = os.path.join(folder_name, file_name)
        if not os.path.exists(file_path):
            os.makedirs(folder_name, exist_ok=True)
            with open(file_path, "w") as file:
                pass
        else:
            pass

        # ログを設定する
        self.logger = getLogger(__name__)

        # コンソールに表示する場合は StreamHandler() を使う
        handler = StreamHandler()

        # ログファイルがあることを確認してそこに書き込む
        # handler = FileHandler("./log/log.txt")

        handler.setLevel(DEBUG)
        self.logger.setLevel(DEBUG)
        for h in self.logger.handlers[:]:
            self.logger.removeHandler(h)
            h.close()
        self.logger.addHandler(handler)
        formatter = Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(message)s')
        handler.setFormatter(formatter)

    def calculate_screen_ratio(self) -> tuple:
        # 画面サイズを取得する
        width, height = pgui.size()
        return width / 3840, height / 2160
    
    def capture_screenshot(self) -> str:
        screenshot_path = "./image/screenshot.png"
        pgui.screenshot(screenshot_path)
        return screenshot_path
    
    def image_ocr(self, path: str, target_str: str, left: int, upper: int, right: int, lower: int) -> tuple:
        x, y = self.calculate_screen_ratio()
        img_org = Image.open(path)
        img_gray = img_org.convert("L")
        img_crop = img_gray.crop((left * x, upper * y, right * x, lower * y))

        # 本番ではsaveしなくていい
        img_crop.save("./image/screenshot_gray.png")
        builder = pyocr.builders.WordBoxBuilder(tesseract_layout=6)
        result = self.tool.image_to_string(img_crop, lang="jpn", builder=builder)

        for line in result:
            if target_str in line.content:
                print(f"{target_str}の座標は、", line.position[0])
                return line.position[0]
        return None

    def locate_click(self, box: tuple):
        if box is not None:
            pgui.click(box)
        else:
            print("座標が見つかりませんでした。")

    def window_size_check(self, original_image: str):
        """_summary_

        画面解像度が3840x2160のとき、元からある画像を参照する
        Args:
            original_image (str): _description_

        Returns:
            _type_: _description_
        """
        if self.width == 3840 and self.height == 2160:
            img_path = original_image
        else:
            img_path = self.capture_screenshot()
        
        return img_path
    

if __name__ == "__main__":
    screen_reader = Automation()

    pgui.hotkey('alt', 'tab')
    pgui.alert()

    target_str = "あり"
    left, upper, right, lower = 670, 1740, 1530, 1940

    if screen_reader.width == 3840 and screen_reader.height == 2160:
        img_path = "./image/image_test.png"
    else:
        img_path = screen_reader.capture_screenshot()

    result = screen_reader.image_ocr(img_path, target_str, left, upper, right, lower)
    x, y = screen_reader.calculate_screen_ratio()

    if result is not None:
        new_tup = (result[0] + (left * x), result[1] + (upper * y))
        screen_reader.locate_click(new_tup)
    else:
        screen_reader.logger.debug("座標が見つかりません")