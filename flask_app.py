import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/sakumaisao/mysite/uploads/'
ALLOWED_EXTENSIONS = {'csv','txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




#バリデーション
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




#トップページ
@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

        # アップロード形式が「file」で有ることのチェック
        if 'file' not in request.files:

            return 'No file part'

            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # アップロード名が「空でないこと」のチェック
        if file.filename == '':

            return 'No selected file'

            flash('No selected file')
            return redirect(request.url)

        # バリデーションチェックが終了したら
        if file and allowed_file(file.filename):


            # アップロード処理
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #【未実装】csvだった場合
            #【未実装】csvをチェックする

            #【未実装】チェック結果をて配列に保存する
            check_result = {
                "count_data" : 102,
                "count_null" : 3,
                "count_error" : 1,
                }

            #【未実装】チェック結果を表示させるページへリダイレクトする
            return redirect('/')


    return '''
    <!doctype html>
    <title>CSV破損チェッカー（Flaskアプリケーション）</title>
    <h1>CSV破損チェッカー</h1>
    <p>チェックしたいcsvをアップロードしてください。</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



#結果ページ
@app.route('/result_check', methods=['GET'])
def result_check():
    return render_template('index.html')

