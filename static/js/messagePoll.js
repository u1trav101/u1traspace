const messagePoll = async () => {
    const messageContainer = document.getElementById("message-container");
    const messages = messageContainer.children;

    const res = await fetch(`${window.location.href}/poll?t=${messages[0].getAttribute("value")}`);
    const resMessages = await res.json();

    if (resMessages[0]) {
        for (let i = 1; i < resMessages.length; i++) {
            const newMessage = document.createElement("div");
            newMessage.setAttribute("value", resMessages[i]["messageid"]);
            newMessage.classList.add("msg");

            const timestamp = document.createElement("span");
            timestamp.innerHTML = `[${resMessages[i]["date"]}]`;
            timestamp.classList.add("timestamp");
            newMessage.appendChild(timestamp);

            const username = document.createElement("span");
            username.innerHTML = `[${resMessages[i]["username"]}]`;
            username.classList.add("username");
            newMessage.appendChild(username);

            const content = document.createElement("span");
            content.innerHTML = resMessages[i]["corpus"];
            content.classList.add("content");
            newMessage.appendChild(content);

            messageContainer.insertBefore(newMessage, messageContainer.firstChild);
        }
    }
}

addEventListener("load", () => {
    messagePoll()
    setInterval(messagePoll, 2000);

    const input = document.getElementById("message-input");
    input.focus()
});
