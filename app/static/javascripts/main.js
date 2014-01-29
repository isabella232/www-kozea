// Generated by CoffeeScript 1.6.3
var lock_scroll, prevent_flickering, restore_mousewheel, unlock_scroll;

$(function() {
  var lock, position, slider;
  position = $("#switch");
  if ($(document).scrollTop() > position.offset().top + position.height()) {
    $("#main-menu").addClass('fixed');
  }
  $('.nav li a').click(function(e) {
    prevent_flickering();
    $('html, body').animate({
      scrollTop: $($(this).attr('href')).offset().top - 82
    }, 1500, function() {
      return restore_mousewheel();
    });
    return false;
  });
  $(document).on('scroll', function() {
    if ($(document).scrollTop() < position.offset().top + position.height()) {
      return $("#main-menu").removeClass('fixed');
    } else {
      return $("#main-menu").addClass('fixed');
    }
  });
  lock = false;
  $(window).bind('load resize', function() {
    if ((matchMedia('all and (max-width: 970px)').matches)) {
      if ($('.nav.menu').is(':visible')) {
        if (!lock) {
          $('.nav.menu').hide();
          lock = true;
        }
      }
    } else {
      if ($('.nav.menu').is(':hidden')) {
        $('.nav.menu').show();
      }
      lock = false;
    }
  });
  $('#navigation-dropdown').on('click', function() {
    $('#main-header-link').hide();
    $(this).toggleClass('active');
    if ($('.nav.menu').is(':visible')) {
      $('#main-header-link').hide();
      $('.nav.menu').slideUp();
    } else {
      $('.nav.menu').slideDown();
      $('#main-header-link').fadeIn(1000);
    }
  });
  slider = $('.bxslider').bxSlider({
    controls: false,
    pager: false,
    adaptiveHeight: true
  });
  $("#main-header-link-icon").click(function(e) {
    e.preventDefault();
    return slider.goToSlide(0);
  });
  $('#web .more').click(function(e) {
    e.preventDefault();
    lock_scroll();
    slider.goToSlide($(this).data('slide'));
  });
  $('.backToFirstSlide').click(function(e) {
    e.preventDefault();
    slider.goToSlide(0);
    unlock_scroll();
  });
});

lock_scroll = function() {
  prevent_flickering();
  $('html, body').animate({
    scrollTop: $($('.nav li a').eq(1).attr('href')).offset().top - 82
  }, 1500, function() {
    return restore_mousewheel();
  });
  return $('body').addClass('stop-scrolling');
};

unlock_scroll = function() {
  prevent_flickering();
  $('html, body').animate({
    scrollTop: $($('.nav li a').eq(1).attr('href')).offset().top - 82
  }, 1500, function() {
    return restore_mousewheel();
  });
  return $('body').removeClass('stop-scrolling');
};

prevent_flickering = function() {
  return $('body').on('mousewheel', function(e) {
    e.preventDefault();
  });
};

restore_mousewheel = function() {
  $('body').off('mousewheel');
};
