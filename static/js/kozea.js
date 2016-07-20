$(document).ready(function() {

  $(window).scroll(function() {
    if ($(this).scrollTop() > 500) {
      $('#back-to-top').fadeIn(400);
    } else {
      $('#back-to-top').fadeOut(400);
    }
  });

  $('#back-to-top').on('click', function() {
    $('html, body').animate({scrollTop : 0}, 900);
  });

  $('#go-to-about').on('click', function() {
    $('html, body').animate({scrollTop : $($.attr(this, 'href')).offset().top}, 900);
  });

  $('form').on('submit', function(e) {
    e.preventDefault();
    $.post($(e.target).attr('action'), $(e.target).serialize())
      .done(function() {
        $('form input:first').before('<p class="message">Votre message a été envoyé.</p>');
        function remove_message() {
          $('.message').fadeOut(400);
        }
        setTimeout(remove_message, 2000);
      });
  });
  window.sr = new scrollReveal();

  /* Window size stuff for burger menu */
  $(window).on('resize', function() {
    $size = window.innerWidth / parseFloat($('body').css('font-size'));
    if ($size < 46) {
      $('nav').addClass('collapsible');
      if ($('.clicked').size()) { $('.menu').css('display', 'block'); }
      else { $('.menu').css('display', 'none'); }
      if (!$('.collapsible-icon').size()) {
        $('nav').prepend('<span class="collapsible-icon"></span>');
        $('.collapsible-icon').click(function() {
          $(this).toggleClass('clicked');
          if ($('.menu').is(':visible')) { $('.menu').slideUp(); }
          else {
            $('.menu').slideDown();
            $('.menu').css('display', 'block');
          }
        })
      }
    }
    else {
      $('nav').removeClass('collapsible');
      $('.menu').css('display', 'flex');
      $('.collapsible-icon').remove();
    }
  })
  $(window).trigger('resize')
});

/* Use this for the popup on the index page
var $popup = $('<div class="popup">').append('<p>Message envoyé.</p>')
$('body').append($popup, $('<div class="black-overlay">'));

function remove_popup() {
  $popup.fadeOut(400, function() {
    $(".popup, .black-overlay").remove();
  });
}*/
