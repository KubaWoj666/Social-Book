
const id = JSON.parse(document.getElementById("user_id").textContent)
const request_user_username = JSON.parse(document.getElementById("request_user_username").textContent)
const message_username = JSON.parse(document.getElementById("user_username").textContent)

const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
)

socket.onopen = function(e){
    // console.log("connected")
}

socket.close = function(e){
    // console.log("disconected")
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data)
    if (data.username == message_username){
        document.querySelector('#chat-body').innerHTML += 
        `
        <td>
            <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">
                ${data.message}
            </p>
        </td>
        ` 
    }else{
        document.querySelector('#chat-body').innerHTML += `
        <td>
            <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">
                ${data.message}
            </p>
        </td>
        `
        

    }  
}


document.querySelector("#message_input").focus()
document.querySelector("#message_input").onkeyup = function(e){
    if (e.key === 'Enter'){
        document.getElementById("chat-message-submit").click()
    }
}

document.querySelector('#chat-message-submit').onclick = function(e){
    const message_input = document.querySelector("#message_input");
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message':message,
        'username':message_username,
        'sender_username': request_user_username
    }));
    message_input.value = "";  
} 