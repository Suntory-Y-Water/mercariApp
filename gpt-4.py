from PIL import Image
import os
import pyocr
import pyocr.builders
import pyautogui as pgui

# インストール済みのTesseractへパスを通す
path_tesseract = "C:\\Program Files\\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

# OCRエンジンの取得
tools = pyocr.get_available_tools()
tool = tools[0]

# 画面サイズを取得する
width, height = pgui.size()

def calculate_screen_ratio() -> tuple:
    return width / 3840, height / 2160

def capture_screenshot() -> str:
    screenshot_path = "./image/screenshot.png"
    pgui.screenshot(screenshot_path)
    return screenshot_path

def image_ocr(
        path: str,
        target_str: str,
        left: int,
        upper: int,
        right: int, 
        lower: int) -> tuple:

    x, y = calculate_screen_ratio()

    # 画像の読み込み
    img_org = Image.open(path)

    # グレースケールに変換
    img_gray = img_org.convert("L")

    # 画像の切り抜き
    img_crop = img_gray.crop((left * x, upper * y, right * x, lower * y))
    img_crop.save("./image/screenshot_gray.png")

    # OCRの実行
    builder = pyocr.builders.WordBoxBuilder(tesseract_layout=6)
    result = tool.image_to_string(img_crop, lang="jpn", builder=builder)

    for line in result:
        if target_str in line.content:
            print(f"{target_str}の座標は、", line.position[0])
            return line.position[0]
    return None

def locate_click(box: tuple):
    if box is not None:
        pgui.click(box)
    else:
        print("座標が見つかりませんでした。")

if __name__ == "__main__":
    pgui.hotkey('alt', 'tab')
    pgui.alert()

    target_str = "あり"
    left, upper, right, lower = 670, 1740, 1530, 1940

    if width == 3840 and height == 2160:
        img_path = "./image/image_test.png"
    else:
        img_path = capture_screenshot()

    result = image_ocr(img_path, target_str, left, upper, right, lower)
    x, y = calculate_screen_ratio()

    if result is not None:
        new_tup = (result[0] + (left * x), result[1] + (upper * y))
        locate_click(new_tup)
    else:
        print("座標が見つかりませんでした。")
