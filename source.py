import os
import time
import Setting as set
import pyautogui as pgui
import pyperclip as pyper

from logging import getLogger, StreamHandler, DEBUG, Formatter, FileHandler

class Automation(object):
    def __init__(self) -> None:

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


    def get_product_url(self) -> str:
        """_summary_

        ログ記載用のURLを取得する。

        Returns:
            element : 現在のURL

        """
        pgui.hotkey("ctrl", "l")
        pgui.hotkey("ctrl", "c")

        element = pyper.paste()
        return element
    

    def reloading_page(self, is_image:str) -> None:
        """_summary_

        指定した画像が読み込めなかったときリロードする。
        2023/03/14
        ここを少し変えたい
            無限にリロードする可能性があるので、例外処理として別で組み込めないか？

        Args:
            is_image (str): 指定した画像のPATH

        """
        if is_image == None:
            pgui.press('F5')
            self.logger.debug("画像が読み込めないためリロードします。")
            time.sleep(10)


    def image_locate_click(self, image_path: str) -> tuple:
        """_summary_

        Webページ内に該当する画像を認識し、その座標をクリックする。

        Args:
            image_path (str): 指定した画像のPATH

        Returns:
            tuple: 画像の座標

        """

        locate = pgui.locateOnScreen(image_path, grayscale=True, confidence=0.7)

        if locate == None:
            raise pgui.ImageNotFoundException
        
        pgui.click(locate, duration=0.5)
        return locate


    def re_listed_with_image(self) -> tuple:
        """_summary_

        画像あり再出品をする。
        画像が読み込めなかったときはリロードする。

        3回連続で読み込めないときは、次のページへ移動する。
        5回連続で読み込めないときは、商品が再出品できる状態ではないと判断して処理を終了する。

        Returns:
            locate : 画像あり再出品の座標を返す。

        Raise:
            ImageNotFoundException : 画像が見つからない

        """

        reload_count : int = 0
        none_page_count : int = 0

        # 画像ありコピーが見つかるまで再読み込みする
        while(True):
            locate : tuple = pgui.locateOnScreen('../../image/mercari_copy.png', grayscale=True, confidence=0.7)

            # 画像が認識できなかったとき、再度読み込みをする
            self.reloading_page(locate)

            # 読み込み回数をカウント
            reload_count += 1
            
            if locate != None:
                break

            if reload_count > 3:
                reload_count = None
                none_page_count += 1
                pgui.hotkey('ctrl', 'w')
                self.logger.debug("3回読み込めなかったので次のタブへ移動します。")

            if none_page_count > 5:
                self.logger.error("再出品可能な状態ではありません。処理を強制終了します。")
                self.logger.error("ImageNotFoundException")
                raise pgui.ImageNotFoundException
        
        self.logger.debug("この商品を再出品します : " + self.get_log_url())

        pgui.click(locate, duration=0.5)
        return locate
    

    def button_click_listing(self) -> tuple:
        """_summary_

        出品するを選択する

        Returns:
            tuple :「出品する」の座標を返す。

        """
        return self.image_locate_click('../../image/syuppinsuru.png')