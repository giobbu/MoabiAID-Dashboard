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

                console.log(figConfigs);

                var nColsRow = 0;
                var nRows = 1;
                for (const config in figConfigs) {
                    if (figConfigs.hasOwnProperty(config)) {
                        const figConf = figConfigs[config];
                        $(`#${timeFrame}-delay-analysis .figures.fig-row-${nRows}`).append(`<div id="figure-${config}" class="col-4"></div>"`);
                        am4core.createFromConfig(figConf, `figure-${config}`);

                        // 3 Figures per row. Insert new row when full
                        if (++nColsRow >= 3) {
                            $(`#${timeFrame}-delay-analysis`).append(`<div class="row figures fig-row-${++nRows}"></div>`);
                        }

                    }
                }

                $('.table-analysis-div table').DataTable();
            });
    }

}