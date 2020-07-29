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
        $.get("/analysis/delay", {
                timeFrame: timeFrame
            })
            .done(function (delayData) {

                // Retrieve html and hide current active (if any)
                $('.analysis-content.active').removeClass('active');
                $('#analytics-body').append(delayData);

                // TODO: set up charts, tables and maps
                drawBxlMap('delay-map');

                const figConfigs = JSON.parse(document.getElementById('figure_configs').textContent);

                for (const config in figConfigs) {
                    if (figConfigs.hasOwnProperty(config)) {
                        const figConf = figConfigs[config];
                        $(`#${timeFrame}-delay-analysis`).append(`<div id="figure-${config}" class="col"></div>"`);
                        am4core.createFromConfig(figConf, `figure-${config}`);

                    }
                }
            });
    }

}