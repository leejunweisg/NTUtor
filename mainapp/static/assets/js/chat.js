//Send function to send message using AJAX
// We define a variable 'text_box' for storing the html code structure of message that is displayed in the chat box.
var text_box = '<div class="card-panel right" style="width: 75%; position: relative">'  +
        '<div style="position: absolute; top: 0; left:3px; font-weight: bolder" class="title">{sender}</div>' + 
        '{message}' +
        '</div>';

function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 800);
}
// Send takes four args: listing_id, sender, receiver, message.
function send(listing_id, sender, receiver, message) {
    //POST to '/api/messages', the data in JSON string format
    $.post('/api/messages', '{"listingID": "'+ listing_id +'","sender": "'+ sender +'", "receiver": "'+ receiver +'","message": "'+ message +'" }', function (data) {
        console.log(data);
        var box = text_box.replace('{sender}', "You"); // Replace the text '{sender}' with 'You'
        box = box.replace('{message}', message); // Replace the text '{message}' with the message that has been sent.
        $('#board').append(box); // Render the message inside the chat-box by appending it at the end.
        scrolltoend(); // Scroll to the bottom of he chat-box
    })
}

// Receive function for receiving the messages
// Receive function sends a GET request to '/api/messages/<sender_id>/<receiver_id>/<listingID>' to get the list of messages. 
function receive() {
    // 'sender_id' and 'receiver_id' are global variable declared in the messages.html, which contains the ids of the users.
    $.get('/api/messages/'+ sender_id + '/' + receiver_id + '/' + listing_id , function (data) {
        console.log(data);
        if (data.length !== 0)
        {
            for(var i=0;i<data.length;i++) {
                console.log(data[i]);
                var box = text_box.replace('{sender}', data[i].sender);
                box = box.replace('{message}', data[i].message);
                box = box.replace('right', 'left blue lighten-5');
                $('#board').append(box);
                scrolltoend();
            }
        }
    })
}
