function onClickButton() {
    $("button").on("click", function(){
        var label = $( "button" ).find("label").html()
        if (label === "Switch to GgPlay") {
            $( "button" ).find("label").html("Switch to iOS");
            prepareData( constants.ggplay, constants.messageFile);
        } else {
            $( "button" ).find("label").html("Switch to GgPlay");
            prepareData( constants.iOS, constants.messageFile );
        }
        // alert('from button() : I was triggered!');
    });
}
