$(document).ready(function () {
    var mymap = L.map('mapid', {
        zoomSnap: 0.25
    }).setView([50.8354, 4.4083], 11.5);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoiYXJkaWxsZW4iLCJhIjoiY2p4NXd1YXdkMDBiMzN5cWpnazF0bTcwYSJ9.PnYEXt4qwH8DUEbhiy8zQw'
    }).addTo(mymap);
});