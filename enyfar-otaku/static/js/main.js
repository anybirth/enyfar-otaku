$(function() {
  $('#hamburger').on('click', function() {
    $('#hamburger').hide();
    $('#cross').fadeIn();
    $('#drawer').animate({height: 'toggle'});
    return false;
  });
  $('#cross').on('click', function() {
    $('#cross').hide();
    $('#hamburger').fadeIn();
    $('#drawer').animate({height: 'toggle'});
    return false;
  });
});
