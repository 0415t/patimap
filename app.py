from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel,format_datetime
import datetime,json

app = Flask(__name__)

# データベースの場所を設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemyをアプリとつなげる
db = SQLAlchemy(app)

# Flask-Migrateを初期化（dbとappを関連付ける）
migrate = Migrate(app, db) 

# models.pyが同じ階層であることが前提
from models import Message,fukuoka_data_lat_lng

app.config['BABEL_DEFAULT_LOCALE'] = 'ja'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'Asia/Tokyo' 

babel = Babel(app)

#format_datetime 関数を 'format_datetime' という名前でJinja2フィルタとして登録
@app.template_filter('format_datetime')
def format_dt_filter(value, format='medium'):
    return format_datetime(value, format)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map():
    # 1. データベースから全件取得
    locations = fukuoka_data_lat_lng.query.all()

    # 2. JSONに変換（JavaScriptが読めるテキスト形式にする）
    # リストの中に辞書を入れる形にします
    data_for_js = []
    for loc in locations:
        data_for_js.append({
            "name": loc.name,
            "address": loc.address,
            "lat": loc.latitude,  # JSで使いやすい名前に
            "lng": loc.longitude,
            "desc": loc.description
        })
    print(f"DEBUG: 取得した件数 = {len(locations)}") # ターミナルに件数が出るか確認
    # DBから取ってJSONにする
    locations_json = json.dumps(data_for_js)
    return render_template('map.html', locations_json=locations_json)

@app.route('/search')
def search():
    return redirect('map')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    
    # 1. データベースからすべてのメッセージを取得する
    #   - .all() で全ての行を取得
    #   - .order_by(Message.post_date.asc()) で投稿日時が古い順に並び替える
    messages = Message.query.order_by(Message.post_date.asc()).all()
    if request.method == 'POST':
        #データの受信
        sender = request.form.get('sender')#name属性が対応している
        content = request.form.get('content')
        # 3. データベースへの格納
        try:
            new_message = Message(
                sender=sender, 
                content=content,
                )
            
            db.session.add(new_message)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            print(f"データベースエラー: {e}")
            return "データベースへの保存中にエラーが発生しました。", 500
        return redirect(url_for('chat'))
    return render_template('chat.html', messages=messages)

# アプリケーションを起動 (開発用サーバー)
if __name__ == '__main__':
    # デバッグモードをオンにして実行 (開発時)
    app.run(debug=True)