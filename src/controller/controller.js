function onClickButton() {
    $("button").on("click", function(){
        var label = $( "button" ).find("label").html()
        if (label === "Switch to GgPlay") {
            $( "button" ).find("label").html("Switch to iOS");
            parseRankAndMessageAndLogs( constants.ggplay, constants.messageFile, constants.iconDir );
        } else {
            $( "button" ).find("label").html("Switch to GgPlay");
            parseRankAndMessageAndLogs( constants.iOS, constants.messageFile, constants.iconDir );
        }
        // alert('from button() : I was triggered!');
    });
}
