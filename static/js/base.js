$(document).ready(function() {
    $(".navbar-burger").click(function(e) {
        e.preventDefault();
        $(this).closest(".navbar").find(".navbar-menu").toggleClass("is-active");
    });

    $("#input").keydown(function(e) {
        var val = $(this).val();
        if (e.which == 13 && val) {
            $("#output").append("<div class='is-clearfix'><span class='msg'>" + $("<div />").text(val).html() + "</span></div>").scrollTop($("#output")[0].scrollHeight);
            e.preventDefault();
            $(this).val("");
        }
    }).focus();
});
