$(function() {
  $('#dummy').css('height', 99999);
  $('#hamburger').on('click', function() {
    $('#hamburger').hide();
    $('#cross').fadeIn();
    $('#dummy').fadeIn();
    $('#drawer').animate({height: 'toggle'});
    return false;
  });
  $('#cross').on('click', function() {
    $('#cross').hide();
    $('#hamburger').fadeIn();
    $('#dummy').fadeOut();
    $('#drawer').animate({height: 'toggle'});
    return false;
  });
});
