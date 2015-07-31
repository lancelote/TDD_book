var input = $('input');

// Hide error on input click
input.click(function () {
    $('.has-error').hide();
});

// Hide error on keypress
input.on('keypress', function () {
    $('.has-error').hide();
});
