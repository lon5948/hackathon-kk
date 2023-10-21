window.onload = () => {
  // Generate client id
  const clientId = Math.floor(Math.random() * 1000000 + 1);
  const serverURL = "ws://hackathon-kk.dasbd72.com";
  const ws = new WebSocket(`${serverURL}/ws/chatroom/${clientId}`);

  const messages = [];
  const url = sessionStorage.getItem("url");
  iframeElement = document.getElementById("iframe-content");
  console.log(url);
  html_str = [
    "<iframe",
    "src=",
    url,
    'allow="autoplay; encrypted-media; clipboard-write"',
    'width="0"',
    'height="0"',
    'frameborder="0"',
    "allowfullscreen",
    ">",
    "</iframe>",
  ].join(" ");

  iframeElement.innerHTML = `${html_str}`;
  console.log(iframeElement);
  window.addEventListener("message", (event) => {
    if (event.data.command === "ping") {
      Array.from(document.querySelectorAll("iframe")).forEach((iframe) =>
        iframe?.contentWindow?.postMessage({ command: "pong" }, "*")
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
    var previousTimestamp = 0;
    var previousClientId = "";
    messages.forEach((message) => {
      const messageParsed = JSON.parse(message);

      if (messageParsed["event-type"] == "chat") {
        const isCurrentUser = messageParsed["client-id"] == clientId;
        const isContinuousMessage =
          previousClientId == messageParsed["client-id"] &&
          previousTimestamp != 0 &&
          messageParsed["timestamp"] - previousTimestamp < 10000;

        const dateElement = document.createElement("div");
        const date = new Date(messageParsed["timestamp"]).toLocaleString();
        dateElement.innerHTML = `${date}`;
        dateElement.className = "text-xs text-gray-400";

        const dateElementContainer = document.createElement("div");
        dateElementContainer.appendChild(dateElement);
        dateElementContainer.className =
          "w-full flex flex-row justify-center mt-2";

        const usernameElement = document.createElement("div");
        usernameElement.innerHTML = `${messageParsed["name"]} `;
        usernameElement.className = "text-xs ml-2 w-2/3";

        const messageElement = document.createElement("div");
        messageElement.className = `text-sm pl-2 py-2 px-3 ${
          isCurrentUser
            ? "bg-sky-400 rounded-bl-3xl rounded-br-xl rounded-tr-xl rounded-tl-3xl text-white"
            : "bg-gray-200 rounded-bl-xl rounded-br-3xl rounded-tr-3xl rounded-tl-xl text-black"
        }`;
        messageElement.innerHTML = `${messageParsed["message"]}`;

        const messageContainer = document.createElement("div");
        if (!isContinuousMessage) messageContainer.appendChild(usernameElement);
        messageContainer.appendChild(messageElement);
        messageContainer.className = `w-2/3 flex flex-col justify-${
          isCurrentUser ? "end" : "start"
        }`;

        const fullMessageContainer = document.createElement("div");
        fullMessageContainer.appendChild(messageContainer);
        fullMessageContainer.className = `w-full flex flex-row mt-1 justify-${
          isCurrentUser ? "end" : "start"
        }`;

        if (!isContinuousMessage)
          chatOutputContainer.appendChild(dateElementContainer);
        chatOutputContainer.appendChild(fullMessageContainer);

        previousTimestamp = messageParsed["timestamp"];
        previousClientId = messageParsed["client-id"];
      } else {
        const systemMessageElement = document.createElement("div");
        systemMessageElement.className =
          "text-xs text-gray-400 w-full flex flex-row justify-center mt-2";
        systemMessageElement.innerHTML = `${messageParsed["message"]}`;
        chatOutputContainer.appendChild(systemMessageElement);
      }
    });
    chatOutputContainer.scrollTop = chatOutputContainer.scrollHeight;
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
