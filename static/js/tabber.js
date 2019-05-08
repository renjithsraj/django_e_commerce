( function( $ ) {

	'use strict';

	$.fn.byaparTabber = function() {

		return this.each(function( k, v ) {
			var firstTab = jQuery(this, v).find('li.active');
			var firstTabCarousel = $(firstTab).data('carousel');
			$( '#' + firstTabCarousel).find('.section-carousel-enabled').slick();

			$(this).easytabs({
				animate: false,
				updateHash: false
			}).bind('easytabs:after',function(event){
				var current_target = event.currentTarget;
				var active_tab = $(current_target).find('li.active');
				var carousel = $(active_tab).data('carousel');
				if ( ! ( $( '#' + carousel ) ).find('.section-carousel-enabled').hasClass('slick-initialized') ) {
					$( '#' + carousel ).find('.section-carousel-enabled').slick();
				}
			});

		});

	};

	$( document ).ready(function( $ ) {
		$( '.products-tab-container' ).byaparTabber();
	});

} )( jQuery );
