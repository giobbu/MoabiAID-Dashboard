/************************
 * General map functions *
 ************************/

/*
Creates a map with an openstreetmap background layer and returns it
*/
function drawBxlMap(mapId) {
    var mymap = L.map(mapId, {
        zoomSnap: 0.25,
        // crs: L.CRS.EPSG4326
    }).setView([50.83507914731851, 4.36468005885868], 12.25);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
        maxZoom: 18,
        minZoom: 10
    }).addTo(mymap);

    return mymap;
}

function resetHighlight(e, geojson) {
    geojson.resetStyle(e.target);
}

function addLegend(position, grades, colorFn) {
    var legend = L.control({
        position: position
    });

    legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend');

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML +=
                '<i style="background:' + colorFn(grades[i]) + '"></i> ' +
                grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
        }

        return div;
    };

    return legend;
}



/***************************
 * Street related functions *
 ***************************/

/*
Splits the given street data in several categories according to street type
*/
function splitStreetData(streetData) {
    var streets = {
        major: [],
        medium: [],
        minor: []
    };
    console.log(streetData);

    streetData.features.forEach(street => {
        var strTypre = street.type; // All streets (GeoJSON?) should have a type property
        streets[strTypre].push(street);
    });

    return streets;
}

function colorStreet(street, measure, timeKey) {
    var propVal = street.properties.list_table[measure][timeKey]; //TODO: Determine how to also us3e other properties (maybe a global variable set by user?)
    var highBound;
    var lowBound;

    // Colors are hard-coded to counts property, should be able to also handle velocities and other properties in final

    if (measure == 'flow') {
        highBound = 10;
        lowBound = 5;
    } else if (measure == 'vel') {
        // Velocity might need to also take street type or max speed into account
        highBound = 50;
        lowBound = 30;
    }

    streetCol = '#0ac20a';

    if (propVal >= highBound) {
        streetCol = '#ff0000';

    } else if (propVal >= lowBound) {
        streetCol = '#f2800d';

    }

    return {
        color: streetCol, // No value or 0 is grey
    };
}

/*
Function to draw coloured streets on a map according to some value (counts, avg. velocity, ...)
Which streets are drawn depends on the zoom level
Note: The timeFrame parameter is used to decide whether we should use the latest available time window or the one for a given time
*/
function drawStreetColors(map, streetData, measure, timeFrame, refresh=false) {
    console.log(streetData);

    var times = streetData.features[0].properties.list_table.time; //Keys where value can be found are the same for each street, so only one is needed
    console.log(times);
    
    var timeIndex = getTimeIndex(times, timeFrame);

    var layers = L.geoJSON(streetData, {
        style: function (feat) {
            return colorStreet(feat, measure, timeIndex);
        },
    }).addTo(map);

    $('#measure-select-drop .dropdown-item').click(function () {
        var newMeasure = $(this).data('measure');

        console.log(newMeasure);

        layers.setStyle(function (feat) {
            return colorStreet(feat, newMeasure, timeIndex);
        });

    });

    console.log(layers);

    // var splitData = splitStreetData(streetData);
    // var layers = {};

    // for (var streetType in splitData) {
    //     layers[streetType] = L.GeoJSON(splitData[streetType], function (feature) { //TODO: We can use real-time leaflet plugin, but this would require a redesign
    //         return colorStreet(feature, measure);
    //     });
    // }

    // layers.major.addTo(map); // Major streets are always shown

    // map.on("zoomend", function () {
    //     var zoomLevel = map.getZoom();
    //     var medLayer = layers.medium;
    //     var minLayer = layers.minor;
    //     if (zoomLevel < 13) {
    //         if (map.hasLayer(medLayer)) {
    //             map.removeLayer(medLayer);
    //         }
    //         // Also check for min layer in case it was not removed in previous zoom (i.e. when zoomLevel changes from > 15 to < 13)
    //         if (map.hasLayer(minLayer)) {
    //             map.removeLayer(minLayer);
    //         }
    //     } else if (zoomLevel < 15) {
    //         if (map.hasLayer(minLayer)) {
    //             map.removeLayer(minLayer);
    //         }
    //         if (!map.hasLayer(medLayer)) {
    //             map.addLayer(medLayer);
    //         }
    //     } else {
    //         if (!map.hasLayer(medLayer)) {
    //             map.addLayer(medLayer);
    //         }
    //         if (!map.hasLayer(minLayer)) {
    //             map.addLayer(minLayer);
    //         }
    //     }
    // });
    return {layers: layers, timeKey: timeIndex};
}

function setupLiveStreetMap(rtMap, rtMeasure, refresh=false) {
    $.get("/data/", {
        data_usage: "real-time",
        table: "state_street" // IF this is relevant
    })
    .done(function (streetData) {
        var streets = streetData.data;
        var {layers, timeKey} = drawStreetColors(rtMap, streets, rtMeasure, 'now', refresh);

        //Extract top 10 streets and draw table
        top_streets = [];
        street_properties = streets.features.map(function (s) {
            var sID = s.properties.id_street;
            var propList = s.properties.list_table;
            return {
                id_street: sID,
                flow: propList.flow[timeKey],
                //Etc if we want to use other properties
            };
        });
        street_properties.sort(function (a, b) {
            return a.flow - b.flow;
        });
        street_properties.reverse();
        console.log(street_properties);
        
        var dataTable = $('#rt-table').DataTable( {
            data: street_properties.slice(0,10),
            columns : [
                { data: 'id_street'},
                { data: 'flow'}
            ],
            paging: false,
            info: false,
            searching: false,
            retrieve: true,
            order: [[1, "desc"]]
        });

        //Update data if data table was already initialised (see: https://datatables.net/manual/tech-notes/3)
        if (refresh) {
            dataTable.clear().rows.add(street_properties.slice(0,10)).draw();
        }

        // Store the data for later reuse
        return {layers: layers, streets:streets};

    })
    .fail(function () {
        alert("Could not retrieve real-time data");
    });

}

/***************************
 * Commune related functions *
 ***************************/

function communeColor(val) {
    // console.log(val);
    var color = '#fef0d9'; //Default color

    var thresholdColors = [
        [10000, '#b30000'],
        [2000, '#e34a33'],
        [1000, '#fc8d59'],
        [500, '#fdbb84'],
        [100, '#fdd49e']
    ];

    thresholdColors.some(tr => {
        // console.log(tr);

        var trVal = tr[0];
        var trCol = tr[1];

        if (val >= trVal) {
            color = trCol;
            return true;
        }
    });

    return color;
}

function communeStyle(commune, truck_counts) {
    return {
        fillColor: communeColor(truck_counts[commune.properties.name].total),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.6
    };
}

function communeHighlight(event) {
    var layer = event.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.8
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}

