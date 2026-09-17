# patimap 🎰

パチンコが好きな友人のために、周辺店舗や関連情報をスムーズに検索・視覚化できるように開発したWebアプリケーションです。

---

## 📸 画面イメージ

| 店舗マップ表示 | チャット機能 |
| :---: | :---: |
| *(ここにドラッグ＆ドロップで画像を配置)* | *(ここにドラッグ＆ドロップで画像を配置)* |

---

## 💡 開発背景

Flaskの基礎講座を修了した後、「学んだ知識を使って、実際にゼロから1つのWebアプリケーションを完成させてみたい」という強い思いから開発をスタートした、自身初のオリジナル作品です。

開発のヒントになったのは、パチンコが好きな友人との「この店舗では負けているけれど、地元の店舗だと勝てている気がする」という何気ない会話でした。

「店舗ごとの情報や収支データを地図（マップ）上で視覚的に把握できれば面白いのではないか」と考え、店舗の視覚化と情報共有を掛け合わせた本アプリの企画・開発に至りました。

---

## ✨ 主な機能

### 🟢 実装済み機能
- **店舗マップ表示 (`/map`)**: DBに登録された福岡の店舗データを地図上にピンで可視化
- **Google Places API連携検索 (`/search_api`)**: キーワード検索により、天神周辺などの店舗情報をリアルタイム取得・マップ表示
- **リアルタイムチャット機能 (`/chat`)**: ユーザー間で情報交換ができるメッセージ投稿・表示機能

### 🟡 現在開発中・実装予定機能（Roadmap）
- **店舗ごとの収支記録・管理**: 各店舗での勝敗や金額をマップ上で可視化する機能
- **ユーザー認証機能**: ユーザーごとに個別の収支や保存店舗を管理する機能
- **セキュリティ・コードリファクタリング**: APIキーの環境変数化（.env）および依存関係の整理

---

## 🛠 使用技術 (Tech Stack)

### Backend
- **Python 3.x**
- **Flask 3.1.2**
- **Flask-SQLAlchemy** (ORM) / **Flask-Migrate** (DBマイグレーション)
- **SQLite** (データベース)
- **Flask-Babel** (多言語対応) / **pytz** (タイムゾーン管理)

### Frontend
- **HTML5 / CSS3 / JavaScript**
- **Jinja2** (テンプレートエンジン)
- **Google Maps API & Google Places API (v1)**

### Tools & Environment
- **Git / GitHub**
- **VS Code**

---

## 🚀 起動手順 (Local Setup)

```bash
# 1. リポジトリのクローン
git clone [https://github.com/0415t/patimap.git](https://github.com/0415t/patimap.git)
cd patimap

# 2. 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windows(cmd)の場合は venv\Scripts\activate

# 3. 依存パッケージのインストール
pip install -r requirements.txt

# 4. アプリケーションの実行
python app.py
