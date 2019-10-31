$(document).ready(function () {

    //TODO: add interaction (hover?) for sidebar


    // Real time tab
    var rtMap = drawBxlMap("rt-map");
    var rtMeasure = "flow"; // Default measure

    $.get("/data/", {
            data_usage: "real-time",
            table: "state_street" // IF this is relevant
        })
        .done(function (streetData) {
            var streets = streetData.data;
            var {layers, timeKey} = drawStreetColors(rtMap, streets, rtMeasure, 'now');

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

            $('#rt-table').DataTable( {
                data: street_properties.slice(0,10),
                columns : [
                    { data: 'id_street'},
                    { data: 'flow'}
                ],
                paging: false,
                info: false,
                searching: false
            });


        })
        .fail(function () {
            alert("Could not retrieve real-time data");
        });

    //Maps tab
    $('#v-pills-maps-tab').one("click", function () {
        console.log("Map tab clicked");

        var histMap = drawBxlMap("hist-map");

        //TODO add layers and hook up map controls
    });

    // Charts tab
    $("#v-pills-charts-tab").one("click", function () { // TODO: this should probably best be triggerd when the charts tab is selected for the first time
        am4core.useTheme(am4themes_animated);
        am4core.useTheme(am4themes_material);
        $(".chart-row").each(function (index) {
            // First chart is shown by default
            if (index != 0) {
                $(this).hide();
            }

            chart_name = $(this).prop("id"); //id of a chart div should correspond to the chart name as accepted by server side handlers

            $(`<h3> ${chart_name} </h3>`).appendTo(this);
            chart = drawChart(chart_name);
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
    });
});