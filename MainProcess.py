import PySimpleGUI as sg
import pyautogui as pgui
import AutoCodeFunc


class GUI(AutoCodeFunc.StartAutomation):
    def __init__(self):
        super().__init__()
        self.logger.info("-------------------------------")
        self.logger.info("メインメニューを表示します。")
        self.logger.info("-------------------------------")

    def create_layout(self):
        GUI_TEXT_SIZE = (15, 1)
        GUI_INPUT_SIZE = (20, 5)
        GUI_FONT_SIZE = (20, 16)

        layout = [[sg.Text('プログラムを選択してください\n', font=GUI_FONT_SIZE)],
                  [sg.Text('プログラム名', size=GUI_TEXT_SIZE, font=GUI_FONT_SIZE),
                   sg.Combo(('自動再出品', '自動RAGE', '自動発送', '自動再出品(取引画面)','自動再出品(添字)'),
                            default_value='自動再出品', size=GUI_INPUT_SIZE, key='code')],
                  [sg.Text('件数', size=GUI_TEXT_SIZE, font=GUI_FONT_SIZE),
                   sg.InputText('', size=GUI_INPUT_SIZE, key='number')],
                  [sg.Text()],
                  [sg.Button('確認', font=GUI_FONT_SIZE, enable_events=True, key='confirmation', bind_return_key=True)]]
        return layout

    def gui_main(self):
        auto = AutoCodeFunc.StartAutomation

        sg.theme('DarkBlue17')

        layout = self.create_layout()

        window = sg.Window('メルカリ 作業自動化アプリ', layout, return_keyboard_events=True)

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                self.logger.info("アプリを終了します。")
                break

            if event == 'confirmation':
                if values['number'].isdecimal():
                    value = pgui.confirm(text='プログラム名 : {}\n件数 : {}件'.format(values['code'], values['number']), title='最終確認')

                    if value == 'OK':
                        auto.main(int_count=values['number'], dict_name=values['code'])
                else:
                    pgui.alert(text='数字を入力してください', title='エラー', button='OK')

        window.close()


if __name__ == "__main__":
    gui = GUI()
    gui.gui_main()
