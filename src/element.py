import pyautogui as pgui
import pyperclip as pyper
import time
import os
from logging import getLogger, DEBUG, Formatter, FileHandler


class Automation(object):
    def __init__(self):
        pgui.FAILSAFE = True
        self.width, self.height = pgui.size()

        folder_name = "../log"
        file_names = ["log.txt", "log_products_name.txt"]

        self.create_log_files(folder_name, file_names)
        self.configure_loggers(folder_name, file_names)

    def create_log_files(self, folder_name, file_names):
        for file_name in file_names:
            file_path = os.path.join(folder_name, file_name)
            if not os.path.exists(file_path):
                os.makedirs(folder_name, exist_ok=True)
                with open(file_path, "w") as file:
                    pass

    def configure_loggers(self, folder_name, file_names):
        formatter = Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(message)s")

        self.logger = self.create_logger(
            "logger", folder_name, file_names[0], formatter, DEBUG
        )
        self.logger_products_name = self.create_logger(
            "log_products_name", folder_name, file_names[1], formatter, DEBUG
        )

    def create_logger(self, name, folder_name, file_name, formatter, level):
        logger = getLogger(name)
        logger.setLevel(level)

        for h in logger.handlers[:]:
            logger.removeHandler(h)
            h.close()

        handler = FileHandler(os.path.join(folder_name, file_name), encoding="UTF-8")
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def get_image_path(self, image_path: str) -> str:
        """_summary_

        画像取得時に画面解像度に応じて参照元を変化させる。

        Args:
            base_path (str): _description_

        Returns:
            str: _description_
        """
        if self.width == 3840 and self.height == 2160:
            return image_path
        else:
            return image_path.replace("image/", "image_1920x1080/")

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

    def reloading_page(self, image_path: str, wait_time: float = 10.0) -> None:
        """_summary_

        指定した画像が読み込めなかったときリロードする。

        Args:
            image_path (str): 指定した画像のPATH
            wait_time (float): リロード後の待機時間（秒）
        """
        if image_path == None:
            pgui.press("F5")
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

        try:
            locate = pgui.locateOnScreen(image_path, grayscale=True, confidence=0.7)
            if not locate:
                raise pgui.ImageNotFoundException

        except pgui.ImageNotFoundException:
            self.logger.error(
                f"Error: The image {image_path} was not found on the screen."
            )
            return None

        x, y = pgui.center(locate)
        pgui.click(x, y, duration=0.5)
        return (x, y)

    def image_path_click(self, image_path: str, log_flag: int = 0) -> tuple:
        """_summary_

        指定した画像の座標をクリックする。
        画像が読み込めなかったときはリロードしする。
        3回連続で読み込めないときは次のページへ移動する。
        5回連続で商品を読み込めずリロードしたときは画像がないと判断して処理自体を終了する。

        Returns:
            locate : 指定した画像の座標
        """

        MAX_RELOAD_ATTEMPTS = 3
        MAX_NONE_PAGE_ATTEMPTS = 5

        reload_count = 0
        none_page_count = 0

        # 指定した画像の座標をクリックする。
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
                pgui.hotkey("ctrl", "w")
                self.logger.debug("3回読み込めなかったので次のタブへ移動します。")

        if none_page_count > MAX_NONE_PAGE_ATTEMPTS:
            self.logger.critical("ImageNotFoundException:指定の座標がありません。処理を強制終了します。")
            raise pgui.ImageNotFoundException

        # 再出品のときだけログを書く　初期値は0
        if log_flag == 1:
            self.logger.debug("この商品を再出品します : " + self.get_log_url())

        pgui.click(locate, duration=0.5)
        return locate

    def check_page(self, image_path: str) -> bool:
        """_summary_

        再出品後に画面遷移が実際にできているか確認する

        Returns:
            bool : 真偽値
        """
        if pgui.locateOnScreen(image_path, grayscale=True, confidence=0.7):
            return True

    def page_back(self, count: int) -> None:
        """_summary_

        ブラウザ上で前のページに戻る

        Args:
            count (int): 戻るページ数
        """
        for _ in range(count):
            pgui.hotkey("alt", "left")
        self.logger.info("元の商品ページへ戻ります")

    def item_deleted(self) -> None:
        """_summary_

        商品編集画面で削除ボタンを押す。

        """
        self.image_locate_click(
            image_path=self.get_image_path("../image/konosyouhinwosakujosuru.png")
        )
        time.sleep(1)

        self.image_locate_click(
            image_path=self.get_image_path("../image/sakujosuru.png")
        )
        time.sleep(2)

    # RAGE時の値段上昇
    def rage_up(self) -> None:
        """_summary_

        RAGE時に値段を一桁上げる

        """
        pgui.write("0")
        time.sleep(0.2)

        pgui.press("enter")
        time.sleep(2)

    def go_product_page(self) -> None:
        """_summary_

        売れた商品の再出品用、取引画面なら商品ページに遷移し、商品ページならそのまま。

        """

        element: str = self.get_log_url()

        # 取引画面のとき商品ページに遷移する。商品ページの場合はそのまま。
        if "transaction" in element:
            e = element.replace("transaction", "item")
            pyper.copy(e)
            pgui.hotkey("ctrl", "l")
            pgui.hotkey("ctrl", "v")
            pgui.press("enter")

        time.sleep(6)

    def comment_product(self) -> None:
        """_summary_

        出品した商品に注意書きをコメントする。

        """
        self.image_locate_click(
            image_path=self.get_image_path("../image/syuppinnsyouhinwomiru.png")
        )
        time.sleep(2)

        self.image_locate_click(
            image_path=self.get_image_path("../image/komentowonyuuryoku.png")
        )
        time.sleep(3)

        pgui.press("tab")
        time.sleep(1)
        self.logger.info("注意書きコメントを入力")

        # 設定ファイルに記載されているコメントを貼り付ける
        with open("../setting/comment.txt", "r", encoding="utf-8") as f:
            comment = f.read()

        pyper.copy(comment)
        pgui.hotkey("ctrl", "v")
        time.sleep(1)

        # コメントを送信する
        pgui.hotkey("tab")
        pgui.hotkey("tab")
        pgui.press("enter")
        time.sleep(0.5)

    def printing_process(self) -> None:
        """_summary_

        印刷時、前の宛名を削除してペーストする。

        """
        pgui.hotkey("ctrl", "a")
        pgui.press("backspace")
        time.sleep(1)

        pgui.hotkey("ctrl", "v")
        pgui.press("backspace")
        pgui.press("up", presses=9)
        pgui.press("delete", presses=5)

    def choice_printing(self) -> None:
        """_summary_

        印刷するアイコンを選択する。

        """
        self.image_locate_click("../image/insatu.png")
        time.sleep(1)
