const generatePureText = (text) => {
  const element = document.createElement("div");
  element.innerText = text;
  return element.innerHTML;
};
const construct = (eventType, message) => {
  const clientId = sessionStorage.getItem("clientId");
  const name = localStorage.getItem("name");
  const email = localStorage.getItem("email");
  const address = localStorage.getItem("address");
  const messageObject = {
    timestamp: Date.now(),
    "event-type": eventType,
    "client-id": clientId,
    name: name,
    email: email,
    address: address,
    message: message,
  };
  return JSON.stringify(messageObject);
};
const constructJoinMessage = () => {
  return construct("join", "Joined");
};
const constructMessage = (message) => {
  return construct("chat", message);
};

window.onload = () => {
  // Generate client id
  const clientId = Math.floor(Math.random() * 1000000 + 1);
  const serverURL = "ws://hackathon-kk.dasbd72.com";
  const ws = new WebSocket(`${serverURL}/ws/chatroom/${clientId}`);
  sessionStorage.setItem("clientId", clientId);

  const messages = [];
  const url = localStorage.getItem("url");
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
        dateElement.innerText = `${date}`;
        dateElement.className = "text-xs text-gray-400";

        const dateElementContainer = document.createElement("div");
        dateElementContainer.appendChild(dateElement);
        dateElementContainer.className =
          "w-full flex flex-row justify-center mt-2";

        const usernameElement = document.createElement("div");
        usernameElement.innerText = `${messageParsed["name"]} `;
        usernameElement.className = "text-xs ml-2";

        const messageElement = document.createElement("div");
        messageElement.className = `text-sm break-words py-2 px-3 w-fit ${
          isCurrentUser
            ? "pl-4 bg-sky-400 rounded-bl-3xl rounded-br-xl rounded-tr-xl rounded-tl-3xl text-white"
            : "pr-4 bg-gray-200 rounded-bl-xl rounded-br-3xl rounded-tr-3xl rounded-tl-xl text-black"
        }`;
        messageElement.innerText = `${messageParsed["message"]}`;

        const messageContainer = document.createElement("div");
        if (!isContinuousMessage) messageContainer.appendChild(usernameElement);
        messageContainer.appendChild(messageElement);
        messageContainer.className = `min-w-[20%] max-w-[60%] flex flex-col justify-${
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
    console.log("Connected to server");
    ws.send(constructJoinMessage());
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

  // send message by pressing enter
  document
    .getElementById("chat-input")
    .addEventListener("keyup", function (event) {
      if (event.key === "Enter") {
        document.getElementById("chat-send").click();
      }
    });

  // Send message on button click
  const sendMessage = () => {
    const chatInputElement = document.getElementById("chat-input");
    const message = chatInputElement.value;
    if (message == "") return;
    ws.send(constructMessage(message));
    chatInputElement.value = "";
  };
  document.getElementById("chat-send").addEventListener("click", (e) => {
    if (e.isTrusted) sendMessage();
  });
  document
    .getElementById("chat-input")
    .addEventListener("keypress", function (e) {
      if (e.ctrlKey && e.key === "Enter") {
        sendMessage();
      }
    });
};
