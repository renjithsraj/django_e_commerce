	jQuery(document).ready(function($) {
		  jQuery("#red" ).on('click', function(){
			  jQuery("#color" ).attr("href", "default/colors/red.css");
			  return false;
		  });
		jQuery("#cyan" ).on('click', function(){
			  jQuery("#color" ).attr("href", "css/colors/cyan.css");
			  return false;
		  });

		  jQuery("#blue" ).on('click', function(){
			  jQuery("#color" ).attr("href", "css/colors/blue.css");
			  return false;
		  });
		  jQuery("#sky-blue" ).on('click', function(){
			  jQuery("#color" ).attr("href", "css/colors/sky-blue.css");
			  return false;
		  });

		  jQuery("#dark-blue" ).on('click', function(){
			  jQuery("#color" ).attr("href", "css/colors/dark-blue.css");
			  return false;
		  });

		  jQuery("#dark-green" ).on('click', function(){
			  jQuery("#color" ).attr("href", "css/colors/dark-green.css");

			  return false;
		  });
		  jQuery("#lite-green" ).on('click', function(){
			  jQuery("#color" ).attr("href", "css/colors/lite-green.css");

			  return false;
		  });


		  jQuery("#orange" ).on('click', function(){
			  jQuery("#color" ).attr("href", "css/colors/orange.css");
			  return false;
		  });

		  jQuery("#brown" ).on('click', function(){
			  jQuery("#color" ).attr("href", "css/colors/brown.css");
			  return false;
		  });


		  jQuery("#purple" ).on('click', function(){
			  jQuery("#color" ).attr("href", "css/colors/purple.css");
			  return false;
		  });

		    jQuery("#dark-purple" ).on('click', function(){
			  jQuery("#color" ).attr("href", "css/colors/dark-purple.css");
			  return false;
		  });

		jQuery("#pink" ).on('click', function(){
			  jQuery("#color" ).attr("href", "css/colors/pink.css");
			  return false;
		  });




		  // picker buttton
		  jQuery(".picker_close").on('click', function(){

			  	jQuery("#choose_color").toggleClass("position");

		   });
		  jQuery("#default" ).on('click', function(){
			  jQuery("#color" ).attr("href", "css/colors/sky-default.css");
			  jQuery(".logo img" ).attr("src", "images/logo.png");
			  return false;
		  });

		   //header

			//stickey header
			jQuery(window).scroll(function() {
				var scroll = jQuery(window).scrollTop();
				if (scroll >= 40) {
					jQuery(".fixed-header").addClass("small-header");
				}
				else {
					jQuery(".fixed-header").removeClass("small-header");
				}
			});



	});
