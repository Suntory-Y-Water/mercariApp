import PySimpleGUI as sg
import pyautogui as pgui
import AutoCodeFunc


class GUI(AutoCodeFunc.StartAutomation):
    def __init__(self):
        super().__init__()
        self.logger.info("-------------------------------")
        self.logger.info("メインメニューを表示します。")
        self.logger.info("-------------------------------")

    def gui_main(self):

        auto = AutoCodeFunc.StartAutomation

        # デザインテーマの設定
        sg.theme('DarkBlue17')

        # GUIのサイズ設定
        GUI_TEXT_SIZE  = (15, 1)
        GUI_INPUT_SIZE = (20, 5)
        GUI_FONT_SIZE  = (20, 16)

        # ウィンドウの内容を定義する
        layout = [[sg.Text('■プログラムを選択してください\n', font=GUI_FONT_SIZE)],
                  [sg.Text('プログラム名', size=GUI_TEXT_SIZE, font=GUI_FONT_SIZE),
                   sg.Combo(('自動再出品', '自動RAGE', '自動発送', '自動再出品(取引画面)'),
                            default_value='自動再出品', size=GUI_INPUT_SIZE, key='code')],
                  [sg.Text('件数', size=GUI_TEXT_SIZE, font=GUI_FONT_SIZE),
                   sg.InputText('', size=GUI_INPUT_SIZE, key='number')],
                  [sg.Text()],
                  [sg.Button('確認', font=GUI_FONT_SIZE, enable_events=True, key='confirmation')]]

        # ウィンドウを作成する
        window = sg.Window('メルカリ 作業自動化アプリ', layout)

        while True:
            event, values = window.read()

            # ウィンドウのXボタンを押したときの処理
            if event == sg.WIN_CLOSED:
                self.logger.info("アプリを終了します。")
                break
            
            # 確認ボタンを押したとき
            if event == 'confirmation':

                # 件数が数字かどうか判定
                # 数字だったとき
                if values['number'].isdecimal():

                    # 最終確認のポップアップ生成
                    value = pgui.confirm(text='プログラム名 : {}\n件数 : {}件'.format(values['code'], values['number']), title='最終確認')

                    # 最終確認でOKだったとき
                    if value == 'OK':
                        auto.main(int_count=values['number'], dict_name=values['code'])
                else:
                    # 数字以外のときはエラーを表示
                    pgui.alert(text='数字を入力してください', title='エラー', button='OK')

        window.close()


if __name__ == "__main__":
    gui = GUI()
    gui.gui_main()
