import pyautogui as pgui
import pyperclip as pyper
from element import Automation
import setting as set
import time


class StartAutomation(Automation):
    def __init__(self):
        super().__init__()
        

    def automatic_shipping(self) -> None:
        """_summary_

        自動発送
        Snapモードがない場合は処理を終了する。

        """

        time.sleep(2)

        self.logger.debug("この商品を発送します : " + self.get_log_url())

        # お届け先を選択しドラッグ→コピー
        self.image_locate_click(image_path=self.get_image_path('../image/otodokesaki.png'))

        time.sleep(1)

        pgui.dragTo(x=self.width * set.dragToAddressX,
                    y=self.height * set.dragToAddressY, duration=0.5)
        pgui.hotkey('ctrl', 'c')

        if self.image_locate_click(image_path='../image/snap.png') or \
            self.image_locate_click(image_path='../image/snap_write.png'):
            
            self.printing_process()
            self.choice_printing()
        else:
            pgui.confirm(text='Snapモードがありません。\n処理を終了します。', title='Error!')
            self.logger.error("Snapモードがありませんでした。処理を終了します。")
            raise pgui.ImageNotFoundException

        # 商品の発送を通知する
        self.image_locate_click(image_path=self.get_image_path('../image/hassouwotuutisuru.png'))
        time.sleep(0.2)

        self.image_locate_click(image_path=self.get_image_path('../image/hontounihassousimasitaka.png'))
        # 次の出品までのリードタイム
        time.sleep(5.0)
        pgui.hotkey('ctrl', 'w')


    def automatic_listing(self, do_not_delete_flag: int = 0) -> None:
        """_summary_
        
        自動再出品
        再出品をして出品後にコメントをし元の商品を削除する。

        Args:
            do_not_delete_flag (int, optional): _description_. Defaults to 0.
        """
        if do_not_delete_flag == 1:
            # 商品ページへ移動
            self.go_product_page()
            self.logger.info("商品ページへ移動")


        # 画像ありで再出品
        self.image_path_click(image_path=self.get_image_path('../image/mercari_copy.png'), log_flag=1)
        time.sleep(8)

        pgui.press('end')
        time.sleep(2)

        self.image_locate_click(image_path=self.get_image_path('../image/syuppinsuru.png'))
        time.sleep(5)

        # 出品ができていた場合
        if self.check_page(image_path=self.get_image_path('../image/check_relisted.png')) == True:

            self.logger.info("再出品完了")
            # コメントで注意書きをする
            self.comment_product()

            # フラグ時はそのままページを閉じる
            if do_not_delete_flag == 1:
                pgui.hotkey('ctrl', 'w')
                self.logger.info("出品後、ページを閉じました")
                return
            
            self.page_back(count=10)
            time.sleep(6)

            # コメントに被らないようにする
            pgui.moveTo(x=1800, y=1100)
            self.image_path_click(image_path=self.get_image_path('../image/syouhinnnohensyuu.png'))
            time.sleep(5)

            pgui.press('end')
            self.logger.info("商品の編集へ移動")
            time.sleep(2)

            self.item_deleted()
            self.logger.info("商品を削除しました")

            pgui.hotkey('ctrl', 'w')
            time.sleep(5)
        else:
            self.page_back(count=8)
            self.logger.debug("出品できなかったため、再度実行します。")

            if do_not_delete_flag == 1:
                self.automatic_listing(do_not_delete_flag=1)
                return
            
            self.automatic_listing()


    def automatic_rage(self) -> None:
        """_summary_

        自動RAGE
        商品の桁を一桁上げて一桁下げる。

        """
        self.logger.debug("この商品をRAGEします : " + self.get_log_url())

        time.sleep(1)

        self.image_path_click(image_path=self.get_image_path('../image/syouhinnnohensyuu.png'))
        time.sleep(5)

        pgui.press('end')
        time.sleep(2)

        self.image_locate_click(image_path=self.get_image_path('../image/hanbaikakaku.png'))
        pgui.press('end')
        pgui.write('0')
        pgui.press('enter')
        time.sleep(3)

        self.image_path_click(image_path=self.get_image_path('../image/syouhinnnohensyuu.png'))
        time.sleep(5)

        pgui.press('end')
        time.sleep(2)

        self.image_locate_click(image_path=self.get_image_path('../image/hanbaikakaku.png'))
        pgui.press('end')
        pgui.press('backspace')
        pgui.press('enter')
        time.sleep(3)

        pgui.hotkey('ctrl', 'w')


    def automatic_listing_with_index(self) -> None:
        """_summary_

        自動再出品(添字つける)
        商品を再出品して、商品名に添え字をつける。

        """
        # 商品ページへ移動
        self.go_product_page()
        self.logger.info("商品ページへ移動")

        # 画像ありで再出品
        self.image_path_click(image_path=self.get_image_path('../image/mercari_copy.png'), log_flag=1)
        time.sleep(8)

        pgui.press('pagedown')
        time.sleep(2)
        
        # 商品名を選択
        self.image_path_click(image_path=self.get_image_path('../image/syouhinmei.png'))

        # 出品する商品名をログに書き込む
        pgui.hotkey('ctrl', 'a')
        pgui.hotkey('ctrl', 'c')
        element = pyper.paste()
        self.logger_products_name.info(element)

        # 商品名の最後に「a」を入れる
        pgui.press('end')
        pgui.keyDown('shift')
        pgui.write(' a')
        pgui.keyUp('shift')
        pgui.press('enter', presses=2)
        time.sleep(5)

        # 出品ができていた場合
        if self.check_page(image_path=self.get_image_path('../image/check_relisted.png')) == True:
            
            self.logger.info("再出品完了")            
            # コメントで注意書きをする
            self.comment_product()

            pgui.hotkey('ctrl', 'w')
            self.logger.info("出品後、ページを閉じました")
        else:
            self.page_back(count=8)
            self.logger.debug("出品できなかったため、再度実行します。")
            self.automatic_listing_with_index()


    def main(int_count: int, dict_name: str) -> None:
        """_summary_

        mainメソッド
        GUIで実行するメソッド名を指定する。

        Args:
            int_count (int): 商品の件数
            dict_name (str): 実行するメソッド名

        Raise:
            FailSafeException: フェイルセーフ発動時にメインメニューへ戻る
        """
        auto = StartAutomation()
        page_count: int = 0

        func_dict: dict = {
            '自動再出品': auto.automatic_listing,
            '自動RAGE': auto.automatic_rage,
            '自動発送': auto.automatic_shipping,
            '自動再出品(取引画面)': lambda: auto.automatic_listing(1),
            '自動再出品(添字)': auto.automatic_listing_with_index
        }

        # Google Chromeのページに移動する
        pgui.keyDown('alt')  # altキーを押しっぱなしにしてtabを二回押す
        pgui.press('tab')
        pgui.keyUp('alt')
    
        try:
            while int(int_count) > page_count:
                if int_count.isdecimal():
                    func = func_dict.get(dict_name)  # 辞書から関数を取得
                    if func:
                        func()  # 関数を実行
                    else:
                        pgui.alert(text='正しくプログラム名を入力してください。', title='エラー', button='OK')
                        break

                    page_count += 1
                else:
                    pgui.alert(text='数字を入力してください', title='エラー', button='OK')
                    break

                if int(int_count) == page_count:
                    pgui.alert(text='処理が終了しました', title='終了通知', button='OK')
                    auto.logger.info("処理が終了しました。メインメニューに戻ります。")
                    return
        
        # 画像読み込めないとかそういったとき
        except Exception as e:
            auto.logger.error(e)
            auto.logger.error("例外を検知しました。強制終了します。")
            pgui.alert(text='例外を検知しました。強制終了します。', title='エラー', button='OK')
            return