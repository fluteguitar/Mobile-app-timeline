function setDataProperties(series, iconDir) {
    for (let i = 0; i < series.length; i++)
	if (series[i].type === "rank") {
	    series[i].type = "spline";
	    series[i].yAxis = 0;
	} else if (series.type === "message") {
	    series[i].type = "line";
	    series[i].yAxis = 1;
	    series[i].id = "Zalo daily message";
	} else {
	    series[i].type = "flags";
	    series[i].shape = 'url(' + iconDir + series[i].appName +  '.png)';
	    series[i].allowPointSelect = true;
	};

    return series;
}


function getSeriesColors(series) {
    let arr = [];
    for (let i = 0; i < series.length; i++)
	if ((series[i].yAxis + 1) && (series[i].yAxis === 0)) {
	    arr.push( appsColorMap[series[i].name] );
	}

    return arr;
};


function drawChart(series, storeName, appsColorMap) {
    
    Highcharts.setOptions({
    	global: {
            timezoneOffset: -7 * 60
    	}
    });

    let color_ = getSeriesColors(series);
    series = setDataProperties(series, constants.iconDir);
    
    Highcharts.stockChart('container', {

	colors: color_,
	
	rangeSelector: {
	    selected: 1
	},
	
	legend: {
	    enabled: true,
	    layout: 'horizontal',
	    maxHeight: 100,
	    borderWidth: 4,
	    borderColor: '#e3e4e0',
	    backgroundColor: '#eeffc5',
	    padding: 15,
	    itemDistance: 40,
	    itemStyle: {
        	color: '#000000',
        	fontSize: '15px'
    	    }
	},

        tooltip: {
            headerFormat:  '<span style="font-size: 12px">{point.key}</span><br/>',
            style: {
            	width: '200px',
            	fontSize: '11pt'
            },
            borderColor: '#e3e4e0',
            backgroundColor: '#eeffc5'
	},
	title: {
	    text: 'Timeline of apps rank, version logs and Zalo messages on ' + storeName,
	    style: {
            	color: '#234CA4',
            	fontSize: '20pt',
            	// 'padding-top': '50px',
            	fontWeight: 'bold',
            }
	},
	yAxis: [{
	    reversed: true,	
	    title: {
		text: 'Daily app rank',
		style: {
            	    color: '#234CA4',
            	    fontSize: '15pt',
            	    // 'padding-top': '50px',
            	    fontWeight: 'bold',
        	}
	    },
	    height: '50%',			        
	    lineWidth: 2,
	    offset: 50,
	    min: 0,
	},
	        {
		    title: {
		        text: 'Daily total messages',
		        style: {
            		    color: '#234CA4',
            		    fontSize: '15pt',
            		    // 'padding-top': '50px',
            		    fontWeight: 'bold',
        		}
		    },
		    top: '50%',	
		    lineWidth: 2,
		    height: '50%',
		    offset: 50,
	    	}
	       ],
	series: series
    }); 
}

