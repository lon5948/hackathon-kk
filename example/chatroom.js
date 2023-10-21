window.onload = () => {
  // Generate client id
  const clientId = Math.floor(Math.random() * 1000000 + 1);
  const serverURL = "ws://hackathon-kk.dasbd72.com";
  const ws = new WebSocket(`${serverURL}/ws/chatroom/${clientId}`);

  const messages = [];

  const constructMessage = (nickname, message) => {
    const messageObject = {
      timestamp: Date.now(),
      "event-type": "chat",
      "client-id": clientId,
      nickname: nickname,
      message: message,
    };
    return JSON.stringify(messageObject);
  };

  // Render messages on document.getElementById("chat-output-container")
  const renderMessages = () => {
    const chatOutputContainer = document.getElementById(
      "chat-output-container"
    );
    chatOutputContainer.innerHTML = "";
    messages.forEach((message) => {
      const messageParsed = JSON.parse(message);
      const messageElement = document.createElement("div");
      const date = new Date(messageParsed["timestamp"]).toLocaleString();
      messageElement.innerHTML = `${date} ${messageParsed["nickname"]} ${messageParsed["message"]}`;
      chatOutputContainer.appendChild(messageElement);
    });
  };

  ws.onopen = () => {
    // connection opened
  };

  ws.onmessage = (e) => {
    // a message was received
    console.log(e.data);
    messages.push(e.data);
    renderMessages();
  };

  ws.onerror = (e) => {
    // an error occurred
    console.log(e.message);
  };

  ws.onclose = (e) => {
    // connection closed
    console.log(e.code, e.reason);
  };

  // Send message on button click
  document.getElementById("chat-send").addEventListener("click", () => {
    const message = document.getElementById("chat-input").value;
    const nickname = document.getElementById("chat-nickname").value;
    ws.send(constructMessage(nickname, message));
  });
};
