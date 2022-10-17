# Djangoフレームワークによる店舗用Web予約システム

## 概要

YouTubeで発信されている徳田啓（トクダ　ケイ）さんによる「店舗用Web予約システム」の開発をPythonのDjangoフレームワークで開発してみました。

↓↓↓
- [【開発実況シリーズ】店舗用Web予約システムを作る#1 企画編【プログラミング】](https://www.youtube.com/watch?v=V7aiz1JfMHw)

上記動画では以下のようなプログラムによって「企画」～「テスト＆仮運用」までの工程を解説しながら開発を行ってくれています（2022/10/17時点では[【開発実況シリーズ】店舗用Web予約システムを作る「#13 機能実装（DB登録処理）編」](https://www.youtube.com/watch?v=Dww3l7pGX6Y)まででした）。

|ツール|ツール名|
|----|----|
|IDE|VSCode|
|データベース|MySQL|
|プログラミング言語|PHP|
|フロント（UI）|BootStrap|

私はPython使いであるためアイディア等を参考にさせて頂き、プログラミング言語のPHPの部分を**PythonのDjangoフレームワーク**に置き換えて開発を行ってみました。

## 各アクセス先のご紹介

ご紹介といっても、YouTubeで発信されている徳田啓さんが作成したUIをそのまま真似しているのでご了承ください。

機能に関しては泥臭さもありますが試行錯誤しながら実装しました。

### 顧客用の予約画面（index）

![reserve_index](https://user-images.githubusercontent.com/51676019/196092889-3957fe3f-1340-45af-a82c-097435b2f4ed.jpg)

![reserve_index_2](https://user-images.githubusercontent.com/51676019/196093156-0ac9edff-07d2-4fd3-9f4c-e553439f5a1b.jpg)

![reserve_index_3](https://user-images.githubusercontent.com/51676019/196093180-07bd27cf-dd88-4508-99da-9cada54d2484.jpg)

### 顧客用の予約確認画面（confirm）

### 顧客用の予約完了画面（complete）

### 店舗用のログイン画面（login）

### 店舗用の予約リスト画面（reserve_list）

### 店舗用の設定画面（setting/id/）
