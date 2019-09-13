function drawBxlMap(mapId) {
    var mymap = L.map(mapId, {
        zoomSnap: 0.25,
        // crs: L.CRS.EPSG4326
    }).setView([50.83507914731851, 4.36468005885868], 12.25);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
        maxZoom: 18
    }).addTo(mymap);
}

