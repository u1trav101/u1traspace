let socket = null;
let messages = {};
let messagesDiv = null;
let renderedMessages = {};
let messageCounts = {};
let recipientID = null;
let avatarImages = {};


const createSocket = recipientID => {
    userID = recipientID
    if (socket) {
        if (socket.url.includes(`/messages/${recipientID}`)) return;
        else {
            socket.close()
            console.log("Closed current socket connection")
        };
    }

    messages = [];
    messagesDiv = document.getElementById(`messages-${recipientID}`)

    if (!renderedMessages[userID]) renderedMessages[[userID]] = 0;

    socket = new WebSocket(`/messages/${recipientID}`);
    socket.onopen = (event) => {
        console.log(`WebSocket opened on /messages/${recipientID}`);
        socket.send(JSON.stringify({
            type: "get",
            resource: "messages"
        }))

        setInterval(refreshMessages, 500)
    };
    socket.onmessage = (event) => {
        receiveMessage(event);
    }
}

const refreshMessages = () => {
    console.log("Refreshing messages...");

    socket.send(JSON.stringify({
        type: "poll",
        resource: "messages"
    }))
}

const sendMessage = textarea => {
    if (textarea.value.trim() !== "") {
        console.log("Sending new message...");

        socket.send(JSON.stringify({
            type: "post",
            resource: "messages",
            data: textarea.value
        }));

        textarea.value = "";
    }
}

const receiveMessage = event => {
    const msg = JSON.parse(event.data);

    if (msg.type === "get") {
        switch (msg.resource) {
            default:
                break;
        }
    }
    else if (msg.type === "post") {
        switch (msg.resource) {
            case "messages":
                console.log("Receiving messages...");

                if (msg.data.constructor != Object) {
                    messages = messages.concat(msg.data);
                } else {
                    messages.push(msg.data);
                }

                renderMessages();
                messageCounts[userID] = messages[messages.length]

                break;

            default:
                break;
        }
    }
}

const renderAvatars = (userID) => {
    console.log("Rendering profile pictures...")
    const avatarElms = document.getElementsByClassName(`avatar ${userID}`);

    for (let i = 0; i < avatarElms.length; i++) {
        avatarElms[i].setAttribute("src", avatarImages[userID] ?
            `https://cdn.u1trav101.net/u1traspace/usercontent/img/rsz/100px/${userID}.webp` :
            "https://cdn.u1trav101.net/u1traspace/usercontent/img/rsz/100px/default.webp"
        );
    }
}

const avatarExists = async (userID, callback) => {
    fetch(`https://cdn.u1trav101.net/u1traspace/usercontent/img/rsz/100px/${userID}.webp`, {
        method: "head",
        mode: "cors",
        headers: {
            "Access-Control-Allow-Origin": "*"
        }
    })
        .then(status => {
            callback(status.ok);
        })
        .catch(() => {
            callback(true);
        });
}

const renderMessages = () => {
    if ((!messageCounts[userID]) || messages.length > messageCounts[userID]) {
        console.log("Rendering...");

        for (let i = renderedMessages[userID]; i < messages.length; i++) {
            // creating new elements
            const newMessage = document.createElement("div");
            const avatar = document.createElement("img"); // checking whether the message author has a profile picture
            if (avatarImages[messages[i]["user_id"]] === true) {
                avatar.setAttribute("src", `https://cdn.u1trav101.net/u1traspace/usercontent/img/rsz/100px/${messages[i]["user_id"]}.webp`);
            } else {
                if (!avatarImages[messages[i]["user_id"]] && avatarImages[[messages[i]["user_id"]]] !== "pending") {
                    avatarImages[messages[i]["user_id"]] = "pending";
                    console.log(`Checking if user ${messages[i]["user_id"]} has a profile picture...`);

                    avatarExists(`${messages[i]["user_id"]}`, exists => {
                        avatarImages[messages[i]["user_id"]] = exists;
                        console.log(`User ${messages[i]["user_id"]} ${exists ? "has" : "doesn't have"} a profile picture.`);

                        renderAvatars(messages[i]["user_id"]);
                    });
                }
            }
            const top = document.createElement("span");
            const right = document.createElement("div");
            const author = document.createElement("h4");
            author.innerHTML = messages[i]["username"];
            const date = document.createTextNode(`at ${messages[i]["date"]}`);
            const corpus = document.createElement("p");
            corpus.innerHTML = messages[i]["corpus"];

            // applying classes to new elements
            avatar.classList = `avatar ${messages[i]["user_id"]}`;
            newMessage.classList = "message";
            top.classList = "top";
            right.classList = "right"
            author.classList = "username";
            corpus.classList = "corpus";

            // organising new element tree
            top.appendChild(author);
            top.appendChild(date);
            right.appendChild(top)
            right.appendChild(corpus)
            newMessage.appendChild(avatar);
            newMessage.appendChild(right);

            // rendering element
            messagesDiv.appendChild(newMessage);

            // incrementing counter of rendered messages
            renderedMessages[userID]++

            // scrolling to bottom
            messagesDiv.scrollTo(0, messagesDiv.scrollHeight);
        }
    }
}
