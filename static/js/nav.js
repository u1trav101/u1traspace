const navCategories = Array.prototype.filter.call(
    document.getElementsByClassName("nav-category"),
    (element) => element.nodeName === "ASIDE"
)

// switches the view to only show the selected pref category
const changeCategory = (category) => {
    for (let i in navCategories) {
        if (!navCategories[i].classList.contains("hidden")) {
            navCategories[i].classList.toggle("hidden");
        }
    }

    navCategories[category].classList.toggle("hidden");

    const curUrl = window.location.href.split('?')[0];
    const newUrl = curUrl + "?c=" + navCategories[category].getAttribute("id");
    history.replaceState(null, window.title, newUrl)
}