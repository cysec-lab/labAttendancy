# Attendance Recoder

学生証をタッチするとスプレッドシートに入退室時間を記録してくれるスクリプト

## 環境

- GoogleSpreadSheet
  - 出欠記録用
- 学生証読み取り側
  - Python3.8.5
    - `pip install -U nfcpy requests`
  - NFCを読み取るための設定諸々
    - [https://nfcpy.readthedocs.io/](https://nfcpy.readthedocs.io/en/latest/topics/get-started.html)

## Usage

- GoogleSpreadSheet
  - `NameList` というシートを作り学籍番号、名前のリストを作る
    ```
    6611XXXXXXX HogeHoge
    2600YYYYYYY HugaHuga
    ...
    ```
  - [script.gs](/gas/script.gs) をスプレッドシートのスクリプトに追加
    - `spreadsheetId` にSpreadSeetのURLを貼り付け
    - `lab_name` に記録する人々の研究室の名前を入れる
  - Webアプリとして公開
- 学生証読み取り側
  - `config.py`
    - URLにGoogleAppScriptの公開URLを貼り付ける
  - `$ python labAttendancy.py`

## Common Problems

- NFCが読み込めなくなった場合
  - NFCリーダをPythonから使うためにデバイスドライバを入れ替えたりしている
  - [環境](環境) にかかれているNFCをを読み取るための設定諸々から設定をし直す必要あり
