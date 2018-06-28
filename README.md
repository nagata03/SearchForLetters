# Search for Letters
======================
## Overview
フレーズと検索文字（もしくは単語）を入力し、フレーズ内にある検索文字（もしくは単語）を検索します。言語は英語を想定しています。
また、検索履歴を参照できます。  
*※本アプリケーションは書籍「Head First Python 第2版」を参考にしながら作成し、一部改良を加えたものです。*

## Demo
![demo](https://github.com/nagata03/sample_python_webapp/Demo_SearchForLetters.gif)

## Description
### search_for_letters
1. フレーズと検索文字を入力します。検索文字は複数入力できます。検索文字に記号やスペースを入れた場合、それらも検索対象となります。
2. フレーズに含まれる検索文字を抽出し、表示します。

### search_for_words
1. フレーズと検索単語を入力します。検索単語は複数入力できます。複数入力する場合ははカンマもしくは半角スペースで区切ってください。
2. フレーズ内での検索単語の出現回数を調べ、表示します。

### viewlog
1. search_for_lettersおよびsearch_for_wordsそれぞれの検索履歴を参照できます。検索履歴には*検索日時、フレーズ、検索文字（もしくは単語）、リモートアドレス、ユーザエージェント、結果*が含まれます。
2. 検索履歴を参照する場合はログインしている必要があります。

## Feature
- ほぼ、Pythonの基本的な構文だけで作成しました。
- DBアクセスにはDBアクセス用コンテキストマネージャを使用しています。
- 検索処理時に行うDBへのログ格納処理は、スレッドを使用して並列処理で行なっています。スレッドの効果を実感できるようログ格納処理にあえてスリープを入れています。

---
## Requirement
- macOS High Sierra v10.13.5 and more
- Python3 and more
- Flask
- MySQL v8.0.11 and more

## Usage
### Install third party modules
```
$ sudo -H python3 -m pip install Flask      # Flask
$ sudo -H python3 -m pip install mysql-connector-python     # MySQL-Connector/Python
.../dist$ sudo python3 -m pip install vsearch1-2.0.tar.gz   # vsearch1
```

### DB Setup
MySQLを使用します。
```
$ brew install mysql    # MySQLのインストール
$ mysql.server start    # MySQLサーバの起動
$ mysql -u root -p      # ログイン
mysql> create database vsearchlogDB;    # DBの作成
mysql> create user 'vsearch' identified by 'vsearchpasswd';     # ユーザの作成
mysql> grant all on vsearchlogDB.* to 'vsearch';    # ユーザ権限の設定
mysql> quit
$ mysql -u vsearch -p vsearchlogDB      # vsearchユーザでログイン
mysql> create table log (       # テーブル「log」を作成
    -> id int auto_increment primary key,
    -> ts timestamp default current_timestamp,
    -> phrase varchar(128) not null,
    -> letters varchar(32) not null,
    -> ip varchar(16) not null,
    -> browser_string varchar(256) not null,
    -> results varchar(64) not null );
mysql> create table log2 (      # テーブル「log2」を作成
    -> id int auto_increment primary key,
    -> ts timestamp default current_timestamp,
    -> phrase varchar(128) not null,
    -> words varchar(64) not null,
    -> ip varchar(16) not null,
    -> browser_string varchar(256) not null,
    -> results varchar(128) not null );
mysql> quit
```

### Start MySQL
```
$ mysql.server start
```

### Start WebApp
```
$ python3 vsearch4web.py
```

### Operation on Browser
URLを直接指定してください。
- localhost:5000/（もしくはlocalhost:5000/entry）-> フレーズと検索文字（もしくは単語）を入力＆検索実行
- localhost:5000/login -> ログイン
- localhost:5000/viewlog -> search_for_lettersの検索履歴を参照。ログイン状態でのみ参照可能。
- localhost:5000/viewlog2 -> search_for_wordsの検索履歴を参照。ログイン状態でのみ参照可能。
- localhost:5000/logout -> ログアウト

---
## Remaining Issues
- Webページの遷移などのUIの改善
- ログ格納処理関数の最適化
- テストコードの作成
