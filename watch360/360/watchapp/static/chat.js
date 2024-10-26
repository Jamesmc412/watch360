const socket = new WebSocket('ws://localhost:8000/ws/chat/');

socket.onmessage = function(event) {
    const messages = document.getElementById('messages');
    const message = JSON.parse(event.data);
    messages.innerHTML += `<div>${message.content}</div>`;
};

document.getElementById('send-button').onclick = function() {
    const input = document.getElementById('message-input');
    const message = input.value;
    socket.send(JSON.stringify({ 'content': message }));
    input.value = '';
};
