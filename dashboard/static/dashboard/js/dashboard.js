$(document).ready(function () {
    drawBxlMap("rt-map");

    $("#v-pills-charts-tab").one("click", function () { //TODO: this should probably best be triggerd when the charts tab is selected for the first time
        am4core.useTheme(am4themes_animated);
        am4core.useTheme(am4themes_material);
        $(".chart-row").each(function (index) {
            // First chart is shown by default
            if (index != 0) {
                $(this).hide()
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
            $(".chart-row").each( function () {
                if ($(this).attr("id") == showChart) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            })
        });
    });
});


