function drawChart(series, storeName) {
    	
    Highcharts.setOptions({
    	global: {
        	timezoneOffset: -7 * 60
    	}
	});
	
	Highcharts.stockChart('container', {

		colors: ['#018FE5', '#04C2FE', '#4AB40C', '#7B519C', 'orange'],
	    
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

