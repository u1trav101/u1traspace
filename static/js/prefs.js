// retrieves required elements
const avatarPreview = document.getElementById("avatar-preview");
const avatarUpload = document.getElementById("avatar-upload");
const audioUploadLabel = document.getElementById("audio-upload-label");
const audioUpload = document.getElementById("audio-upload");
const cancelAudio = document.getElementById("cancel-audio");
const cssTextArea = document.getElementById("css");
const prefCategories = Array.prototype.filter.call(
    document.getElementsByClassName("pref-category"),
    (element) => element.nodeName === "ASIDE"
)

// switches the view to only show the selected pref category
const changeCategory = (category) => {
    for (let i in prefCategories) {
        if (!prefCategories[i].classList.contains("hidden")) {
            prefCategories[i].classList.toggle("hidden");
        }
    }

    prefCategories[category].classList.toggle("hidden");

    const curUrl = window.location.href.split('?')[0];
    const newUrl = curUrl + "?c=" + prefCategories[category].getAttribute("id");
    history.replaceState(null, window.title, newUrl)
}

// cancels audio upload
const cancelAudioAction = () => {
    audioUpload.value = "";
    audioUploadLabel.innerText = "upload song";
    cancelAudio.classList = "cancel-audio hidden";
}

// initiialises ace code editor for css editing
const editor = ace.edit("ace");
editor.setTheme("ace/theme/dracula");
editor.session.setMode("ace/mode/css");
editor.session.setValue(cssTextArea.value);
editor.session.on("change", () => {
    cssTextArea.value = editor.session.getValue();
});
editor.setOptions({
    minLines: 5,
    maxLines: 20,
    fontSize: "1rem",
    fontFamily: "fira-code"
});

// responsively changes the user avatar to match the selected file
avatarUpload.addEventListener("change", (event) => {
    const newAvatar = event.target.files[0];
    const fileReader = new FileReader();

    fileReader.onload = (event) => {
        avatarPreview.src = event.target.result;
    }

    fileReader.readAsDataURL(newAvatar);
});

// responsively changes the upload song text to match the filename of the uploaded song
audioUpload.addEventListener("change", (event) => {
    const newAudio = event.target.files[0];
    audioUploadLabel.innerText = newAudio.name;

    // shows a button to cancel song upload
    cancelAudio.classList = "cancel-audio"
});