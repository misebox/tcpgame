2021.5.22

# TCPで通信する簡単なゲームを作る。

## 概要
- 最初はジャンケンとかで良い
- せっかく通信するので、クロスプラットフォームにする。
- windows - linux でやるので、簡単なprintだけでやる。


## 設計

CLI ---- SERVER  ---- CLI

server


- 接続前

server
- 起動
- listen開始
- receive
- お互いの名前
- game開始

cli
- 設定ファイルで自分の名前と接続先を指定
- 自分のソケット情報（IP, port）を貰う
- 接続先へ自分の名前をsend
- 
- 相手の名前を取得
- ゲーム開始



メッセージの種類
- OK
- ERROR
- welcome
- register
- create_game
- res_create_game
- list_game
- res_list_game
- join_game
- ready_game
- start_game
- action
- result
- score

メッセージ
- sender
- kind
- params(dict)
- timestamp

メッセージプロトコル
- client: (connect) --> server: welcome --> client: register

cli:connect: [Welcome, register, OK]
cli:create_game: [OK]
srv:start_game: [Game, OK]

課題

2021.6.5

メッセージクラスを作った。



次回
create_game
ready_game
timeout
input


2021.6.12
メッセージのフローが必要？

