$(document).ready(function () {

    var mymap = drawBxlMap("mapid");

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
                    ticDiv.find("#total-trucks").html(`There are currently <strong>${res_data.total_trucks}</strong> trucks in Brussels.`)
                    ticDiv.find("#truck-classes")
                    .html(`<strong>${res_data.cat_b}</strong> of them are class <strong>B</strong> (< 3.5 T) and <strong>${res_data.cat_c}</strong> of them are class <strong>C</strong> (> 3.5T)`)
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