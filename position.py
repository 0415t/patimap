import requests
import json 
import csv
import time

API_KEY ="AIzaSyApqFmKGpDBIPyupwqIbx9BEzuVnTjD-Tc"
# 複数の検索地点をリストで定義
CITIES = [
    {"name": "福岡市", "lat": 33.5904, "lng": 130.4017},
    {"name": "久留米市", "lat": 33.3167, "lng": 130.5500},
    {"name": "北九州市", "lat": 33.8814, "lng": 130.8710},
    {"name": "八女市", "lat": 33.2008, "lng": 130.5694},  # 座標を修正
    {"name": "朝倉市", "lat": 33.4170, "lng": 130.6558},  # 座標を修正
    
    # --- 網羅に必要な追加地点 ---
    {"name": "糸島市", "lat": 33.5786, "lng": 130.2036},
    {"name": "大野城市", "lat": 33.5358, "lng": 130.4907},
    {"name": "直方市", "lat": 33.7380, "lng": 130.7303},
    {"name": "行橋市", "lat": 33.7258, "lng": 130.9859},
    {"name": "大牟田市", "lat": 33.0232, "lng": 130.4439},
    {"name": "飯塚市", "lat": 33.6429, "lng": 130.6865},
]

RADIUS = 25000 # 検索半径を50kmとする
KEYWORD = "パチンコ"
filename ="fukuoka_data.csv"
pachinko_shops = []
result_count = 0
all_shop_data = [] # 全データを一時的に保存するリスト
fieldnames = ['中心地','名前','住所']
is_first_write = True 

# 複数都市のデータを蓄積するため、CSVファイルを追記モード ('a') で開く
with open(filename, 'w', newline='', encoding='utf_8_sig') as csvfile: 
    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() # ヘッダーを最初に書き込む
    
    # CITIESリストをループして、各都市で検索を実行
    for city in CITIES:
        city_name = city["name"]
        LATITUDE = city["lat"]
        LONGITUDE = city["lng"]
        
        print(f"\n▶️ {city_name} の周辺データを検索中...")
        
        next_page_token = None
        page_counter = 0 # ページ数をカウント（最大3まで）
        while True:
        # 1ページ目のURL構築 (locationとradiusを使用)
            if page_counter == 0:
                URL = (
                    f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    f"?location={LATITUDE},{LONGITUDE}"
                    f"&radius={RADIUS}&keyword={KEYWORD}&language=ja&key={API_KEY}"
                )
        # 2ページ目以降のURL構築 (pagetokenのみを使用)
            else:
                # --- APIの仕様により、次のページリクエスト前に必ず2秒間待機 ---
                print("   (次のページへ移動するため、2秒間待機します...)")
                time.sleep(2) 
                
                URL = (
                    f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    f"?pagetoken={next_page_token}&language=ja&key={API_KEY}"
                )

            # APIにリクエストを送信
            response = requests.get(URL)
            data = response.json()

            if data.get("status") == "OK":
                page_counter += 1
                print(f"   -> ページ {page_counter} から {len(data['results'])} 件取得")

                for result in data["results"]:
                    shop_data = {
                        "中心地": city_name,
                        "名前": result.get("name"),
                        "住所": result.get("vicinity") 
                    }
                    
                    all_shop_data.append(shop_data)
                    result_count += 1
                
                # next_page_tokenの確認と更新
                next_page_token = data.get("next_page_token")

                # 3ページ取得済み、または next_page_token がなければループを終了
                if not next_page_token or page_counter >= 3:
                    break

            elif data.get("status") == "ZERO_RESULTS":
                if page_counter == 0:
                    print(f"  - 該当する結果が見つかりませんでした。")
                break # 結果がなければループ終了

            else:
                print(f"  - エラーが発生しました: {data.get('status')} (ページ {page_counter + 1})")
                # --- API制限エラーの場合、さらに長く待つなどの処理を追加することも可能 ---
                break
unique_shops = {} 
for shop in all_shop_data:
    # '名前'と'住所'を結合した文字列をユニークなキーとして使用
    key = (shop['名前'], shop['住所'])
    
    if key not in unique_shops:
        # 重複がなければ、辞書に追加
        unique_shops[key] = shop
    else:
        # 重複がある場合、中心地の情報を追加・更新（どの検索でヒットしたか分かるように）
        # 例: "福岡市, 久留米市" のように連結する処理を後で追加可能
        pass # 今回はシンプルに最初のヒット情報を採用

final_unique_list = list(unique_shops.values())
unique_count = len(final_unique_list)

with open(filename, 'w', newline='', encoding='utf_8_sig') as csvfile: 
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() 
    writer.writerows(final_unique_list) # ユニークなリストを一括で書き込む


print(f"\n✅ 収集が完了しました。")
print(f"   全リクエストで取得したデータ総数: {result_count} 件")
print(f"   データは '{filename}' に保存されました。")
print(f"   重複排除後の**ユニークな店舗数**: {unique_count} 件")