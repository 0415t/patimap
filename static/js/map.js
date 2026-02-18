function initLeafletMap() {
    // 1. 地図オブジェクトの作成
    // L.map('map') でHTML要素(#map)に地図を関連付け、
    // setView([緯度, 経度], ズームレベル) で中心とズームを設定します。
    // Leafletは [緯度, 経度] の順序です。
    const map = L.map('map').setView([33.6960213, 130.4408748], 15); 

    // 2. OpenStreetMapのタイルレイヤーを追加
    // これにより、地図の見た目（道路、建物など）が表示されます。
    // attributionは著作権表示（必須）です。
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // 3. マーカー（ピン）を地図上に追加
    L.marker([33.6960213,130.4408748 ])
        .addTo(map)
        .bindPopup('福岡工業大学') // ポップアップのテキストを設定
        .openPopup(); // 初期状態でポップアップを開く

    // 4.マーカーの追加
    //L.marker([33.68, 130.42]) // 👈 iconオプションで指定
        //.addTo(map)
        //.bindPopup('カスタム画像の場所');

    // 4. DBから取得した店のピンを全部立てる
    // locationsが空でないか、正しく読み込めているかチェック
    if (typeof locations !== 'undefined' && locations !== null) {
        locations.forEach(loc => {
            // 値が入っているか確認してからピンを立てる
            if (loc.lat && loc.lng) {
                L.marker([loc.lat, loc.lng])
                    .addTo(map)
                    .bindPopup(`<b>${loc.name}</b><br>${loc.address}`);
            }
        });
        console.log(`${locations.length}件のピンを表示しました`);
    } else {
        console.error("locationsが見つかりません。HTML側で正しく定義されていますか？");
    }
}

// ページ読み込み後に地図を初期化
initLeafletMap();