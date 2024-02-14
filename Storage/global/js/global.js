// global js
// @auther:  github.com/alisharify7
const burger_menu = document.querySelector("#navbar-burger-menu");
if (burger_menu) {
    burger_menu.addEventListener("click", function (e) {
        burger_menu.classList.toggle("burger_active");
    });
}
