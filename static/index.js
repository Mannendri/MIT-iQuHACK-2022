window.addEventListener("load", function(){


let socket = io.connect
('https://mit-iquhack-2022.mannendri.repl.co/')

let sendbtn = document.querySelector("#send-message");
let message = document.querySelector("#message");
let inbox = document.querySelector("#received-messages");

socket.on('connect',function(){
  console.log('User has connected!');
});


socket.on('message', function(msg){
  let msgNode = document.createTextNode(msg);

  //creates li element with message and appends it to ul
  inbox.appendChild(document.createElement("li").appendChild(msgNode));
  console.log("received message");

  
});

sendbtn.addEventListener("click", function(){
  socket.send(message.value);
  message.value = '';

});




});
  
