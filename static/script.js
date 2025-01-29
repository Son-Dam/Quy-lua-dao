document.addEventListener("DOMContentLoaded", function () {
    const socket = io();  // Connect to Flask-SocketIO server
    const dataDiv = document.getElementById("mqtt-data");

    socket.on("mqtt_message", function (data) {
        console.log("Received MQTT Data:", data);
        dataDiv.innerHTML = `
            <p><strong>Symbol:</strong> ${data.symbol}</p>
            <p><strong>Price:</strong> ${data.price}</p>
            <p><strong>Timestamp:</strong> ${data.timestamp}</p>
        `;
    });
});
