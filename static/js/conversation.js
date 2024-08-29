let socket = null;
let messages = {};
let messagesDiv = null;
let renderedMessages = 0;
let messageCounts = {};
let recipientID = null;


const createSocket = recipientID => {
    userID = recipientID
    if (socket) { 
        if (socket.url.includes(`/msg/${recipientID}`)) return;
        else {
            socket.close()
            console.log("Closed current socket connection")
        };
    }

    messages = [];
    messagesDiv = document.getElementById(`messages-${recipientID}`)
    renderedMessages = 0;
    
    socket = new WebSocket(`/msg/${recipientID}`);
    socket.onopen = (event) => {
        console.log(`WebSocket opened on /msg/${recipientID}`);
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
        switch(msg.resource) {
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

const renderMessages = () => {
    if ((!messageCounts[userID]) || messages.length > messageCounts[userID]) {
        console.log("Rendering...");

        for (let i = renderedMessages; i < messages.length; i++) {
            // creating new elements
            const newMessage = document.createElement("div");
            const avatar = document.createElement("img");
            avatar.setAttribute("src", `https://cdn.u1trav101.net/u1traspace/usercontent/img/rsz/100px/${messages[i]["user_id"]}.webp`)
            const top = document.createElement("span");
            const right = document.createElement("div");
            const author = document.createElement("h4");
            const date = document.createTextNode(`at ${messages[i]["date"]}`);
            author.innerHTML = messages[i]["username"];
            const corpus = document.createElement("p");
            corpus.innerHTML = messages[i]["corpus"];
            
            // applying classes to new elements
            avatar.classList = "avatar";
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
            renderedMessages++;
    
            // scrolling to bottom
            messagesDiv.scrollTo(0, messagesDiv.scrollHeight);
        }
    }
}