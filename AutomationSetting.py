import pyautogui as pgui
import pyperclip as pyper
import Setting as set
import time
import os
from logging import getLogger, StreamHandler, DEBUG, Formatter, FileHandler


class Automation(object):

    def __init__(self):
        pgui.FAILSAFE = True
        self.width, self.height = pgui.size()

        # log.txtがなかったら作成する。
        folder_name = "log"
        file_name = "log.txt"
        file_path = os.path.join(folder_name, file_name)
        if not os.path.exists(file_path):
            os.makedirs(folder_name, exist_ok=True)
            with open(file_path, "w") as file:
                # file.write("This is a new file.")
                pass
        else:
            pass

        # ログを設定する
        self.logger = getLogger(__name__)

        # コンソールに表示する場合は StreamHandler() を使う
        # handler = StreamHandler()

        # ログファイルがあることを確認してそこに書き込む
        handler = FileHandler("./log/log.txt")


        handler.setLevel(DEBUG)
        self.logger.setLevel(DEBUG)
        for h in self.logger.handlers[:]:
            self.logger.removeHandler(h)
            h.close()
        self.logger.addHandler(handler)
        formatter = Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(message)s')
        handler.setFormatter(formatter)


    def calculate_screen_ratio(self) -> tuple:
        """_summary_

        画面サイズを取得する

        Returns:
            tuple: _description_
        """
        width, height = pgui.size()
        return width / 3840, height / 2160

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

    def reloading_page(self, image_path: str, wait_time: int = 10) -> None:
        """_summary_

        指定した画像が読み込めなかったときリロードする。

        Args:
            image_path (str): 指定した画像のPATH
            wait_time (int): リロード後の待機時間（秒）
        """
        if image_path == None:
            pgui.press('F5')
            self.logger.debug("画像が読み込めないためリロードします。")
            time.sleep(wait_time)

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

    def image_path_click(self, image_path: str, log_flag: int = 0) -> tuple:
        """_summary_

        指定した画像の座標をクリックする。
        画像が読み込めなかったときはリロードしする。
        3回連続で読み込めないときは次のページへ移動する。
        5回連続で商品を読み込めずリロードしたときは、商品が再出品できる状態ではないと判断して処理自体を終了する。

        Returns:
            locate : 指定した画像の座標
        """

        MAX_RELOAD_ATTEMPTS = 3
        MAX_NONE_PAGE_ATTEMPTS = 5

        reload_count = 0
        none_page_count = 0


        # 画像ありコピーが見つかるまで再読み込みする
        while none_page_count <= MAX_NONE_PAGE_ATTEMPTS:

            locate = pgui.locateOnScreen(image_path, grayscale=True, confidence=0.7)

            # 画像が認識できなかったとき、再度読み込みをする
            self.reloading_page(locate)
            reload_count += 1

            if locate != None:
                break

            if reload_count > MAX_RELOAD_ATTEMPTS:
                reload_count = 0
                none_page_count += 1
                pgui.hotkey('ctrl', 'w')
                self.logger.debug("3回読み込めなかったので次のタブへ移動します。")

        if none_page_count > MAX_NONE_PAGE_ATTEMPTS:
            self.logger.critical("ImageNotFoundException:指定の座標がありません。処理を強制終了します。")
            raise pgui.ImageNotFoundException

        # 再出品のときだけログを書く　初期値は0
        if log_flag == 1:
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

    def check_page(self, image_path:str) -> bool:
        """_summary_

        再出品後に画面遷移が実際にできているか確認する

        Returns:
            bool : 真偽値
        """
        if pgui.locateOnScreen(image_path, grayscale=True, confidence=0.7):
            return True

    def page_back(self, count:int) -> None:
        """_summary_
        
        ページを戻るだけ
        
        Args:
            count (int): 戻るページ数
        """
        for _ in range(count):
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
            locate: tuple = pgui.locateOnScreen('../../image/syouhinnnohensyuu.png', grayscale=True, confidence=0.7)

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
        self.image_locate_click('../../image/konosyouhinwosakujosuru.png')
        time.sleep(1)

        self.image_locate_click('../../image/sakujosuru.png')
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
        if pgui.locateOnScreen('../../image/check_relisted.png', grayscale=True, confidence=0.7):
            return True

    def comment_product(self) -> None:
        """_summary_

        出品した商品に注意書きをコメントする。
        """
        self.image_locate_click('../../image/syuppinnsyouhinwomiru.png')
        time.sleep(2)

        self.image_locate_click('../../image/komentowonyuuryoku.png')
        time.sleep(3)

        self.image_locate_click('../../image/komentoran.png')
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
        self.image_locate_click('../../image/insatu.png')
        time.sleep(1)