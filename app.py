from flask import Flask, render_template,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel,format_datetime
import datetime

app = Flask(__name__)

# データベースの場所を設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemyをアプリとつなげる
db = SQLAlchemy(app)

# Flask-Migrateを初期化（dbとappを関連付ける）
migrate = Migrate(app, db) 


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- ここに直接書く (models.py から持ってくる) ---
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=False)
    post_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, sender, content):
        self.sender = sender
        self.content = content

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
    return render_template('map.html')

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
    # デバッグモードをオンにして実行 (開発時)
    app.run(debug=True)