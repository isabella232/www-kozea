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
});
