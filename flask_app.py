import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename



"""
初期設定
"""
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app






"""
【設定】ファイルアップロード機能
"""
UPLOAD_FOLDER = '/home/sakumaisao/mysite/uploads/'
ALLOWED_EXTENSIONS = {'csv'} #{'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER








"""
バリデーション
"""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS







"""
【ルーティング】トップページ
"""
@app.route('/', methods=['GET'])
def upload_file():

    return render_template('index.html')








"""
【ルーティング】結果ページ
"""
@app.route('/result_check', methods=['GET','POST'])
def result_check():

    if request.method == 'POST':

        # アップロード形式が「file」で有ることのチェック
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # アップロード名が「空でないこと」のチェック
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # バリデーションチェックが終了したら
        if file and allowed_file(file.filename):

            # アップロード処理
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #【未実装】csvをチェックする
            #【未実装】チェック結果をて配列に保存する
            result_dict = {
                "count_data" : 102,
                "count_null" : 3,
                "count_error" : 1,
                }

            #【未実装】チェック結果を表示させるページへリダイレクトする
            return render_template('result.html', result_dict=result_dict)

        else:
            flash('バリデーションエラーです')
            return redirect('/')

    else:

        return redirect('/')







"""
【ルーティング】helloページ
"""
@app.route('/hello')
def hello():
    return 'Hello, World!'

