# Djangoフレームワークによる店舗用Web予約システム（未完成）

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

「/index」のURL部分では顧客が入力するための予約画面です。

[上部]

![reserve_index](https://user-images.githubusercontent.com/51676019/196092889-3957fe3f-1340-45af-a82c-097435b2f4ed.jpg)

[下部]

![reserve_index_2](https://user-images.githubusercontent.com/51676019/196093156-0ac9edff-07d2-4fd3-9f4c-e553439f5a1b.jpg)

「備考欄」以外のフォームは必須なため、入力せずに「確認画面へ」のボタンをクリックしてしまうとエラーが発生します。

![reserve_index_3](https://user-images.githubusercontent.com/51676019/196093180-07bd27cf-dd88-4508-99da-9cada54d2484.jpg)

### 顧客用の予約確認画面（confirm）

予約画面での入力フォームデータが問題無くクリアされ、予約確認画面へ遷移されると「/confirm」というURLにリダイレクトされます。

以下は正常に表示された場合の画です。

![reserve_confirm](https://user-images.githubusercontent.com/51676019/196093383-94f1dc0f-0922-45d8-9db8-d8d3a586eb3d.jpg)

エラーが発生した場合は以下のようにアラートが表示されます。このエラーの内容は店舗側で行える「設定」によって時間当たりの予約人数を「５」に設定しており、既にこの日付けと時間では「１人」の予約が完了されているので、「５人」以上での予約は受け付けできないという事になります。

![reserve_confirm_2](https://user-images.githubusercontent.com/51676019/196093398-6a5ee77d-d28b-4775-831b-857d5eca9fcf.jpg)

確認画面から「戻る」ボタンをクリックすると、入力したデータが保持された状態で再入力を行えます。

![reserve_confirm_3](https://user-images.githubusercontent.com/51676019/196093417-b1dfe2b3-cdc7-4b49-8e1b-869307d858ae.jpg)

### 顧客用の予約完了画面（complete）

「予約完了」ボタンがクリックされると、顧客が入力した「Email」アドレス宛と店舗側のメールアドレスへ予約完了メールが送信されます。それと同時に「/complete」のURLへアクセスされ以下のような画面にリダイレクトされます。

![reserve_complete](https://user-images.githubusercontent.com/51676019/196093506-fc8d16ca-b832-47f0-8a18-b85a73ecae1c.jpg)

### 店舗用のログイン画面（login）

店舗側の人間がシステムにログインするために「/login」URLにアクセスするか、予約リストを確認できる「/reserve_list」URLにアクセスするとログイン画面が表示されます。

ログインが完了すると、予約リストの「/reserve_list」URLへリダイレクトされます。

![reserve_login](https://user-images.githubusercontent.com/51676019/196093533-dc87f959-cd41-49d6-b553-0c40674c9ac4.jpg)

### 店舗用の予約リスト画面（reserve_list）

予約リストでは当日以降のリストをデフォルトで表示しています。

![reserve_reserve_list](https://user-images.githubusercontent.com/51676019/196093557-24a5840e-d629-4ad3-9eb0-e499093f8884.jpg)

プルダウンで設置してある西暦と月で絞り込みが容易にできるように非同期処理でリストを表示できるようにしています。

![reserve_reserve_list_2](https://user-images.githubusercontent.com/51676019/196093567-7f4ab81b-7c94-436d-88f2-1060f6446f60.jpg)

### 店舗用の設定画面（setting/id/）

設定画面では、プルダウンによって予約に関する設定を行えます。

設定画面で設定項目を選択するには管理画面での初設定が必要になるため、管理者は予め各種項目をデータベースに保存しておきます。

![reserve_setting](https://user-images.githubusercontent.com/51676019/196093575-c3dfff41-04be-428b-9ca6-132f2c35f281.jpg)
