$(document).ready(function() {
    $("#input").keydown(function(e) {
        var val = $(this).val();
        if (e.which == 13 && val) {
            $("#output").append("<div class='is-clearfix'><span class='msg'>" + $("<div />").text(val).html() + "</span></div>").scrollTop($("#output")[0].scrollHeight);
            e.preventDefault();
            $(this).val("");
        }
    }).focus();

    $.get("/gifs", function(data) {
        $("#gifs").children().remove()
        data.data.forEach(function(item) {
            var img = $("<img />").attr("src", item);
            $("#gifs").append(img);
        });
    });
});
