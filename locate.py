import pyautogui as gui
import sys

print('中断するにはCtrl+Cを入力してください。')

try:
    while True:
        x=input("取得したい箇所にカーソルを当てEnterキー押してください\n")
        print(gui.position())

except KeyboardInterrupt:
    print('\n終了')
    sys.exit()