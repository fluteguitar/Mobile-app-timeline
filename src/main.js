


$(function () {
	$.ajaxSetup({
    // Disable caching of AJAX responses
    cache: false
	});
	// var data = $.get("messages.csv");
	// // console.log(JSON.stringify(data),data);
	// SHOULD BE PUT IN AN INDEX FILE BUT I AM LAZY, SORRY THE NEXT PROGRAMMER WHO HAS TO READ THESE LINE OF CODE!
	dir = "data/iOS/"
	rankFile = "ranking.csv";
	messageFile = 'message.csv';
	// versionLogFile = "database.csv";
	startDate = "01/01/2016"
	versionLogDir = dir + "version-logs/";
	iconDir = "data/icon/32px/"
	versionLogFile = ["App_Annie_Store_Stats_TimeLine_iOS_Messenger.csv",
					"App_Annie_Store_Stats_TimeLine_iOS_BIGO LIVE - Live Broadcasting.csv",
					"App_Annie_Store_Stats_TimeLine_iOS_Viber.csv",
					"App_Annie_Store_Stats_TimeLine_iOS_WeChat.csv",
					"App_Annie_Store_Stats_TimeLine_iOS_Zalo.csv"];

	var series = [];



    Highcharts.setOptions({
        global: {
            timezoneOffset: -7 * 60
        }
    });


	// Get and process input data

});

