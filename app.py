from flask import Flask, render_template,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel,format_datetime
from database import db
from models import fukuoka_data_lat_lng ,Message
import datetime

app = Flask(__name__)

# データベースの場所を設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False





app.config['BABEL_DEFAULT_LOCALE'] = 'ja'

    
app.config['BABEL_DEFAULT_LOCALE'] = 'ja'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'Asia/Tokyo' 


#format_datetime 関数を 'format_datetime' という名前でJinja2フィルタとして登録
# 【ここに追加！】flask run で起動しても確実にテーブルを作る魔法

db.init_app(app)
with app.app_context():
    db.create_all()
    print("DEBUG: データベースのテーブルを確認・作成しました")
migrate = Migrate(app, db)
babel = Babel(app)

@app.template_filter('format_datetime')
def format_dt_filter(value, format='medium'):
    return format_datetime(value, format)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map():
    # 1. データベースから全店舗を取得
    stores_data = fukuoka_data_lat_lng.query.all()
    
    # 【追加】ターミナルに件数を表示させる
    print(f"DEBUG: データベースから {len(stores_data)} 件取得しました")
    
    # 2. JSが読み取れる「辞書のリスト」に変換
    locations = []
    for s in stores_data:
        locations.append({
            "name": s.name,
            "address": s.address,
            "latitude": s.latitude,   # ← s.lat から s.latitude に修正
            "longitude": s.longitude,  # ← s.lng から s.longitude に修正
            "description": s.description
        })
    
    # 3. templates/index.html にデータを渡して表示
    return render_template('map.html',locations=locations )

@app.route('/search')
def search():
    return redirect('map')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/messages',methods=['GET','POST'])
def messages_api():
    if request.method== 'POST':
        data = request.json
        try:
            new_message = Message(
                sender=data.get('sender'),
                content=data.get('content')
            )
            db.session.add(new_message)
            db.session.commit()
            return jsonify({"status": "ok"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    messages = Message.query.order_by(Message.post_date.asc()).all()
    # 辞書形式のリストに変換して返す
    return jsonify([
        {"sender": m.sender, "content": m.content, "date": m.post_date.isoformat()} 
        for m in messages
    ])

# アプリケーションを起動 (開発用サーバー)
if __name__ == '__main__':
    # 1. データベースのテーブルを自動作成する（これがないとエラーになります）
    with app.app_context():
        db.create_all()
    
    # 2. host='0.0.0.0' を指定して外からの接続を許可する
    app.run(debug=True, host='0.0.0.0', port=5000)