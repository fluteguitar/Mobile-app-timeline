$(function () {
    $.ajaxSetup({
	// Disable caching of AJAX responses
    	cache: false
    });
    prepareData( constants.ggplay, constants.messageFile ); 
    onClickButton();
});
