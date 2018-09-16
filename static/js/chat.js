$(document).ready(function() {
    var currentRecipient = null;
    var socket = io();

    function showConversation(peer) {
        currentRecipient = peer.social_id;

        $("#partner").text(peer.display);

        $("#output .msg").remove();
        $.get("/chat/history?other=" + encodeURIComponent(currentRecipient), function(data) {
            if (data.error) {
                return;
            }
            data.data.forEach(function(item) {
                showMessage("msg" + (item.sender == data.id ? " " : " other"), item.message);
            });
        });
    }

    $.get("/chat/conversations", function(data) {
        $("#peers").children().remove();
        data.data.forEach(function(item) {
            $("#peers").append($("<div class='peer' />").text(item.display).attr("data-id", item.social_id));
        });

        if (data.data.length > 0) {
            showConversation(data.data[0]);
            $("#find").text("Find a new mentor");
        } else {
            $("#find").text("Find a Mentor");
        }
    });

    $("#peers").on("click", ".peer", function(e) {
        showConversation({
            "social_id": $(this).attr("data-id"),
            "display": $(this).text()
        });
        e.preventDefault();
    });

    $("#find").click(function(e) {
        e.preventDefault();
        $.post("/pair_mentor", function(data) {
            if (data.success) {
                window.location.reload();
            }
            else if (data.error) {
                Messenger().error(data.error);
            }
        });
    });

    function showMessage(cls, msg) {
        if (/^https?:\/\/media\d+.giphy.com\/media\/[a-zA-Z0-9]+\/giphy-preview.gif$/.test(msg)) {
            $("#output").append("<div class='is-clearfix'><span class='" + cls + "'><img src='" + msg + "' /></span></div>");
        }
        else {
            $("#output").append("<div class='is-clearfix'><span class='" + cls + "'>" + $("<div />").text(msg).html() + "</span></div>");
        }
        $("#output").scrollTop($("#output")[0].scrollHeight);
    }

    socket.on("message", function(data) {
        if (data.owner == currentRecipient) {
            showMessage("msg other", data.contents);
        }
    });

    socket.on("reload", function(data) {
        window.location.reload(true);
    });

    function sendMessage(msg) {
        if (currentRecipient !== null) {
            showMessage("msg", msg);
            socket.emit("message", msg, currentRecipient);
        }
    }

    $("#input").keydown(function(e) {
        var val = $(this).val();
        if (e.which == 13 && val && currentRecipient !== null) {
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
