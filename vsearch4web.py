from flask import Flask, render_template, request, escape, session, copy_current_request_context
from vsearch1 import search_for_letters, search_and_count_words  # 自作モジュール
from DBcm import UseDataBase, ConnectionError, CredentialsError, SQLError   # 自作モジュール
from checker import check_logged_in # 自作モジュール
from threading import Thread
from time import sleep

app = Flask(__name__)

# データベース接続情報の設定
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB',}

# このWebアプリの秘密鍵の設定
app.secret_key = 'YouWill#NeverGuess%MySecretKey'


# ログインページ
@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return '現在ログインしています。'


# ログアウトページ
@app.route('/logout')
def do_logout() -> str:
    if 'logged_in' not in session.keys():
        return 'ログインしていません。'
    session.pop('logged_in')    # sessionからlogged_inキーを削除
    return 'ログアウトしました。'


@app.route('/')
@app.route('/entry')    # entry_page関数に2つのURLをマッピング
def entry_page() -> str:
    """ SearchForLettersアプリのホーム画面（入力画面） """
    return render_template('entry.html', the_title='「SearchForLetters」にようこそ！')


@app.route('/search4', methods=['POST'])  # URL「/search4」をdo_search関数にマッピング。POSTメソッドだけをサポート。
def do_search() -> str:
    """ 文字検索処理を行い、結果をレンダリングする """

    @copy_current_request_context   # アクティブなHTTPリクエストを、その後にスレッド内で関数を実行した時でもアクティブのままにするデコレータ
    def log_request(req: 'flask_request', res: str) -> None:
        """ Webリクエストの詳細とレスポンスをロギングする """
    #    with open('vsearch1.log', 'a') as log:
    #        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')
        sleep(15)   # スレッドの効果を確認するためのスリープ
        try:
            with UseDataBase(app.config['dbconfig']) as cursor: # 自作のコンテキストマネージャ(UseDataBase)を使用する
                _SQL = """insert into log
                            (phrase, letters, ip, browser_string, results)
                            values
                            (%s, %s, %s, %s, %s)"""
                cursor.execute(_SQL, (req.form['phrase'],
                                      req.form['letters'],
                                      req.remote_addr,
                                      req.user_agent.browser,
                                      res, ))
        except Exception as err:
            print('※※※※※ ロギング処理でエラーが発生しました。', str(err))

    phrase = request.form['phrase'] # Flaskの組み込みオブジェクト「request」の辞書属性「form」を使う
    letters = request.form['letters']
    title = '検索結果：'
    results = str(search_for_letters(phrase, letters))
    try:
        t = Thread(target=log_request, args=(request, results)) # スレッドを使う
        t.start()
    except Exception as err:
        print('※※※※※ ロギング処理のスケジューリングでエラーが発生しました。:', str(err))
    return render_template('results.html',
                            the_title=title,
                            the_phrase=phrase,
                            the_letters=letters,
                            the_results=results,)


@app.route('/search42', methods=['POST'])
def do_search2() -> str:
    """ 単語検索＆カウント処理を行い、結果をレンダリングする """

    @copy_current_request_context   # アクティブなHTTPリクエストを、その後にスレッド内で関数を実行した時でもアクティブのままにするデコレータ
    def log_request2(req: 'flask_request', res: str) -> None:
        """ Webリクエストの詳細とレスポンスをロギングする """
        sleep(15)   # スレッドの効果を確認するためのスリープ
        try:
            with UseDataBase(app.config['dbconfig']) as cursor: # 自作のコンテキストマネージャ(UseDataBase)を使用する
                _SQL = """insert into log2
                            (phrase, words, ip, browser_string, results)
                            values
                            (%s, %s, %s, %s, %s)"""
                cursor.execute(_SQL, (req.form['phrase'],
                                      req.form['words'],
                                      req.remote_addr,
                                      req.user_agent.browser,
                                      res, ))
        except Exception as err:
            print('※※※※※ ロギング処理でエラーが発生しました。', str(err))

    phrase = request.form['phrase']
    words = request.form['words']
    title = '検索結果：'
    results = str(search_and_count_words(phrase, words))
    try:
        t = Thread(target=log_request2, args=(request, results)) # スレッドを使う
        t.start()
    except Exception as err:
        print('※※※※※ ロギング処理のスケジューリングでエラーが発生しました。:', str(err))
    return render_template('results.html',
                            the_title=title,
                            the_phrase=phrase,
                            the_letters=words,
                            the_results=results,)


@app.route('/viewlog')
@check_logged_in    # ログインしている場合のみログの閲覧を可能にするデコレータ
def view_the_log() -> 'html':
    """ 文字検索処理の有用な内容をHTMLテーブルで表示する """
#    contents = []
#    with open('vsearch1.log') as log:
#        for line in log:
#            contents.append([])
#            for item in line.split('|'):
#                contents[-1].append(escape(item))
    try:
        with UseDataBase(app.config['dbconfig']) as cursor:
            _SQL = """select ts,  phrase, letters, ip, browser_string, results from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ['検索日時', 'フレーズ', '検索文字', 'リモートアドレス', 'ユーザエージェント', '結果']
        return render_template('viewlog.html',
                                the_title='ログの閲覧',
                                the_row_titles=titles,
                                the_data=contents)
    except CredentialsError as err:
        print('※※※※※ ユーザID/パスワード不正。:', str(err))
    except ConnectionError as err:
        print('※※※※※ データベースに接続できません。データベースは起動していますか？:', str(err))
    except SQLError as err:
        print('※※※※※ SQLクエリの実行に失敗しました。', str(err))
    except Exception as err:
        print('※※※※※ 想定外のエラーが発生しました。:', str(err))
    return 'Error'


@app.route('/viewlog2')
@check_logged_in    # ログインしている場合のみログの閲覧を可能にするデコレータ
def view_the_log2() -> 'html':
    """ 単語検索＆カウント処理の有用な内容をHTMLテーブルで表示する """
    try:
        with UseDataBase(app.config['dbconfig']) as cursor:
            _SQL = """select ts,  phrase, words, ip, browser_string, results from log2"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ['検索日時', 'フレーズ', '検索単語', 'リモートアドレス', 'ユーザエージェント', '結果']
        return render_template('viewlog.html',
                                the_title='ログの閲覧',
                                the_row_titles=titles,
                                the_data=contents)
    except CredentialsError as err:
        print('※※※※※ ユーザID/パスワード不正。:', str(err))
    except ConnectionError as err:
        print('※※※※※ データベースに接続できません。データベースは起動していますか？:', str(err))
    except SQLError as err:
        print('※※※※※ SQLクエリの実行に失敗しました。', str(err))
    except Exception as err:
        print('※※※※※ 想定外のエラーが発生しました。:', str(err))
    return 'Error'


if __name__ == '__main__':  # このプログラムが直接実行された場合のみ、Webアプリケーションを起動(app.run())する
    app.run(debug=True)   # デフォルトのプロトコルポート番号は「5000」。デバッグモードを有効にする。
