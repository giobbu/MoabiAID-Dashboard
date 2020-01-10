function initMapsTab() {
    console.log("Map tab clicked");

    var histMap = drawBxlMap("hist-map");
    $(this).on('shown.bs.tab', function (e) {
        console.log('Map tab loaded');

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
    am4core.useTheme(am4themes_animated);
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
    var rtMap = drawBxlMap("rt-map");
    var rtMeasure = "flow"; // Default measure
    setupLiveStreetMap(rtMap, rtMeasure);
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