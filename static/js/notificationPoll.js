const notificationPoll = async () => {
    const res = await fetch("/notifications/poll");
    const resJSON = await res.json();

    const interfaceType = document.getElementById("interface-type").getAttribute("value");

    const commentCounter = document.getElementById("comment-counter");
    const commentCounterA = document.getElementById("comment-counter-a");
    const friendCounter = document.getElementById("friend-counter");
    const friendCounterA = document.getElementById("friend-counter-a");
    const messageCounter = document.getElementById("message-counter");
    const messageCounterA = document.getElementById("message-counter-a");

    const comments = resJSON.profile_comment_approval + resJSON.blog_comment_approval;
    const friends = resJSON.friend_request_approval;
    const messages = resJSON.unseen_message;

    console.log(comments, friends, messages);

    const counterElements = [
        commentCounter, // 0
        friendCounter, // 1
        messageCounter, // 2
        commentCounterA, // 3
        friendCounterA, // 4
        messageCounterA, // 5
        comments, // 6
        friends, // 7
        messages, // 8
        "comment", // 9
        "friend", // 10
        "message" // 11
    ];
    
    // god came to me in a dream and told me to write this, now only he knows how it works (but it does)
    for (let i = 3; i < 6; i ++) {
        if (counterElements[i + 3]) {
            const counterString = `${counterElements[i + 3]} new ${counterElements[i + 6]}${counterElements[i + 3] !== 1 ? "s" : ""}!!`;

            switch (interfaceType) {
                default:
                    console.log("iterating");

                    counterElements[i - 3].innerHTML = counterString;
                    counterElements[i].style.display = "unset";
                    break;
            
                case "twitter":
                    counterElements[i].innerHTML = counterString;
                    counterElements[i].style.display = "block";
                    break;
            }
        } else {
            counterElements[i].style.display = "none";
        }
    }

    const oldCounter = parseInt(document.title.replace("[", ".").replace("]", ".").split(".")[1]);
    document.title = `[${comments + friends + messages}] ChiyoNET`;

    if (comments + friends + messages > oldCounter) {
        try {
            const audio = new Audio("/static/etc/notif.ogg");
            audio.play()
        } catch (DOMException) {}

    }
}

addEventListener("load", () => {
    notificationPoll()
    setInterval(notificationPoll, 10000);
});
