$(function () {
	$.ajaxSetup({
	    // Disable caching of AJAX responses
    	cache: false
	});
	
	parseRankAndMessageAndLogs( constants.ggplay, constants.messageFile, constants.iconDir );
	
	onClickButton();
	// Get and process input data

});

