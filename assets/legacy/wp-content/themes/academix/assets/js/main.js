jQuery(document).ready( function($) {
    'use strict';
    /* Preloader JS */
    $(window).load(function() {
	    $('.preloader-wrap').fadeOut('500', function() {
            $(this).remove();
        });
	});

    //=================== Adminer add class ====================
    $('#wpadminbar').addClass('mobile');
});

jQuery(window).load(function() {
    jQuery('.mobile-menu').meanmenu();
});