const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/'
);

chatSocket.onopen = function (e) {
    console.log('WebSocket connection established.');
};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(`Message from ${data.username}: ${data.message} at ${data.time}`);
};

chatSocket.onclose = function (e) {
    console.error('WebSocket closed unexpectedly.');
};