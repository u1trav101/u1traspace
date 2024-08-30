const optionContent = document.getElementsByTagName("aside");
console.log(optionContent);


// switches the view to only show the selected pref category
const changeCategory = (category) => {
    for (let i in optionContent) {
        try {
            if (!optionContent[i].classList.contains("hidden")) {
                optionContent[i].classList.toggle("hidden");
            }
            if (optionContent[i].getAttribute("id") == category) {
                optionContent[i].classList.toggle("hidden");

                const curUrl = window.location.href.split('?')[0];
                const newUrl = curUrl + "?c=" + optionContent[i].getAttribute("id");

                history.replaceState(null, window.title, newUrl);
        }} catch (error) {}
    }
}