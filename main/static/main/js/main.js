$(function() {

  // slider
  $('#top-slide').slick({
    autoplay: true,
    autoplaySpeed: 4000,
    speed: 800,
    arrows: false,
    dots: true,
  });

  // display toggle
  var selectStatus = 0;
  var buttonStatus = 'rec';

  $('[name=select-box]').change(function() {
    selectStatus = $('[name=select-box]').val();
    var target = '.select-display-' + selectStatus + '.button-display-' + buttonStatus;
    $('.display').addClass('display-none');
    $(target).removeClass('display-none');
  });

  $('#button-rec').on('click', function() {
    buttonStatus = 'rec';
    var target = '.select-display-' + selectStatus + '.button-display-' + buttonStatus;
    $('#button-new').removeClass('warning');
    $('#button-new').addClass('secondary');
    $('#button-rec').removeClass('secondary');
    $('#button-rec').addClass('warning');
    $('.display').addClass('display-none');
    $(target).removeClass('display-none');
  });

  $('#button-new').on('click', function() {
    buttonStatus = 'new';
    var target = '.select-display-' + selectStatus + '.button-display-' + buttonStatus;
    $('#button-rec').removeClass('warning');
    $('#button-rec').addClass('secondary');
    $('#button-new').removeClass('secondary');
    $('#button-new').addClass('warning');
    $('.display').addClass('display-none');
    $(target).removeClass('display-none');
  });
});
