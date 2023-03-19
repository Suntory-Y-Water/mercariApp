from PIL import Image
import os
import pyocr
import pyocr.builders
import Setting as set
import pyautogui as pgui

# インストール済みのTesseractへパスを通す
path_tesseract = "C:\\Program Files\\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

# OCRエンジンの取得
tools = pyocr.get_available_tools()
tool = tools[0]


def calculate_screen_ratio() -> int:

    """_summary_

    取得した画面解像度の比率を計算する

    Returns:
        _type_: _description_
        
    """

    # 画面サイズを取得する
    width, height = pgui.size()
    
    # 元の画面サイズから解像度を表示
    calculate_screen_X : int = width / 3840
    calculate_screen_Y : int = height / 2160

    return calculate_screen_X, calculate_screen_Y


def image_ocr(path):

    # 座標の基準値となる値
    left : int = 670
    upper : int = 1740
    right : int = 1530
    lower : int = 1940

    x, y = calculate_screen_ratio()

    print("比率は", x, y)

    # 画像の読み込み
    img_org = Image.open(path)

    # グレースケールに変換
    img_gray =img_org.convert("L")

    # 画像の切り抜き
    img_crop = img_gray.crop((left * x, upper * y, right * x, lower * y))

    # 切り抜いた画像の確認
    img_crop.save('./image/image_test_crop.png')

    # OCRの実行
    builder = pyocr.builders.WordBoxBuilder(tesseract_layout=6)
    result = tool.image_to_string(img_crop, lang="jpn", builder=builder)

    target_str = 'あり'
    for line in result:
        if target_str in line.content:
            print("画像ありの画面位置は", line.position[0], "です")
            return line.position[0]
    

def locate_click(box:tuple):

    result = box
    print(result)

    pgui.hotkey('alt', 'tab')
    pgui.alert()

    # locate = pgui.moveTo(result[0], result[1])


if __name__ == "__main__":
    result = image_ocr("./image/image_test.png")
    x, y = calculate_screen_ratio()
    print("元の座標", result)
    print(x, y)
    
    new_tup = (result[0] + (670 * x), result[1] + (1740 * y))
    print("新しい座標", new_tup)
    locate_click(result)
    pgui.moveTo(new_tup)
    