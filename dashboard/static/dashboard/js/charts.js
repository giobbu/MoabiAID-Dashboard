/*
This script populates a page with the appropriate figures 
*/


/*
 * Functions related to Drawing AmCharts
 */
function addDetails(chart) {
    var details = chart.chartAndLegendContainer.createChild(am4core.Image);
    chart.chartAndLegendContainer.reverseOrder = true;
    details.align = "right";
    details.valign = "top";
    details.width = 50;
    details.height = 50;
    details.verticalCenter = "top";
    details.horizontalCenter = "left";
    details.href = detailIcon; //Referenced from template
    details.tooltipText = "Test"; // TODO: retrieve the description somewhere
}

function formatLabels(chart) {

    chart.fontSize = 13;
    chart.fontWeight = "bolder";
    chart.numberFormatter.numberFormat = "#";

    chartType = chart.className;

    if (chartType == "XYChart") {
        // console.log(chart)
        chart.yAxes.each(function (axis) {

            // Wrap labels that are too long
            labelTemplate = axis.renderer.labels.template;
            labelTemplate.wrap = true;
            labelTemplate.maxWidth = 300;

            // Add ticks
            ticksTemplate = axis.renderer.ticks.template;
            ticksTemplate.disabled = false;
            ticksTemplate.strokeOpacity = 1;
            ticksTemplate.length = 10;
        })

        chart.series.each(function (ser) {
            // columnTemplate = ser.columns.template.width = am4core.percent(20);
        })
    }

}

function drawChart(chart_name) {

    var divSelector = insertDrawDiv(chart_name);

    var chart = null;
    requestData(chart_name, 'chart')
        .done(function (chart_data) {

            $(divSelector).empty();
            // console.log(divSelector);
            // console.log(chart_data);
            // Generate chart
            var divID = chart_name + "_figure_div"; // Same as in insertDrawDiv
            chart = am4core.createFromConfig(chart_data.data, divID);

            // // Add an icon to the legend with some information about the chart on hover and details on tooltips
            // addDetails(chart);

            // // Format labels
            formatLabels(chart);
            // console.log(chart);
            
        });
    // TODO: add fail and always callbacks as necessary
    return chart
}

/*
 * Functions related to Drawing DataTables
 */
function insertHeaders(columns, tableSelector) {

    //TODO order columns

    $("<thead><tr></tr></thead> <tfoot><tr></tr></tfoot>").appendTo(tableSelector);

    columns.forEach(col => {
        var colWords = col.data.split("_");
        colWords.forEach((word, index, arr) => {
            arr[index] = jsUcfirst(word);
        });
        var colName = "<th>" + colWords.join(" ") + "</th>";
        $(`${tableSelector} tr`).append(colName);

    });


}

function generateTable(name, data, divSelector) {

    var tableId = name + "_table";
    $(divSelector).replaceWith(`<table id=${tableId} class='display'></table>`);
    var tableSelector = `#${tableId}`;

    console.log(`Inserting table in ${tableSelector}`);


    insertHeaders(data.columns, tableSelector);

    return $(tableSelector).DataTable(data);

}

// function drawVariantsTable(data, divSelector) {
//     var tabsID = "vartable-tabs";
//     var contenID = "variant-tables";
//     $(divSelector).replaceWith(`<ul class="nav nav-tabs" role="tablist" id=${tabsID}></ul> <div class="tab-content" id=${contenID}></div>`);

//     var navTabs = $(`#${tabsID}`);
//     // console.log($(divSelector));
//     var tabContent = $(`#${contenID}`);

//     var first = true;
//     for (const varTable in data) {
//         var contentSelector = `#${varTable}`;
//         var tableName = `${varTable.toUpperCase()}`;

//         console.log(contentSelector);
//         if (first) { // First tab is active
//             navTabs.append(`<li class="nav-item">
//                 <a class="nav-link active" id="${varTable}-tab" data-toggle="tab" href="${contentSelector}" role="tab" 
//                 aria-controls="varTable" aria-selected="true">${tableName}</a></li>`);
//             tabContent.append(`<div class="tab-pane fade show active table-row" id="${varTable}" role="tabpanel" aria-labelledby="${varTable}-tab"></div>`);
//             first = false;
//         } else {
//             navTabs.append(`<li class="nav-item">
//                 <a class="nav-link" id="${varTable}-tab" data-toggle="tab" href="${contentSelector}" role="tab" 
//                 aria-controls="varTable" aria-selected="false">${tableName}</a></li>`);
//             tabContent.append(`<div class="tab-pane fade table-row" id="${varTable}" role="tabpanel" aria-labelledby="${varTable}-tab"></div>`);
//         }



//         var divSelector = insertDrawDiv(varTable);

//         generateTable(tableName, data[varTable], divSelector);
//     }
// }

function drawTable(table_name) {

    var divSelector = insertDrawDiv(table_name);
    // console.log(divSelector);

    var table = null;
    var dataRequest = requestData(table_name, 'table')
        .done(function (table_data) {
            // if (table_name == 'Variant') {
            //     // Make sub-tables
            //     drawVariantsTable(table_data, divSelector);
            // } else {
                table = generateTable(table_name, table_data, divSelector);
            // };
            // var tableId = table_name + "_table";
            // $(divSelector).replaceWith(`<table id=${tableId} class='display'></table>`);
            // var tableSelector = `#${tableId}`;
            // insertHeaders(table_data.columns, tableSelector);
            // table = $(tableSelector).DataTable(table_data);
        });
    // TODO: add fail and always callbacks as necessary
    return table
}


/*
 * Script that populates a page with figures
 */

// $("#v-pills-charts-tab").one("click", function () { //TODO: this should probably best be triggerd when the charts tab is selected for the first time
//     am4core.useTheme(am4themes_animated);
//     am4core.useTheme(am4themes_material);
//     $(".chart-row").each(function (index) {
//         // First chart is shown by default
//         if (index != 0) {
//             $(this).hide()
//         }

//         chart_name = $(this).prop("id"); //id of a chart div should correspond to the chart name as accepted by server side handlers

//         // console.log("Drawing chart");
        
//         $(`<h3> ${chart_name} </h3>`).appendTo(this);
//         chart = drawChart(chart_name);
//         // TODO: Eventual additional client-side processing/customization for specific charts
//     });

//     // Bind event handlers to dropdown

//     $("#chart-select-drop .dropdown-item").click(function () {
//         var showChart = $(this).data("chart");

//         // Make sure all other chart divs are hidden and show the selected one
//         // NOTE: It might be better to store the currently shown chart somewhere and only toggle the currently shown and newly selected ones
//         $(".chart-row").each( function () {
//             if ($(this).attr("id") == showChart) {
//                 $(this).show();
//             } else {
//                 $(this).hide();
//             }
//         })
//     });

//     // $(".table-row").each(function () {
//     //     table_name = $(this).prop("id"); //id of a table div should correspond to the table name as accepted by server side handlers

//     //     $(`<h3> ${table_name} </h3>`).appendTo(this);
//     //     table = drawTable(table_name);
//     //     // TODO: Eventual additional client-side processing/customization for specific tables
//     // });
// });