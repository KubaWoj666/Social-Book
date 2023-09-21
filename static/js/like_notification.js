const request_user_id = JSON.parse(document.getElementById("request-user-id").textContent)
const request_user_username = JSON.parse(document.getElementById("request-user-username").textContent)
const like_btn = document.getElementById("like")
const form = document.getElementById("like-form")
// const notification = document.getElementById("notification")
// const notification_dropdown = document.getElementById("notification-dropdown")
// console.log(request_user_username);
// console.log(notification.textContent);

// notification_dropdown.innerHTML+=`
// <li >
//                 <span id="notification">dupa</span>
//               </li>
// `


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

    console.log(typeof(post_id));
    
    console.log(username + " - " + post_id + " - " + post_title);
    console.log(post_owner);
    
}


like_btn.addEventListener('click', (e)=>{
    console.log("clicke")
    form.innerHTML = `
    <button id="unlike" type="submit" class="btn btn-link "><i class="fa-solid fa-heart fa-xl " style="color: #f2075a;"></i></button>
    `
})