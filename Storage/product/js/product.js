const similar_products = $(".similar_product_slider");
similar_products.owlCarousel({
    rtl: true,
    loop: true,
    margin: 10,
    autoplay: true,
    responsiveClass: true,
    autoplayTimeout: 1400,
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
        },
        250: {
            items: 2,
        },
        650: {
            items: 4,
        },
        980: {
            items: 4,
        },
    },
    navText: ["<i class='bi bi-chevron-right display-4 fw-bold mt-3 '></i>", "<i class='bi bi-chevron-left display-4 fw-bold mt-3 '></i>"]

});