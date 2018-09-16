$(document).ready(function() {
    var socket = io();

    function showMessage(cls, msg) {
        if (/^https?:\/\/media\d+.giphy.com\/media\/[a-zA-Z0-9]+\/giphy-preview.gif$/.test(msg)) {
            $("#output").append("<div class='is-clearfix'><span class='" + cls + "'><img src='" + msg + "' /></span></div>");
        }
        else {
            $("#output").append("<div class='is-clearfix'><span class='" + cls + "'>" + $("<div />").text(msg).html() + "</span></div>").scrollTop($("#output")[0].scrollHeight);
        }
    }

    socket.on("message", function(data) {
        showMessage("msg other", data);
    });

    function sendMessage(msg) {
        showMessage("msg", msg);
        socket.emit("message", msg);
    }

    $("#input").keydown(function(e) {
        var val = $(this).val();
        if (e.which == 13 && val) {
            e.preventDefault();
            sendMessage(val);
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

    $("#gifs").on("click", "img", function(e) {
        e.preventDefault();
        sendMessage($(this).attr("src"));
        $("#gifs").hide();
    });

    $("#gif-button").click(function(e) {
        e.preventDefault();
        $("#gifs").toggle().css({
            "top": ($(this).offset().top - $("#gifs").height() - 55) + "px",
            "left": ($(this).offset().left - $("#gifs").width() - 5) + "px"
        });
    });
});