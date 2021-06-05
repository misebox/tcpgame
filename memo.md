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
- welcome
- register
- create_game
- list_game
- join_game
- start_game
- action
- result
- score

メッセージ
- sender
- kind
- params(dict)
- timestamp


課題