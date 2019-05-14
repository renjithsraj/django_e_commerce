(function($) {
    "use strict";
    
    /*-------------------------------------
     jQuery MeanMenu activation code
     --------------------------------------*/
    $('nav#dropdown').meanmenu({ siteLogo: "<a href='index.html' class='logo-mobile-menu'><img src='img/logo.png' /></a>" });

    /*-------------------------------------
     Home page 4 Category Menu
     -------------------------------------*/
    $('#menu-content').on('click', 'li.has-sub-menu > a', function(e) {
        e.preventDefault();
    });

    /*-------------------------------------
     wow js active
     -------------------------------------*/
    new WOW().init();

    /*-------------------------------------
     jquery Scollup activation code
     -------------------------------------*/
    $.scrollUp({
        scrollText: '<i class="fa fa-angle-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    });


    /*-------------------------------------
     Carousel slider initiation
     -------------------------------------*/
    $('.metro-carousel').each(function() {
        var carousel = $(this),
            loop = carousel.data('loop'),
            items = carousel.data('items'),
            margin = carousel.data('margin'),
            stagePadding = carousel.data('stage-padding'),
            autoplay = carousel.data('autoplay'),
            autoplayTimeout = carousel.data('autoplay-timeout'),
            smartSpeed = carousel.data('smart-speed'),
            dots = carousel.data('dots'),
            nav = carousel.data('nav'),
            navSpeed = carousel.data('nav-speed'),
            rXsmall = carousel.data('r-x-small'),
            rXsmallNav = carousel.data('r-x-small-nav'),
            rXsmallDots = carousel.data('r-x-small-dots'),
            rXmedium = carousel.data('r-x-medium'),
            rXmediumNav = carousel.data('r-x-medium-nav'),
            rXmediumDots = carousel.data('r-x-medium-dots'),
            rSmall = carousel.data('r-small'),
            rSmallNav = carousel.data('r-small-nav'),
            rSmallDots = carousel.data('r-small-dots'),
            rMedium = carousel.data('r-medium'),
            rMediumNav = carousel.data('r-medium-nav'),
            rMediumDots = carousel.data('r-medium-dots'),
            rLarge = carousel.data('r-large'),
            rLargeNav = carousel.data('r-large-nav'),
            rLargeDots = carousel.data('r-large-dots'),
            center = carousel.data('center');

        carousel.owlCarousel({
            loop: (loop ? true : false),
            items: (items ? items : 4),
            lazyLoad: true,
            margin: (margin ? margin : 0),
            autoplay: (autoplay ? true : false),
            autoplayTimeout: (autoplayTimeout ? autoplayTimeout : 1000),
            smartSpeed: (smartSpeed ? smartSpeed : 250),
            dots: (dots ? true : false),
            nav: (nav ? true : false),
            navText: ["<i class='fa fa-angle-left' aria-hidden='true'></i>", "<i class='fa fa-angle-right' aria-hidden='true'></i>"],
            navSpeed: (navSpeed ? true : false),
            center: (center ? true : false),
            responsiveClass: true,
            responsive: {
                0: {
                    items: (rXsmall ? rXsmall : 1),
                    nav: (rXsmallNav ? true : false),
                    dots: (rXsmallDots ? true : false)
                },
                480: {
                    items: (rXmedium ? rXmedium : 2),
                    nav: (rXmediumNav ? true : false),
                    dots: (rXmediumDots ? true : false)
                },
                768: {
                    items: (rSmall ? rSmall : 3),
                    nav: (rSmallNav ? true : false),
                    dots: (rSmallDots ? true : false)
                },
                992: {
                    items: (rMedium ? rMedium : 5),
                    nav: (rMediumNav ? true : false),
                    dots: (rMediumDots ? true : false)
                },
                1199: {
                    items: (rLarge ? rLarge : 6),
                    nav: (rLargeNav ? true : false),
                    dots: (rLargeDots ? true : false)
                }
            }
        });

    });



    /*-------------------------------------
     Countdown activation code
     -------------------------------------*/
    $('#countdown').countdown('2018/01/01', function(e) {
        $(this).html(e.strftime("<div class='countdown-section'><h3>%-d</h3> <p>day%!d</p> </div><div class='countdown-section'><h3>%H</h3> <p>Hour%!H</p> </div><div class='countdown-section'><h3>%M</h3> <p>Min%!M</p> </div><div class='countdown-section'><h3>%S</h3> <p>Sec%!S</p> </div>"));
    });

    /*-------------------------------------
     Jquery Serch Box
     -------------------------------------*/
    $(document).on('click', '#top-search-form a.search-button', function(e) {
        e.preventDefault();

        var targrt = $(this).prev('input.search-input');
        targrt.animate({
            width: ["toggle", "swing"],
            height: ["toggle", "swing"],
            opacity: "toggle"
        }, 500, "linear");

        return false;

    });

    /*-------------------------------------
     Contact Form activation code
     -------------------------------------*/
    if ($('#contact-form').length) {
        $('#contact-form').validator().on('submit', function(e) {
            var $this = $(this),
                $target = $('.form-response');
            if (e.isDefaultPrevented()) {
                $target.html("<div class='alert alert-success'><p>Please select all required field.</p></div>");
            } else {
                var name = $('#form-name').val();
                var email = $('#form-email').val();
                var message = $('#form-message').val();
                // ajax call
                $.ajax({
                    url: "php/form-process.php",
                    type: "POST",
                    data: "name=" + name + "&email=" + email + "&message=" + message,
                    beforeSend: function() {
                        $target.html("<div class='alert alert-info'><p>Loading ...</p></div>");
                    },
                    success: function(text) {
                        if (text == 'success') {
                            $this[0].reset();
                            $target.html("<div class='alert alert-success'><p>Message has been sent successfully.</p></div>");
                        } else {
                            $target.html("<div class='alert alert-success'><p>" + text + "</p></div>");
                        }
                    }
                });
                return false;
            }
        });
    }


    /*-------------------------------------
     Input Quantity Up & Down activation code
     -------------------------------------*/
    $('#quantity-holder,#quantity-holder2').on('click', '.quantity-plus', function() {

        var $holder = $(this).parents('.quantity-holder');
        var $target = $holder.find('input.quantity-input');
        var $quantity = parseInt($target.val(), 10);
        if ($.isNumeric($quantity) && $quantity > 0) {
            $quantity = $quantity + 1;
            $target.val($quantity);
        } else {
            $target.val($quantity);
        }

    }).on('click', '.quantity-minus', function() {

        var $holder = $(this).parents('.quantity-holder');
        var $target = $holder.find('input.quantity-input');
        var $quantity = parseInt($target.val(), 10);
        if ($.isNumeric($quantity) && $quantity >= 2) {
            $quantity = $quantity - 1;
            $target.val($quantity);
        } else {
            $target.val(1);
        }

    });

    /*-------------------------------------
     Select2 activation code
     -------------------------------------*/
    if ($('#checkout-form select.select2').length) {
        $('#checkout-form select.select2').select2({
            theme: 'classic',
            dropdownAutoWidth: true,
            width: '100%'
        });
    }

    /*-------------------------------------
     Sidebar Menu activation code
     -------------------------------------*/
    $('#additional-menu-area').on('click', 'span.side-menu-trigger', function() {

        var $this = $(this);
        if ($this.hasClass('open')) {
            document.getElementById('mySidenav').style.width = '0';
            $this.removeClass('open').find('i.fa').removeClass('fa-times').addClass('fa-bars');
        } else {
            $this.addClass('open').find('i.fa').removeClass('fa-bars').addClass('fa-times');
            document.getElementById('mySidenav').style.width = '280px';
        }

    });

    $('#mySidenav').on('click', '.closebtn', function(e) {
        e.preventDefault();
        document.getElementById('mySidenav').style.width = '0';
        $('#additional-menu-area span.side-menu-trigger').removeClass('open').find('i.fa').removeClass('fa-times').addClass('fa-bars');

    });

    /*-------------------------------------
     Category menu selecting
     -------------------------------------*/
    $('#adv-search .sidenav-nav li').on('click', 'a', function() {
        var $this = $(this),
            target = $this.parents('div.dropdown').children('button').children('span');
        target.text($this.text());
    });


    /*-------------------------------------
     Shop category submenu positioning
     -------------------------------------*/
    $('#category-menu-area,#category-menu-area-top').on("mouseenter", "ul > li", function() {
        var self = $(this),
            target = self.find('ul.dropdown-menu'),
            targetUlW = target.outerWidth(),
            parentHolder = self.parents('.category-menu-area'),
            w = $(window).width() - (parentHolder.offset().left + parentHolder.width());
        if (targetUlW > w) {
            target.css({
                'top': 0,
                'left': '-' + targetUlW + 'px'
            });
        }
    }).on("mouseleave", "ul li > a", function() {
        var self = $(this),
            target = self.find('ul.dropdown-menu');
        target.css({
            'top': '',
            'left': ''
        });
    });

    /*-------------------------------------
     Auto height for product listing
     -------------------------------------*/
    function equalHeight() {
        $('.products-container').each(function() {
            var mHeight = 0;
            $(this).children('div').children('div').height('auto');
            $(this).children('div').each(function() {
                var itemHeight = $(this).actual('height');
                if (itemHeight > mHeight) {
                    mHeight = itemHeight;
                }
                $(this).children('div').height(mHeight + 'px');
            });
        });
    }

    /*-------------------------------------
     Window load function
     -------------------------------------*/
    $(window).on('load', function() {
        // Page Preloader
        $('#preloader').fadeOut('slow', function() {
            $(this).remove();
        });

        //jQuery for Isotope initialization
        var $container = $('#home-isotope');
        if ($container.length > 0) {
            var $isotope = $container.find('.featuredContainer').isotope({
                filter: '*',
                animationOptions: {
                    duration: 750,
                    easing: 'linear',
                    queue: false
                }
            });

            $container.find('.isotop-classes-tab').on('click', 'a', function() {
                var $this = $(this);
                $this.parent('.isotop-classes-tab').find('a').removeClass('current');
                $this.addClass('current');
                var selector = $this.attr('data-filter');
                $isotope.isotope({
                    filter: selector,
                    animationOptions: {
                        duration: 750,
                        easing: 'linear',
                        queue: false
                    }
                });
                return false;
            });
        }
    }); // end window load function

    /*-------------------------------------
     Call the load and resized function
     -------------------------------------*/
    $(window).on('load resize', function() {
        equalHeight(); // Call Equal height function
        //Define the maximum height for mobile menu
        var wHeight = $(window).height(),
            mLogoH = $('a.logo-mobile-menu').outerHeight();
        wHeight = wHeight - 50;
        $('.mean-nav > ul').css('height', wHeight + 'px');
    });

    /*-------------------------------------
     window scroll function
     -------------------------------------*/
    $(window).on('scroll', function() {
        //jquery Stiky Menu activation code
        var s = $('#sticker'),
            w = $('.wrapper-area'),
            target = s.find('.header-bottom'),
            windowpos = $(window).scrollTop(),
            windowWidth = $(window).width();

        if (windowWidth > 767) {
            var topBar = s.find('.header-top'),
                topBarH = 0;
            if (topBar.length) {
                topBarH = topBar.outerHeight();
            }

            if (windowpos >= topBarH) {
                s.addClass('stick');
                var h = target.outerHeight();
                w.css('padding-top', h + 'px');
            } else {
                s.removeClass('stick');
                w.css('padding-top', 0);
            }
        }
    }); // end of scrool function

    /*-------------------------------------
     Google Map activation code
     -------------------------------------*/
    if ($('#googleMap').length) {
        var initialize = function() {
            var mapOptions = {
                zoom: 15,
                scrollwheel: false,
                center: new google.maps.LatLng(-37.81618, 144.95692)
            };
            var map = new google.maps.Map(document.getElementById("googleMap"), mapOptions);
            var marker = new google.maps.Marker({
                position: map.getCenter(),
                animation: google.maps.Animation.BOUNCE,
                icon: 'img/map-marker.png',
                map: map
            });
        }
        google.maps.event.addDomListener(window, 'load', initialize);
    }


       
        var priceSlider = document.getElementById('price-range-filter');
        if (priceSlider) {
            noUiSlider.create(priceSlider, {
                start: [20, 80],
                connect: true,
                /*tooltips: true,*/
                range: {
                    'min': 0,
                    'max': 100
                },
                format: wNumb({
                    decimals: 0
                }),
            });
            var marginMin = document.getElementById('price-range-min'),
                marginMax = document.getElementById('price-range-max');
            priceSlider.noUiSlider.on('update', function(values, handle) {
                if (handle) {
                    marginMax.innerHTML = "$" + values[handle];
                } else {
                    marginMin.innerHTML = "$" + values[handle];
                }
            });
        }
    

})(jQuery);
