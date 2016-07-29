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

  $('.contact-form').on('submit', function(e) {
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
      else { $('.menu').hide(); }
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

  /* Newsletter  */
  $('#newsletter a').click(function() {
    if ($('.popup').size() === 0) {
      $popup = $('<div class="hidden popup">')
      $popup.append($('<span class="close-popup">')).append(
        $('<p class="sent hidden">').html(
        'Vous avez été ajouté à la liste dʼenvoi de la newsletter'))
      $popup.append($("<div>").append($('<p>').html(
        'Entrez votre adresse mail pour recevoir la newsletter</p>')).append(
        $('<form class="newsletter-form" method="POST">').attr(
          "action", "/send_mail/newsletter").append(
          $('<input type="email" placeholder="[ Email ]" required />').attr(
            "name", "email")
          ).append($('<input type ="submit" value="Valider"/>'))))
      $('#news').append($popup)
    }

    $(window).keyup(function(e) {
      if (e.keyCode === 27) {
        remove_popup();
        $('body > :not(.popup)').off('click');
      }
    });
    $('.close-popup').click(function() {
      remove_popup();
      $('body > :not(.popup)').off('click');
    });

    $('.popup').slideDown(function() {
      $('body').click(function(e) {
        if (!$(e.target).parents('div').is('.popup')) {
          remove_popup();
          $('body').off('click');
        }
      });
    });

    $form = $('.newsletter-form')
    $form.on('submit', function(e) {
      e.preventDefault();
      $.post($form.attr('action'), $form.serialize()).done(function() {
        $('.popup div').slideUp(400, function() {
          $('.popup .hidden').slideDown();
          setTimeout(remove_popup, 2000);
        });
      });
    });
  });

  function remove_popup() {
    $('.popup').fadeOut(400, function() {
      $('.popup .sent').hide();
      $('.popup div').show();
      $(window).off('keyup');
    });
  };
});
