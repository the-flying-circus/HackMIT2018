$(document).ready(function() {
    $(".navbar-burger").click(function(e) {
        e.preventDefault();
        $(this).closest(".navbar").find(".navbar-menu").toggleClass("is-active");
    });
});
