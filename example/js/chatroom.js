window.onload = () => {
  // Generate client id
  const clientId = Math.floor(Math.random() * 1000000 + 1);
  const serverURL = "ws://hackathon-kk.dasbd72.com";
  const ws = new WebSocket(`${serverURL}/ws/chatroom/${clientId}`);

  const messages = [];
  const url = sessionStorage.getItem("url");
  iframeElement = document.getElementById("iframe-content");
  console.log(url);
  html_str = ['<iframe',
    'src=',
    url,
    'allow="autoplay; encrypted-media; clipboard-write"',
    'width="0"',
    'height="0"',
    'frameborder="0"',
    'allowfullscreen',
    '>',
    '</iframe>'
  ].join(" ")
  
  iframeElement.innerHTML = `${html_str}`;
  console.log(iframeElement);
  window.addEventListener('message', event => {
    if (event.data.command === 'ping') {
      Array.from(document.querySelectorAll('iframe')).forEach(iframe =>
        iframe?.contentWindow?.postMessage({ command: 'pong' }, '*')
      );
    }
  });
  const constructMessage = (name, email, address, message) => {
    const messageObject = {
      timestamp: Date.now(),
      "event-type": "chat",
      "client-id": clientId,
      name: name,
      email: email,
      address: address,
      message: message
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
      const messageContainer = document.createElement("div");
      const date = new Date(messageParsed["timestamp"]).toLocaleString();
      const info = document.createElement("div")
      info.innerHTML = `${date} ${messageParsed["name"]} `;
      info.classList.add("chat-message");
      info.classList.add("text-xs");
      info.classList.add("ml-2");
      messageElement.classList.add("chat-message");
      messageElement.classList.add("text-sm");
      messageContainer.className = [
        "ml-2",
        "py-3",
        "px-4",
        "bg-gray-400",
        "rounded-bl-xl",
        "rounded-br-3xl",
        "rounded-tr-3xl",
        "rounded-tl-xl",
        "text-white",
        "justify-end",
        "mb-2"
      ].join(" ");      
      messageElement.innerHTML = `${messageParsed["message"]}`;
      messageContainer.appendChild(messageElement);
      chatOutputContainer.appendChild(info);
      chatOutputContainer.appendChild(messageContainer);
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
    const name = sessionStorage.getItem("name");
    const email = sessionStorage.getItem("email");
    const address = sessionStorage.getItem("address");
    ws.send(constructMessage(name, email, address, message));
  });
};
