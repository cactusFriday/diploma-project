$(function () {
    $(window).on('scroll', function () {
        if ( $(window).scrollTop() > 10 ) {
            $('.navbar-ws').addClass('active');
        } else {
            $('.navbar-ws').removeClass('active');
        }
    });
});