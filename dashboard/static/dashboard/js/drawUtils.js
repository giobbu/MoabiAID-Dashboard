/*
Inserts a div to draw the figure in (table, chart, ...) and inserts the ajax loader image as its child
*/
function insertDrawDiv(figure_name) {
    // console.log(figure_name);
    var table_row = `#${figure_name}`;
    // Make nested div
    var divID = figure_name + "_figure_div";
    // console.log(divID);
    $("<div></div>", {
            "id": divID,
            // "class": "h-25" //Bootstrap sizing utility
        })
        .appendTo(table_row);

    var divSelector = `#${divID}`;
    // console.log(divSelector);

    $("<img>", {
        "class": "img-responsive",
        "src": ajaxLoaderPath,
        "alt": ""
    }).appendTo(divSelector);

    return divSelector;

}

function requestData(reqData, usage) {
    var data_request = $.ajax({
        type: "GET",
        url: "/data",
        data: {
            data_usage: usage,
            data: reqData
        },
        dataType: "json"
    });
    return data_request;
}


