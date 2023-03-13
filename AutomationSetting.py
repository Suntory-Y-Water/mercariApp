import pyautogui as pgui
import pyperclip as pyper
import Setting as set
import time
import os
from logging import getLogger, StreamHandler, DEBUG, Formatter, FileHandler


class Automation(object):

    def __init__(self):
        self.window_size_x, self.window_size_y = pgui.size()
        pgui.FAILSAFE = True

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


    def get_window_size_x(self, x):
        x = self.window_size_x * x
        return x

    def get_window_size_y(self, y):
        y = self.window_size_y * y
        return y

    def get_log_url(self) -> str:
        """_summary_

        ログ記載用のURLを取得する。

        Returns:
            element : 現在のURL
        """
        pgui.hotkey("ctrl", "l")
        pgui.hotkey("ctrl", "c")

        element = pyper.paste()
        return element

    def reloading_page(self, is_image: str) -> None:
        """_summary_

        指定した画像が読み込めなかったときリロードする。

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
        画像が読み込めなかったときはリロードしする。
        3回連続で読み込めないときは次のページへ移動する。
        5回連続で商品を読み込めずリロードしたときは、商品が再出品できる状態ではないと判断して処理自体を終了する。

        Returns:
            locate : 画像あり再出品の座標を返す。
        """

        reload_count : int = 0
        none_page_count : int = 0

        # 画像ありコピーが見つかるまで再読み込みする
        while(True):
            locate : tuple = pgui.locateOnScreen('./image/mercari_copy.png', grayscale=True, confidence=0.7)

            # 画像が認識できなかったとき、再度読み込みをする
            self.reloading_page(locate)
            reload_count += 1
            
            if locate != None:
                break

            if reload_count > 3:
                reload_count = 0
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
        return self.image_locate_click('./image/syuppinsuru.png')

    def check_page(self, image_path: str) -> bool:
        """_summary_

        再出品後に画面遷移が実際にできているか確認する

        Returns:
            bool : 真偽値
        """
        if pgui.locateOnScreen(image_path, grayscale=True, confidence=0.7):
            return True

    def page_back(self) -> None:
        """_summary_

        再出品完了後元の商品ページに戻る。
        ログを取るためにURLを参照して置換したほうがミスがなくなるかもしれないので要検討

        """
        for _ in range(5):
            pgui.hotkey('alt', 'left')

    # 商品の編集を選択する
    def edit_products_click(self) -> tuple:
        """_summary_

        商品を編集するを選択する。
        画像が読み込めなかったときはリロードし、5回連続で読み込めなかったときはページを閉じて処理を終了する。

        Returns:
            locate : 「商品を編集する」の座標を返す。
        """

        # 商品を編集するが見つかるまで再読み込みする
        while(True):
            locate: tuple = pgui.locateOnScreen('./image/syouhinnnohensyuu.png', grayscale=True, confidence=0.7)

            reload_count: int = 0

            # 画像が認識できなかったとき、再度読み込みをする
            self.reloading_page(locate)
            reload_count += 1

            if locate != None:
                break

            if reload_count > 5:
                break

        pgui.click(locate, duration=0.5)
        return locate

    def item_deleted(self) -> None:
        """_summary_

        商品編集画面で削除ボタンを押す。

        """
        self.image_locate_click('./image/konosyouhinwosakujosuru.png')
        time.sleep(1)

        self.image_locate_click('./image/sakujosuru.png')
        time.sleep(2)

    def go_page(self) -> None:
        """_summary_

        現在のページから実行するGooglechromeのタブへ移動する。

        """
        pgui.keyDown('alt')  # altキーを押しっぱなしにしてtabを二回押す
        pgui.press('tab')
        pgui.keyUp('alt')

    # RAGE時の値段上昇
    def rage_up(self) -> None:
        """_summary_

        RAGE時に値段を一桁上げる

        """
        pgui.write('0')
        time.sleep(0.2)

        pgui.press('enter')
        time.sleep(2)

    def go_product_page(self) -> None:
        """_summary_

        売れた商品の再出品用、取引画面なら商品ページに遷移し、商品ページならそのまま。

        """

        element : str = self.get_log_url()
        
        # 取引画面のとき商品ページに遷移する。商品ページの場合はそのまま。
        if "transaction" in element:
            e = element.replace("transaction", "item")
            pyper.copy(e)
            pgui.hotkey('ctrl', 'l')
            pgui.hotkey('ctrl', 'v')
            pgui.press('enter')
        
        time.sleep(10)

    def check_listed(self) -> bool:
        """_summary_

        再出品ができているか確認する。

        Returns:
            bool: 売れていたらTrueを返す。
        """
        if pgui.locateOnScreen('./image/check_relisted.png', grayscale=True, confidence=0.7):
            return True

    def comment_product(self) -> None:
        """_summary_

        出品した商品に注意書きをコメントする。
        """
        self.image_locate_click('./image/syuppinnsyouhinwomiru.png')
        time.sleep(2)

        self.image_locate_click('./image/komentowonyuuryoku.png')
        time.sleep(3)

        self.image_locate_click('./image/komentoran.png')
        time.sleep(1)

        # 設定ファイルに記載されているコメントを貼り付ける
        pyper.copy(set.comment)
        pgui.hotkey('ctrl', 'v')
        time.sleep(1)

        # コメントを送信する
        pgui.hotkey('tab')
        pgui.hotkey('tab')
        pgui.press('enter')
        time.sleep(0.5)

    def printing_process(self) -> None:
        """_summary_

        印刷時、前の宛名を削除してペーストする。

        """
        pgui.hotkey('ctrl', 'z')
        time.sleep(1)

        pgui.hotkey('ctrl', 'v')

    def choice_printing(self) -> None:
        """_summary_

        印刷するアイコンを選択する。

        """
        self.image_locate_click('./image/insatu.png')
        time.sleep(1)