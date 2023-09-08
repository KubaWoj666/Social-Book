console.log("opa")

const id = JSON.parse(document.getElementById("user_id").textContent)
const request_user_username = JSON.parse(document.getElementById("request_user_id").textContent)
console.log(id)


const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
);

socket.onopen = function(e){
    console.log("connect")
};