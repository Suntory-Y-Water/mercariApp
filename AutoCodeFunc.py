import pyautogui as pgui
import AutomationSetting
import Setting as set
import time


class StartAutomation(AutomationSetting.Automation):
    def __init__(self):
        super().__init__()
        pgui.FAILSAFE = True

    def automatic_shipping(self) -> None:
        """_summary_

        自動発送
        Snapモードがない場合は処理を終了する。

        """

        time.sleep(2)

        self.logger.debug("この商品を発送します : " + self.get_log_url())

        # お届け先を選択しドラッグ→コピー
        self.image_locate_click('../../image/otodokesaki.png')
        self.image_locate_click('../../image/otodokesaki.png')
        time.sleep(1)

        pgui.dragTo(x=self.width(set.dragToAddressX),
                    y=self.height(set.dragToAddressY), duration=0.5)
        pgui.hotkey('ctrl', 'c')

        if self.image_locate_click('../../image/snap.png') or \
            self.image_locate_click('../../image/snap_write.png'):
            
            self.printing_process()
            self.choice_printing()
        else:
            pgui.confirm(text='Snapモードがありません。\n処理を終了します。', title='Error!')
            self.logger.error("Snapモードがありませんでした。処理を終了します。")
            return

        # 商品の発送を通知する
        self.image_locate_click('../../image/hassouwotuutisuru.png')
        time.sleep(0.2)

        self.image_locate_click('../../image/hontounihassousimasitaka.png')
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

        # 画像ありで再出品
        self.image_path_click(image_path='../../image/mercari_copy.png', log_flag=1)
        time.sleep(6)

        pgui.press('end')
        time.sleep(2)

        self.button_click_listing()
        time.sleep(5)

        # 出品ができていた場合
        if self.check_page('../../image/check_relisted.png') == True:
            
            # コメントで注意書きをする
            self.comment_product()

            # フラグ時はそのままページを閉じる
            if do_not_delete_flag == 1:
                pgui.hotkey('ctrl', 'w')
                return
            
            self.page_back(count=8)
            time.sleep(6)

            self.image_path_click(image_path='../../image/syouhinnnohensyuu.png')
            time.sleep(5)

            pgui.press('end')
            time.sleep(2)

            self.item_deleted()
            pgui.hotkey('ctrl', 'w')
            time.sleep(5)
        else:
            self.page_back(5)
            self.logger.debug("出品できなかったため、再度実行します。")

            if do_not_delete_flag == 1:
                self.automatic_listing_sold_product()
                return
            
            self.automatic_listing()


    def automatic_listing_sold_product(self):
        """_summary_

        取引画面 or 商品ページから自動再出品
        売り切れた商品が対象なため、出品後の商品削除は行わない。

        """

        # 商品ページへ移動
        self.go_product_page()

        # 画像ありで再出品
        self.image_path_click()
        time.sleep(6)

        # らくらくメルカリ便に変更される障害に対応するため、発送方法を普通郵便に変更する
        pgui.press('pagedown', presses=2)
        time.sleep(0.5)
        self.image_locate_click('../../image/henkousuru.png')
        time.sleep(0.5)
        pgui.press('end')
        time.sleep(1)

        self.image_locate_click('../../image/hutuuyuubin.png')
        self.image_locate_click('../../image/kousinsuru.png')

        time.sleep(3)

        pgui.press('end')
        time.sleep(2)

        self.button_click_listing()
        time.sleep(5)

        # 出品できているかの処理
        self.check_page('../../image/check_relisted.png')

        # 出品ができていた場合コメントをする
        if self.check_page('../../image/check_relisted.png') == True:
            self.comment_product()
            pgui.hotkey('ctrl', 'w')
        else:
            for _ in range(5):
                pgui.hotkey('alt', 'left')
            time.sleep(5)

            self.logger.debug("出品できなかったため、再度実行します。")
            self.automatic_listing_sold_product()


    def automatic_rage(self) -> None:
        """_summary_

        自動RAGE
        商品の桁を一桁上げて一桁下げる。

        """
        self.logger.debug("この商品をRAGEします : " + self.get_log_url())

        time.sleep(1)

        self.edit_products_click()
        time.sleep(5)

        pgui.press('end')
        time.sleep(2)

        self.image_locate_click('../../image/hanbaikakaku.png')
        pgui.press('end')
        pgui.write('0')
        pgui.press('enter')
        time.sleep(3)

        self.edit_products_click()
        time.sleep(5)

        pgui.press('end')
        time.sleep(2)

        self.image_locate_click('../../image/hanbaikakaku.png')
        pgui.press('end')
        pgui.press('backspace')
        pgui.press('enter')
        time.sleep(3)

        pgui.hotkey('ctrl', 'w')


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
            '自動再出品(取引画面)': lambda: auto.automatic_listing(1)
        }

        try:
            # Google Chromeのページに移動する
            auto.go_page()

            while int(int_count) > page_count:
                if int_count.isdecimal():
                    func = func_dict.get(dict_name)  # 辞書から関数を取得
                    if func:
                        func()  # 関数を実行
                    else:
                        pgui.alert(text='指定されたメソッド名が見つかりませんでした', title='エラー', button='OK')
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