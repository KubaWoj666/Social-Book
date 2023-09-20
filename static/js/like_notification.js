const request_user_id = JSON.parse(document.getElementById("request-user-id").textContent)
const request_user_username = JSON.parse(document.getElementById("request-user-username").textContent)
const like_btn = document.getElementById("like")
console.log(request_user_username);


const like_websocket = new WebSocket(
    "ws://"
    + window.location.host
    + "/ws/"
    + "like-notification/"
)


like_websocket.onopen = (e)=>{
    console.log("like_websocket connected" );
    like_websocket.send(JSON.stringify({
        "request_user_id": request_user_id,
    }))
}

like_websocket.onclose = (e)=>{
    console.log("like_websocket disconected");
}

like_websocket.onmessage = (e)=>{
    
}


