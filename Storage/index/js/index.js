window.addEventListener("resize", e => {
    // close mobile size category modal
    if (window.innerWidth >= 765) {
        $("#category-modal > div > div > div.modal-header > button").click()
    }
})



$(document).ready(function () {
    const owl_carousel_slider = $(".owl-carousel-slider");
    owl_carousel_slider.owlCarousel({
        rtl: true,
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        autoplayTimeout: 2000,
        autoplayHoverPause: true,
        // lazyContent: true,
        lazyLoad: true,
        center: true,
        nav: true,
        responsive: {
            0: {
                items: 1,
            },
        },
    });

    const news_owl = $(".news-slider");
    news_owl.owlCarousel({
        rtl: true,
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        autoplayTimeout: 2000,
        autoplayHoverPause: true,
        lazyContent: true,
        lazyLoad: true,
        center: true,
        nav: true,
        dots: true,
        pagination: false,
        navigation: true,
        responsive: {
            0: {
                items: 1,
            },
            250: {
                items: 1,
            },
            650: {
                items: 2,
            },
            980: {
                items: 3,
            },
        },
        navText: ["<i class='bi bi-chevron-right display-4 fw-bold mt-3 '></i>", "<i class='bi bi-chevron-left display-4 fw-bold mt-3 '></i>"]

    });

    const product_owl = $(".product-slider");
    product_owl.owlCarousel({
        rtl: true,
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        autoplayTimeout: 1000,
        autoplayHoverPause: true,
        // lazyContent: true,
        // lazyLoad: true,
        center: true,
        nav: true,
        dots: true,
        pagination: false,
        navigation: true,
        responsive: {
            0: {
                items: 1,
            },
            250: {
                items: 1,
            },
            450: {
                items: 2,
            },
            650: {
                items: 3,
            },
            980: {
                items: 4,
            },
            1300: {
                items: 4,
            },
        },
        navText: ["<i class='bi bi-chevron-right display-4 fw-bold mt-3 '></i>", "<i class='bi bi-chevron-left display-4 fw-bold mt-3 '></i>"]

    });

    const top_products_slider = $(".TopProductsSlider");
    top_products_slider.owlCarousel({
        rtl: true,
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        autoplayTimeout: 1500,
        autoplayHoverPause: true,
        lazyContent: true,
        lazyLoad: true,
        center: true,
        nav: false,
        dots: false,
        pagination: false,
        navigation: true,
        responsive: {
            0: {
                items: 1,
            }
        },
        navText: ["<i class='bi bi-chevron-right display-4 fw-bold mt-3 '></i>", "<i class='bi bi-chevron-left display-4 fw-bold mt-3 '></i>"]

    });

    const partership_owl = $(".partnership-company-slider");
    partership_owl.owlCarousel({
        rtl: true,
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        autoplayTimeout: 1000,
        autoplayHoverPause: true,
        lazyLoad: true,
        center: true,
        nav: false,
        dots: false,
        pagination: false,
        navigation: false,
        responsive: {
            0: {
                items: 2,
            },
            400: {
                items: 3,
            },
            980: {
                items: 4,
            },
            1300: {
                items: 6,
            },
        },
        navText: ["<i class='bi bi-chevron-right display-4 fw-bold mt-3 '></i>", "<i class='bi bi-chevron-left display-4 fw-bold mt-3 '></i>"]

    });


});
