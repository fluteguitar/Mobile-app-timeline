function toTimestamp(date) {
	//Sample input format: "2016-01-01" (ISO date format)
	if (date.includes('-')) {
		date=date.split("-");
		date=date[1]+"/"+date[2]+"/"+date[0];
	}
	return (new Date(date).getTime());
}


function parseChangeLogs(changeLogs, startDate) {
	// changeLogs: Data to be used for HighCharts.flags
	// startDate: string (MM-DD-YYYY)
	var startDate = new Date(startDate).getTime();
	var processedData = [];

	// console.log(changeLogs);
	var previousLog = "";
	for (i = 0; i < changeLogs.length; i++) 
		if (changeLogs[i]["Update Type"] === "Version") {	
			var dateUTC = toTimestamp(changeLogs[i]["Date"]);
			var latestLog = changeLogs[i]["Notes"];
			if (latestLog === previousLog)
				continue;
			previousLog = latestLog;
			latestLog = "Version " + changeLogs[i]["New Value"] + ": " + latestLog;
			// console.log(changeLogs[i]);
			//title_ = changeLogs[i]["App Name"].split(" ")[0];

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

// Store type is either iOS or Google Play
function parseRankAndMessageAndLogs(storeType, messageFile, iconDir) {	
	// dir, rankFile, messageFile, versionLogDir, versionLogFile, startDate
	$.get(storeType.dir + storeType.rankFile, function(rank) {
		$.get(messageFile, function(message){
		// console.log(data);
		// Parsing app ranking 
		// console.log(storeType.dir + storeType.rankFile)
		var series = [];

		var rankData = Papa.parse(rank, {
			header: true,
			newline: "\n",
			skipEmptyLines: true
		});
		// console.log(rankData)
		rankData = rankData.data;
		var rank_header = Object.keys(rankData[0]);
		// select columns corresponding to app name within the table
		function creatSeriesElement(key) {
			//// console.log(kvArray);
			var newArr = rankData.map(function(obj){ 
				// // console.log(key, obj, obj[key]);
		   		return [toTimestamp(obj.Date), parseInt(obj[key])];
			});
			for (var i = 1; i < newArr.length; i++ )
				if ( ( newArr[i][1] <= 0 ) || ( newArr[i][1] >= 
					constants.rank_bound ) ) {
					newArr[i][1] = newArr[i-1][1];
				}
			return newArr;
		}

		for (var i = 1; i < rank_header.length; i++) {
			series[i-1] = {
				name: rank_header[i],
				data: creatSeriesElement(rank_header[i]),
				yAxis: 0,
				type: 'spline',
			}
		}

		// console.log(creatSeriesElement(rank_header[1]));
		// Parsing Zalo daily messages
		var messData = Papa.parse(message, {
			header: true,
			newline: "\n",
			skipEmptyLines: true
		});
		// console.log(rankData)
		messData = messData.data;		
		var mess_header = Object.keys(messData[0]);		

		messData = messData.map(function(obj){ 
			// console.log(key, obj, obj[key]);
	   		return [toTimestamp(obj[mess_header[0]]), parseInt(obj[mess_header[1]])];
		});

		series.push({
			type: 'line',
			id: "Zalo Daily message",
			name: mess_header[1],
			data: messData,
			// type: 'line',
			yAxis: 1
		});		
		// this variable is to check if data is finished reading.
		var counter = 0;
		storeType.versionLogFile.forEach(function(file) {
			$.get(storeType.versionLogDir + file, function(versionLog) {				
				// console.log(storeType.versionLogDir + file);
				// Read and parse data
				var versionLogData = Papa.parse(versionLog, {
					header: true,
					newline: "\n",
					skipEmptyLines: true
				});	
				
				// console.log(versionLogData);
				// only take the first words of the app name
				var appName = versionLogData.data[0]["App Name"].split(" ")[0];
				appName = appName.replace( ":", "" );
				console.log(appName);
				versionLogData =  parseChangeLogs(versionLogData.data, storeType.startDate, iconDir);
				// Added to chart
				series.push({
					// className: "Version logs",
			        type: 'flags',
			        name: "Logs " + appName,
			        data: versionLogData,
			        shape: 'url(' + iconDir + appName +  '.png)',
			        // useHTML: true,
			        color : 'orange',
			        allowPointSelect: true,
	    		});

	    		counter += 1;		
	    		if (counter === storeType.versionLogFile.length) {
	    			console.log(series);
					drawChart(series, storeType.name);
	    		}
			});
		});
		});
	});
}