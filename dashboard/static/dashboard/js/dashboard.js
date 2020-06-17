function setupLiveStreetMap(rtMap, rtMeasure, selectPanel, refresh = false) {
    return $.get("/data/", {
            data_usage: "real-time",
            table: "state_street" // IF this is relevant
        })
        .done(function (streetData) {
            var streets = streetData.data;
            var [
                flow_layers,
                flow_timeKey
            ] = drawStreetColors(rtMap, streets, 'flow', 'now', refresh);
            console.log(flow_layers);

            selectPanel.addOverlay({
                layer: flow_layers,
                active: true
            }, 'Street flow', 'Streets');
            var [
                vel_layers,
                vel_timeKey
            ] = drawStreetColors(rtMap, streets, 'vel', 'now', refresh);
            vel_layers.remove(); 

            selectPanel.addOverlay({
                layer: vel_layers,
                active: false
            }, 'Average Truck Velocity', 'Streets');
            


            //Extract top 10 streets and draw table
            top_streets = [];
            street_properties = streets.features.map(function (s) {
                var sID = s.properties.id_street;
                var propList = s.properties.list_table;
                return {
                    id_street: sID,
                    flow: propList.flow[flow_timeKey],
                    //Etc if we want to use other properties
                };
            });
            street_properties.sort(function (a, b) {
                return a.flow - b.flow;
            });
            street_properties.reverse();
            // console.log(street_properties);

            var dataTable = $('#rt-table-street').DataTable({
                data: street_properties.slice(0, 10),
                columns: [{
                        data: 'id_street'
                    },
                    {
                        data: 'flow'
                    }
                ],
                paging: false,
                info: false,
                searching: false,
                retrieve: true,
                order: [
                    [1, "desc"]
                ]
            });

            //Update data if data table was already initialised (see: https://datatables.net/manual/tech-notes/3)
            if (refresh) {
                // console.log('Map data refreshed');
                dataTable.clear().rows.add(street_properties.slice(0, 10)).draw();
            }

            // Set up refresh button
            $('#refreshMap').click(function (e) {
                // liveData.layers.remove();
                setupLiveStreetMap(rtMap, rtMeasure, selectPanel, true);
            });

            flow_layers.on({
                add: function (e) {
                    $('#street-table-div').show();
                },
                remove: function (e) {
                    $('#street-table-div').hide();
                }
            });

            // Store the data for later reuse
            return {
                layers: [vel_layers, flow_layers],
                streets: streets
            };

        })
        .fail(function () {
            alert("Could not retrieve real-time data for streets");
        });

}

function setupLiveCommuneMap(rtMap, rtMeasure, selectPanel, refresh = false) {
    return $.get("/data/", {
            data_usage: "real-time",
            table: "state_commune" // IF this is relevant
        })
        .done(function (communeData) {

            var communes = communeData.data.features;
            var truck_counts = {};
            var com_list = [];

            communes.forEach(com => {
                var com_name = com.properties.name;
                // delete com.properties.name;
                truck_counts[com_name] = com.properties;
                com_list.push(com.properties);
            });
            var [layer, legend] = drawCommuneMap(communes, rtMap, truck_counts);

            // console.log(truck_counts);

            com_list.sort(function (a, b) {
                return a.total - b.total;
            });
            com_list.reverse();

            var dataTable = $('#rt-table-com').DataTable({
                data: com_list.slice(0, 5),
                columns: [{
                        data: 'name'
                    },
                    {
                        data: 'total'
                    }
                ],
                paging: false,
                info: false,
                searching: false,
                retrieve: true,
                order: [
                    [1, "desc"]
                ]
            });

            //Update data if data table was already initialised (see: https://datatables.net/manual/tech-notes/3)
            if (refresh) {
                // console.log('Map data refreshed');
                dataTable.clear().rows.add(com_list.slice(0, 5)).draw();
            }

            // Set up refresh button
            $('#refreshMap').click(function (e) {
                // liveData.layers.remove();
                setupLiveCommuneMap(rtMap, rtMeasure, selectPanel, true);
            });

            layer.on({
                add: function (e) {
                    legend.addTo(rtMap);
                    $('#com-table-div').show();

                },
                remove: function (e) {
                    legend.remove();
                    $('#com-table-div').hide();
                }
            });
            layer.remove();

            selectPanel.addOverlay({
                name: 'Communes',
                layer: layer,
                active: false
            });



            // Store the data for later reuse
            return {
                layers: layer,
                communes: communes
            };

        })
        .fail(function () {
            alert("Could not retrieve real-time data for communes");
        });
}

function initRtTab() {

    // TODO: cleanup (add layers after panel add?), only allow 1 layer at atime? 

    // Set up map
    var rtMap = drawBxlMap("rt-map");

    // Set up map controls
    var panel = L.control.panelLayers(null, [{
        group: 'Streets',
        layers: []
    }], {
        title: 'Active Layers',
        position: 'topleft',
        compact: true,
        sortLayers: true,
        sortFunction: function (layerA, layerB, nameA, nameB) {
            console.log(nameA);

            // Define ordering of layers in the panel
            if (nameA == 'Streets') {
                return -1;
            }
            if (nameB == 'Streets') {
                return 1;
            }
        }
    }).addTo(rtMap); // Layer selection control
    var rtMeasure = "flow"; // Default measure

    // Add street and commune layers for RT
    setupLiveStreetMap(rtMap, rtMeasure, panel);
    setupLiveCommuneMap(rtMap, rtMeasure, panel);
}

function initMapsTab() {
    // console.log("Map tab clicked");

    var histMap = drawBxlMap("hist-map");
    $(this).on('shown.bs.tab', function (e) {
        // console.log('Map tab loaded');

        histMap.invalidateSize();
    });

    getTypicalData();

    $('#v-pills-maps .sliderwidget').on('input', function (e) {
        var valueDisplay = $(this).data('valuedisplay');
        $(valueDisplay).text(e.target.value);
        // console.log('New slider value:');        
        // console.log(e.target.value);

    });


    //TODO add layers and hook up map controls
}

function initChartsTab() {
    // am4core.useTheme(am4themes_animated);
    am4core.useTheme(am4themes_material);
    $(".chart-row").each(function (index) {
        // First chart is shown by default
        if (index != 0) {
            $(this).hide();
        }

        var chart_name = $(this).prop("id"); //id of a chart div should correspond to the chart name as accepted by server side handlers

        $(`<h3> ${chart_name} </h3>`).appendTo(this);
        var chart = drawChart(chart_name);
    });

    // Bind event handlers to dropdown

    $("#chart-select-drop .dropdown-item").click(function () {
        var showChart = $(this).data("chart");

        // Make sure all other chart divs are hidden and show the selected one
        // NOTE: It might be better to store the currently shown chart somewhere and only toggle the currently shown and newly selected ones
        $(".chart-row").each(function () {
            if ($(this).attr("id") == showChart) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
}

function initAnalyticsTab() {
    $('#entity-select-dropdown .dropdown-item').click(function (e) {
        e.preventDefault();
        var selected = $(this).text();

        switch (selected) {
            case 'Streets':
                //TODO: load individual street analytics
                break;

            default:
                break;
        }
    });
}



$(document).ready(function () {

    // Real time tab
    initRtTab();

    // var retrievedData = {
    //     now: {
    //         streets: liveData.streets
    //     }
    // }; // Variable that stores data retrieved by ajax to avoid making unnecessary new calls

    // $('#refreshMap').click(function (e) {
    //     liveData.layers.remove();  
    //     liveData = setupLiveStreetMap(rtMap, rtMeasure, true);
    //     retrievedData.now.streets = liveData.streets;
    // });

    //Maps tab
    $('#v-pills-maps-tab').one("click", function () {
        initMapsTab();
    });

    // Charts tab
    $("#v-pills-charts-tab").one("click", function () {
        initChartsTab();
    });

    // Analytics tab
    $('#v-pills-analytics-tab').one('click', function (e) {
        initAnalyticsTab();
    });

});