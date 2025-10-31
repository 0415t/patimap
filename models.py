from app import db # app.pyで初期化したdbをインポート
from datetime import datetime # 投稿日時を扱うためのツールをインポート

class Message(db.Model):
    # ID: 投稿を識別する番号。必ず必要で、自動で増えるようにする
    id = db.Column(db.Integer, primary_key=True)
    
    # 本文 (content): 
    # 投稿内容の文字列。長くなる可能性があるので db.Text を使う。空は許さない
    content = db.Column(db.Text, nullable=False)
    
    # 送信者 (sender): 
    # 送信者の名前。最大50文字程度。空は許さない
    sender = db.Column(db.String(50), nullable=False)
    
    # 投稿日時 (post_date): 
    # 投稿された日時。もし値が指定されなかったら、現在の時刻を自動で入れる
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # オブジェクト表示用
    def __repr__(self):
        return f"Message('{self.sender}', '{self.post_date}')"
    
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable = False)
    # 緯度 (ピンの縦位置)
    latitude = db.Column(db.Float, nullable=False)
    # 経度 (ピンの横位置)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    def __repr__(self):
        return f"<Location {self.id}: {self.name}>"