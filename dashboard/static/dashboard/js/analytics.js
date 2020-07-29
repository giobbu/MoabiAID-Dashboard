function loadStreetAnalytics(params) {
    var chart = am4core.create("chartdiv", "PieChart"); //TODO: determine default chart to load
}

function loadDelayAnalysis(timeFrame = 'current') {
    // timeFrame = 'current', 'daily', 'weekly', 'allTime

    if ($(`#${timeFrame}-delay-analysis`).length) {
        // If data was already loaded, simply set this as the active analysis
        $('.analysis-content.active').removeClass('active');
        $(`#${timeFrame}-delay-analysis`).addClass('active');
    } else {
        // Retrieve data
        $.get("/data/delay", {
                timeFrame: timeFrame
            })
            .done(function (delayData) {

                // Retrieve html and hide current active (if any)
                $('.analysis-content.active').removeClass('active');
                $('#analytics-body').append(delayData);

                // TODO: se up charts, tables and maps
                
            });
    }

}