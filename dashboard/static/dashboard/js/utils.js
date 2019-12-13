function getTimeIndex(times, timeFrame) {
    var curTime = timeFrame; //For the simulation
    // NOTE: we currently hard-code the current time
    // if (timeFrame == 'now') {
    //     curTime = new Date();
    // } else {
    //     curTime = new Date(timeFrame); //TODO: depending on the format of timeFrame we might need to instantiate this in the same way as below
    // } 
    var year = curTime.getFullYear();
    var month = curTime.getMonth();
    var day = curTime.getDate();

    var resIndex;

    for (var timeIndex in times) {
        var [hours, mins, secs] = times[timeIndex].split(':');
        var timeVal = new Date(year, month, day, hours, mins, secs);
        // timeVal is the upper bound of the time window
        if (timeVal <= curTime) {
            resIndex = timeIndex;
        } else if(timeFrame == 'now'){ //Window that was chosen in the last loop is the last available one
            break;
        } else {
            //resIndex = timeIndex; //Update and break if we retrieve an historical time window, 
            break;
        }     
    }

    var timewindow = `[${resIndex == 0 ? times[times.length-1] : times[resIndex-1]} -- ${times[resIndex]}]`;
    console.log(`Reading data for time window: ${timewindow}`);

    $('#current-timeframe').text(`Currently shown time window: ${timewindow}`);
    

    return resIndex;

}

function getTypicalData(dataType) {
    return $.get("/data/", {
        data_usage: "typical",
        table: "dataType" // IF this is relevant
    });
}

/*
Uppercase only the first charachter of a string
Copied from: https://dzone.com/articles/how-to-capitalize-the-first-letter-of-a-string-in
*/
function jsUcfirst(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}