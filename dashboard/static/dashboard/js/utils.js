function getTimeIndex(times, timeFrame) {
    var curTime;
    if (timeFrame == 'now') {
        curTime = new Date();
    } else {
        curTime = new Date(timeFrame); //TODO: depending on the format of timeFrame we might need to instantiate this in the same way as below
    } 
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
            resIndex = timeIndex; //Update and break if we retrieve an historical time window, 
            break;
        }     
    }

    return resIndex;

}