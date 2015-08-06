jQuery(document).ready(function ($) {
    var input = $('input');

    // Hide error on keypress
    input.on('keypress', function () {
        $('.has-error').hide();
    });
});
