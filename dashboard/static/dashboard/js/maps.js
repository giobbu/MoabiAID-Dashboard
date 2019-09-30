function drawBxlMap(mapId) {
    var mymap = L.map(mapId, {
        zoomSnap: 0.25,
        // crs: L.CRS.EPSG4326
    }).setView([50.83507914731851, 4.36468005885868], 12.25);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
        maxZoom: 18
    }).addTo(mymap);

    return mymap
}

/*
Splits the given street data in several categories according to street type
*/
function splitStreetData(streetData) {
    var streets = {
        major: [],
        medium: [],
        minor: []
    };
    streetData.forEach(street => {
        var strTypre = street.type; // All streets (GeoJSON?) should have a type property
        streets[strTypre].push(street);
    });

    return streets
}

function colorStreet(street, measure) {
    var propVal = street.properties[measure]; //TODO: Determine how to also us3e other properties (maybe a global variable set by user?)
    var highBound;
    var lowBound;

    // Colors are hard-coded to counts property, should be able to also handle velocities and other properties in final

    if (measure == 'count') {
        highBound = 100;
        lowBound = 20;
    } else if (measure == 'velocity') {
        // Velocity might need to also take street type or max speed into account
        highBound = 50;
        lowBound = 30;
    }

    return {
        color:  propVal > highBound ? '#00ff00' : // High values are green 
                propVal >= lowBound ? '#ff531a' : // Medium values are orange
                propVal > 0 ? '#ff0000' : // Low values are red
                '#b3b3b3' // No value or 0 is grey
    }
}

/*
Function to draw coloured streets on a map according to some value (counts, avg. velocity, ...)
Whic streets are drawn depends on the zoom level
*/
function drawStreetColors(map, streetData, measure) {
    var splitData = splitStreetData(streetData);
    var layers = {};

    for (streetType in splitData) {
        layers[streetType] = L.GeoJSON(splitData[streetType], function (feature) { //TODO: We can use real-time leaflet plugin, but this would require a redesign
            return colorStreet(feature, measure)
        })
    }

    layers.major.addTo(map); // Major streets are always shown

    map.on("zoomend", function () {
        var zoomLevel = map.getZoom();
        var medLayer = layers.medium;
        var minLayer = layers.minor;
        if (zoomLevel < 13) {
            if (map.hasLayer(medLayer)) {
                map.removeLayer(medLayer);
            }
            // Also check for min layer in case it was not removed in previous zoom (i.e. when zoomLevel changes from > 15 to < 13)
            if (map.hasLayer(minLayer)) {
                map.removeLayer(minLayer)
            } 
        } else if (zoomLevel < 15) {
            if (map.hasLayer(minLayer)){
                map.removeLayer(minLayer);
            }
            if (!map.hasLayer(medLayer)) {
                map.addLayer(medLayer)
            }
        } else {
            if (!map.hasLayer(medLayer)) {
                map.addLayer(medLayer)
            }
            if (!map.hasLayer(minLayer)) {
                map.addLayer(minLayer)
            }
        }
    })
    
}

