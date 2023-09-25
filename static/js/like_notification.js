const request_user_id = JSON.parse(document.getElementById("request-user-id").textContent)
const request_user_username = JSON.parse(document.getElementById("request-user-username").textContent)




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
    data = JSON.parse(e.data)
    username = data.username
    post_id = data.post_id
    post_title = data.post_title
    post_owner = data.post_owner

    let span_num_of_notification = document.getElementById("number-of-notification")
    let num_of_notification = span_num_of_notification.innerHTML
    

    if (post_owner == request_user_username){
        
        const notification_dropdown = document.getElementById("notification-dropdown")
        notification_dropdown.innerHTML+=`
        <li>
              <div class="alert alert-primary" role="alert">
              ${username} liked ${post_title}
              </div>
            </li>
        
        `
        if (!num_of_notification) {
            span_num_of_notification.innerHTML = 1;
        } else {
            span_num_of_notification.innerHTML = parseInt(num_of_notification) + 1;                
        }

    }

}
    



