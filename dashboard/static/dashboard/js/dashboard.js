function drawRtTable(tableId, data, columns) {
    return $(tableId).DataTable({
        data: data,
        columns: columns,
        paging: false,
        info: false,
        searching: false,
        retrieve: true,
        order: [
            [1, "desc"]
        ],
        ordering: false
    });
}

function drawRtChart(chartDiv, data, cat_key, val_key, textConfig) {

    // For now we assume only XY charts 
    var chart = am4core.create(chartDiv, am4charts.XYChart);

    chart.numberFormatter.numberFormat = '#.';

    chart.data = data;

    // Create axes
    var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = cat_key;
    categoryAxis.renderer.grid.template.location = 0;
    //categoryAxis.renderer.minGridDistance = 30;

    categoryAxis.renderer.labels.template.events.on("over", function (ev) {
        var point = categoryAxis.categoryToPoint(ev.target.dataItem.category);
        chart.cursor.triggerMove(point, "soft");
    });

    categoryAxis.renderer.labels.template.events.on("out", function (ev) {
        var point = categoryAxis.categoryToPoint(ev.target.dataItem.category);
        chart.cursor.triggerMove(point, "none");
    });

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;

    // Create series
    var series = chart.series.push(new am4charts.ColumnSeries());
    series.dataFields.valueY = val_key;
    series.dataFields.categoryX = cat_key;
    series.tooltipText = "{categoryX}: {valueY}";

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.lineY.disabled = true;
    chart.cursor.lineX.disabled = true;

    // Create title and configure title
    let title = chart.titles.create();
    title.text = textConfig.title;
    title.fontWeight = 'bold';
    title.align = 'center';
    title.paddingBottom = 10;
    title.paddingLeft = 20;

    // Configure category axis
    categoryAxis.title.text = textConfig.catLabel;
    categoryAxis.renderer.minGridDistance = 50;
    categoryAxis.renderer.labels.template.fontSize = 14;
    categoryAxis.renderer.labels.template.horizontalCenter = 'middle';
    categoryAxis.renderer.labels.template.wrap = true;
    categoryAxis.renderer.labels.template.maxWidth = 165;

    // Configure value axis
    valueAxis.title.text = textConfig.valLable;


    return chart;

}

function setupLiveTruckMap(rtMap, rtMeasure, selectPanel, refresh = false) {
    return $.get("/data/", {
            data_usage: "real-time",
            table: "truck",
            data: "positions"
        })
        .done(function (truckData) {

            var markerIcon = new L.Icon({

                iconUrl: 'https://github.com/google/material-design-icons/raw/master/maps/1x_web/ic_local_shipping_black_24dp.png',
                iconSize: [24, 24]

            });

            console.log(truckData);


            if (refresh) {
                selectPanel.removeLayer('Trucks');
            }

            // var trucks = truckData.data.features;
            // Use marker clustering with layer support as in https://github.com/ghybs/Leaflet.MarkerCluster.LayerSupport
            var markers = L.markerClusterGroup(),
                layer_group = L.featureGroup.subGroup(markers),
                truck_layers = L.geoJSON(truckData.data, {
                    onEachFeature: function (feature, layer) {
                        text = `Truck ${feature.properties.truck_id} (At: ${feature.properties.datetime})`;
                        layer.bindPopup(text);
                    },
                    pointToLayer: function (feature, latlng) {
                        return L.marker(latlng, {
                            icon: markerIcon
                        });
                    }
                });

            markers.addTo(rtMap);
            truck_layers.addTo(layer_group);

            // truck_layers.addTo(rtMap);

            selectPanel.addOverlay({
                name: 'Trucks',
                icon: '<i class="material-icons">local_shipping</i>',
                layer: layer_group,
                active: false
            });

            layer_group.addTo(rtMap);

            // Store the data for later reuse
            return {
                layers: truck_layers,
                communes: truckData.data
            };

        })
        .fail(function () {
            alert("Could not retrieve real-time data for trucks");
        });
}

function setupLiveStreetMap(rtMap, rtMeasure, selectPanel, refresh = false) {
    return $.get("/data/", {
            data_usage: "real-time",
            table: "street"
        })
        .done(function (streetData) {
            var streets = streetData.data;

            if (refresh) {
                // Remove old layers from select panel on refresh to avoid deduplication
                selectPanel.removeLayer('Street flow');
                selectPanel.removeLayer('Average Truck Velocity');
            }

            // Add layer for the flow (truck counts) measure to the map
            var [
                flow_layers,
                flow_timeKey
            ] = drawStreetColors(rtMap, streets, 'flow', 'now', refresh);
            console.log(flow_layers);
            selectPanel.addOverlay({
                layer: flow_layers,
                icon: '<i class="material-icons">local_shipping</i>',
                active: true
            }, 'Street flow', 'Streets');

            // Add layer for the velocity measure to the map (disabled by default)
            var [
                vel_layers,
                vel_timeKey
            ] = drawStreetColors(rtMap, streets, 'vel', 'now', refresh);
            vel_layers.remove();

            selectPanel.addOverlay({
                layer: vel_layers,
                icon: '<i class="material-icons">speed</i>',
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

            top10Streets = street_properties.slice(0, 10);

            var dataTable = drawRtTable('#rt-table-street', top10Streets, [{
                    data: 'id_street'
                },
                {
                    data: 'flow'
                }
            ]);

            var rtChart = drawRtChart('rt-figdiv-street', top10Streets, 'id_street', 'flow', {
                title: 'Top 10 most busy streets',
                catLabel: 'Street',
                valLable: 'Number of Trucks'
            });

            //Update data if data table was already initialised (see: https://datatables.net/manual/tech-notes/3)
            if (refresh) {
                // console.log('Map data refreshed');
                dataTable.clear().rows.add(top10Streets).draw();
                rtChart.data = top10Streets;
            }

            // Set up refresh button
            $('#refreshMap').click(function (e) {
                // liveData.layers.remove();
                setupLiveStreetMap(rtMap, rtMeasure, selectPanel, true);
            });

            flow_layers.on({
                add: function (e) {
                    $('#street-table-div').show();
                    $('#rt-figdiv-street').show();
                },
                remove: function (e) {
                    $('#street-table-div').hide();
                    $('#rt-figdiv-street').hide();
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

            if (refresh) {
                selectPanel.removeLayer('Communes');
            }

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

            top5Coms = com_list.slice(0, 5)

            var dataTable = drawRtTable('#rt-table-com', top5Coms, [{
                    data: 'name'
                },
                {
                    data: 'total'
                }
            ]);

            var chart = drawRtChart('rt-figdiv-com', top5Coms, 'name', 'total', {
                title: 'Top 5 most busy communes',
                catLabel: 'Commune',
                valLable: 'Number of trucks'
            });

            //Update data if data table was already initialised (see: https://datatables.net/manual/tech-notes/3)
            if (refresh) {
                // console.log('Map data refreshed');
                dataTable.clear().rows.add(top5Coms).draw();
                chart.data = top5Coms;
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
                    $('#rt-figdiv-com').show();

                },
                remove: function (e) {
                    legend.remove();
                    $('#rt-figdiv-com').hide();
                    $('#com-table-div').hide();

                }
            });

            // Remove layer as it is not shown by default
            chart.events.on('inited', function (e) {
                // Need to wait for chart to be initialized, otherwise it will break the layout
                console.log('Chart ready, removing layer');
                layer.remove();
            });


            selectPanel.addOverlay({
                name: 'Communes',
                icon: '<i class="material-icons">location_city</i>',
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
    }, {
        group: 'Areas of Interest',
        collapsed: true,
        layers: [],
        
    }], {
        title: '<i class="material-icons align-middle">layers</i> Layers',
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
        },
        collapsibleGroups: true
    }); // Layer selection control
    var rtMeasure = "flow"; // Default measure

    console.log(panel);
    

    // Add street and commune layers for RT
    setupLiveStreetMap(rtMap, rtMeasure, panel);
    setupLiveCommuneMap(rtMap, rtMeasure, panel);
    setupLiveTruckMap(rtMap, rtMeasure, panel);
    addAreaLayers(rtMap, panel);

    panel.addTo(rtMap);
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
        console.log(chart);

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
                loadStreetAnalytics('params'); // NOTE: This still has to be implemented 
                break;
            
            case 'Delay':
                loadDelayAnalysis();
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