function initLeafletMap() {
    // 1. 地図オブジェクトの作成
    // L.map('map') でHTML要素(#map)に地図を関連付け、
    // setView([緯度, 経度], ズームレベル) で中心とズームを設定します。
    // Leafletは [緯度, 経度] の順序です。
    const map = L.map('map').setView([35.6812, 139.7671], 15); 

    // 2. OpenStreetMapのタイルレイヤーを追加
    // これにより、地図の見た目（道路、建物など）が表示されます。
    // attributionは著作権表示（必須）です。
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // 3. マーカー（ピン）を地図上に追加
    L.marker([35.6812, 139.7671])
        .addTo(map)
        .bindPopup('初期のピン（東京駅周辺）') // ポップアップのテキストを設定
        .openPopup(); // 初期状態でポップアップを開く
}

// ページ読み込み後に地図を初期化
initLeafletMap();