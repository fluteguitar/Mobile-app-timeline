function toTimestamp(date) {
    //Sample input format: "2016-01-01" (ISO date format)
    if (date.includes('-')) {
	date=date.split("-");
	date=date[1]+"/"+date[2]+"/"+date[0];
    }
    return (new Date(date).getTime());
}


function refineAppsVersionLogs(versionLogs, startDate) {
    // versionLogs: Data to be used for HighCharts.flags
    // startDate: string (MM-DD-YYYY)
    var startDate = new Date(startDate).getTime();
    var processedData = [];

    // console.log(versionLogs);
    var previousLog = "";
    for (i = 0; i < versionLogs.length; i++) 
	if (versionLogs[i]["Update Type"] === "Version") {	
	    var dateUTC = toTimestamp(versionLogs[i]["Date"]);
	    var latestLog = versionLogs[i]["Notes"];
	    if (latestLog === previousLog)
		continue;
	    previousLog = latestLog;
	    latestLog = "Version " + versionLogs[i]["New Value"] + ": " + latestLog;
	    // console.log(versionLogs[i]);
	    //title_ = versionLogs[i]["App Name"].split(" ")[0];

	    if (dateUTC >= startDate) {
		var new_element = {
		    x: dateUTC,
		    // Only take the first word to shorten for better displaying
		    title: ' ',
		    text: latestLog,
		};
		// console.log(new_element.text);
		processedData.push(new_element);
	    }
	}

    processedData.sort(function(a, b) {return a.x > b.x});
    return processedData;
}

//pparse Ranking of app
function parseRank(rank) {

    let series = [];

    let rankData = Papa.parse(rank, {
	header: true,
	newline: "\n",
	skipEmptyLines: true
    });
    // console.log(rankData)
    rankData = rankData.data;
    let rankHeader = Object.keys(rankData[0]);

    // select columns corresponding to app name within the table
    function creatSeriesElement(key) {
	//// console.log(kvArray);
	let newArr = rankData.map(function(obj){ 
	    // // console.log(key, obj, obj[key]);
	    return [toTimestamp(obj.Date), parseInt(obj[key])];
	});
	for (let i = 1; i < newArr.length; i++ )
	    if ( ( newArr[i][1] <= 0 ) || ( newArr[i][1] >= 
					    constants.rank_bound ) ) {
		newArr[i][1] = newArr[i-1][1];
	    }
	return newArr;
    }

    for (let i = 1; i < rankHeader.length; i++) {
	series[i-1] = {
	    name: rankHeader[i],
	    data: creatSeriesElement(rankHeader[i]),
	    type: 'rank',
	}
    }

    return series;    
}


//Parse message from Zalo
function parseZaloMessgage(message) {
    let messData = Papa.parse(message, {
	header: true,
	newline: "\n",
	skipEmptyLines: true
    });

    messData = messData.data;		
    let messHeader = Object.keys(messData[0]);		
    messData = messData.map(function(obj){ 
	return [toTimestamp(obj[messHeader[0]]), parseInt(obj[messHeader[1]])];
    });

    return [messHeader, messData];
}


function parseAppsVersionLogs(storeType, file, versionLogs) {
    let versionLogsData = Papa.parse(versionLogs, {
	header: true,
	newline: "\n",
	skipEmptyLines: true
    });	
    
    let appName = versionLogsData.data[0]["App Name"].split(" ")[0];
    appName = appName.replace( ":", "" );    
    versionLogsData =  refineAppsVersionLogs(versionLogsData.data, storeType.startDate);

    return [appName, versionLogsData];
}


// Store type is either iOS or Google Play
function prepareData(storeType, messageFile) {	
    $.get(storeType.dir + storeType.rankFile, function(rank) {
	$.get(messageFile, function(message){
	    let series = parseRank(rank);
	    message = parseZaloMessgage(message);
	    series.push({
		name: message[0],
		data: message[1],
		type: 'message',
	    });		

	    // this variable is to check if data is finished reading.
	    let counter = 0;
	    storeType.versionLogFile.forEach(function(file) {
		$.get(storeType.versionLogDir + file, function(versionLogs) {
		    versionLogs = parseAppsVersionLogs(storeType, file, versionLogs);
		    // Added to chart
		    series.push({
			type: 'versionLogs',
			appName: versionLogs[0],
			name: "Logs " + versionLogs[0],
			data: versionLogs[1],
	    	    });

	    	    counter += 1;		
	    	    if (counter === storeType.versionLogFile.length) {
	    		console.log(series);
			drawChart(series, storeType.name, appsColorMap);
	    	    }
		});
	    });
	});
    });
}
