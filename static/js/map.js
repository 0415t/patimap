function initLeafletMap() {
    // 1. 地図の作成（ここは変更なし）
    const map = L.map('map').setView([33.6960213, 130.4408748], 15); 

    // 2. タイルレイヤーの追加
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // 3. 福岡工業大学のピン
    L.marker([33.6960213, 130.4408748])
        .addTo(map)
        .bindPopup('福岡工業大学');

    // 4. マーカーの追加（修正済み：カッコを閉じました）
    // もしカスタムアイコンを使わないなら、普通のピンとして表示させます
    L.marker([33.68, 130.42])
        .addTo(map)
        .bindPopup('テスト地点');

    // 5. DBから取得した店のピンを全部立てる
    if (typeof locations !== 'undefined' && locations !== null) {
        locations.forEach(loc => {
            // Python側から届くデータが数値(Float/REAL)であることを利用します
            if (loc.latitude && loc.longitude) {
                L.marker([loc.latitude, loc.longitude])
                    .addTo(map)
                    .bindPopup(`<b>${loc.name}</b><br>${loc.address}`);
            }
        });
        console.log(`${locations.length}件のデータを地図に反映しました`);
    } else {
        console.error("locationsが見つかりません。HTML側を確認してください。");
    }
}

initLeafletMap();