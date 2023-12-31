const user_username = JSON.parse(document.getElementById("request_user_username").textContent)


const online_socket = new WebSocket(
    "ws://"
    + window.location.host
    +'/ws/'
    +"online/"
)

online_socket.onopen = function(e){
    online_socket.send(JSON.stringify({
        "username": user_username,
        "type":"open",
        
    }))
}

window.addEventListener('beforeunload',(e)=>{
    online_socket.send(JSON.stringify({
        "username": user_username,
        "type": "close"
    }))
})

online_socket.onclose = function(e){
    console.log("Online status diconected");
}

online_socket.onmessage = function(e){
    var data = JSON.parse(e.data)
    if(data.username != user_username){
        var user_to_change = document.getElementById(`${data.username}_status`)
        var small_status_to_change = document.getElementById(`${data.username}_small`)
        if(data.online_status == true){
            user_to_change.style.color = 'green'
            small_status_to_change.textContent = 'Online'
        }else{
            user_to_change.style.color = 'grey'
            small_status_to_change.textContent = 'Offline'
        }
    }
}