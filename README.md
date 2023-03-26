# MercariAutoApp

# 1.概要

[フリマアシスト](https://chrome.google.com/webstore/detail/%E3%83%95%E3%83%AA%E3%83%9E%E3%82%A2%E3%82%B7%E3%82%B9%E3%83%88/jcbljdgnpcckiamdgmnfhijgkkaogmgg)を用いたメルカリの出品作業を自動化するアプリケーションです。

# 2. 使用方法

Microsoft Edgsで商品を新しいタブで開いてください。
> Google Chromeはページが重いため、Edgs推奨

複数個商品ページを開き終わったらアプリケーションを実行し、件数を入力してください。

# 3. 動作環境

- Windows 11

## 画面解像度:画面拡大比率:ブラウザの拡大比率

**ここを守らないと動きません。**

- 3840 x 2160 : 225% : 100%
- 1920 x 1080 : 100% : 100%

# 4. 実行方法

下記階層にある.exeを実行してください。
``` cmd
dist/MainProcess/MainProcess.exe
```

**2023/03/26時点、他の環境では動作確認をしていません。**

# 5. プログラム概要

## 自動再出品

出品する商品のURLを取得して、ログファイルに書き込みます。

その後、商品ページで【画像あり】再出品を選択し、出品した商品へ注意書きコメントを入力します。

入力後、元の商品ページへ戻り重複を防止するため削除します。

## 自動RAGE

**RAGE = 商品価格を更新して、タイムラインの一番上に表示させること**

RAGEする商品のURLを取得して、ログファイルに書き込みます。

その後、商品ページで**商品の編集**を選択し、値段を上げます。

値段を上げたのち、商品ページで**商品の編集**を選択し元の値段に戻します。
> 値下げ(100円以上)をすると、タイムライン上部に商品が表示されます(例外あり)。

## 自動発送

**発送の手順が個人で異なるため、開発者以外は実行非推奨。**

## 自動再出品(取引画面)

**通常の再出品と異なり、既に売れた商品に対して使用します。**

取引画面からも使用可能で、実行時に取引画面であれば商品ページに遷移します。

出品した商品のURLを取得して、ログファイルに書き込みます。

その後、商品ページで【画像あり】再出品を選択し、出品した商品へ注意書きコメントを入力します。
入力後、商品ページを閉じます。
> 元の商品を削除しないのは、既に売れている商品を対象にしているためです。


# 6. tree(必要なもの以外省略)

``` cmd
D:.
│   .gitignore
│   AutoCodeFunc.py
│   AutomationSetting.py
│   LICENSE
│   MainProcess.py
│   MainProcess.spec
│   README.md
│   Setting.py
│   
├───build
│   └───MainProcess
│               
├───dist
│   └───MainProcess
│       │      MainProcess.exe
│       └───log
│              log.txt
├───image
│       check_relisted.png
│       hanbaikakaku.png
│       hassouwotuutisuru.png
│       henkousuru.png
│       hontounihassousimasitaka.png
│       hutuuyuubin.png
│       image_test.png
│       image_test_crop.png
│       insatu.png
│       komentoran.png
│       komentowonyuuryoku.png
│       konosyouhinwosakujosuru.png
│       kousinsuru.png
│       mercari_copy.png
│       otodokesaki.png
│       sakujosuru.png
│       snap.png
│       snap_write.png
│       syouhinnnohensyuu.png
│       syuppinnsyouhinwomiru.png
│       syuppinsuru.png
│       
├───image_1920x1080
│       check_relisted.png
│       hanbaikakaku.png
│       hassouwotuutisuru.png
│       henkousuru.png
│       hontounihassousimasitaka.png
│       hutuuyuubin.png
│       insatu.png
│       komentoran.png
│       komentowonyuuryoku.png
│       konosyouhinwosakujosuru.png
│       kousinsuru.png
│       mercari_copy.png
│       otodokesaki.png
│       sakujosuru.png
│       snap.png
│       snap_write.png
│       syouhinnnohensyuu.png
│       syuppinnsyouhinwomiru.png
│       syuppinsuru.png
│       
└───setting
       comment.txt
```
