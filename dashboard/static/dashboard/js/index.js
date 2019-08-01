$(document).ready(function () {
    var mymap = L.map('mapid', {
        zoomSnap: 0.25,
        // crs: L.CRS.EPSG4326
    }).setView([50.83507914731851, 4.36468005885868], 12.25);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
        maxZoom: 18
    }).addTo(mymap);

    var communeStyle = {
        "color": "#ff7800",
        "weight": 5,
        "opacity": 0.65
    };

    $.getJSON("/data/", {
            table: 'Commune',
            data: 'borders'
        },
        function (borders) {
            $.getJSON("/data/", {
                    table: 'Truck',
                    data: 'in_commune'
                },
                function (response) {
                    res_data = response.data
                    var ticDiv = $("#trucks-in-commune")
                    ticDiv.find("#total-trucks").text(`There are currently ${res_data.total_trucks} trucks in Brussels.`)
                    ticDiv.find("#truck-classes").text(`${res_data.cat_b} of them are class B (< 3.5 T) ${res_data.cat_c} of them are class C (> 3.5T)`)
                    ticDiv.find("table").DataTable(res_data.table)

                    var commune_trucks = {};
                    res_data.table.data.forEach(com => {
                        var com_name = com.commune;
                        delete com.commune;
                        commune_trucks[com_name] = com;    
                    }); 

                    var commune_layer = L.geoJSON(borders, {
                        style: communeStyle,
                        onEachFeature: function (feat, layer) {
                            com_name = feat.properties.name;
                            com_trucks = commune_trucks[com_name];
                            layer.bindTooltip(`There are ${com_trucks.total} trucks in ${com_name}`);
                          }
                    }).addTo(mymap);

                    console.log(commune_layer);
                    
                }
            );
        }
    );

    window.map = mymap;
});