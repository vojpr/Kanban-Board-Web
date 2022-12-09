// Insert username into hero headline
$(".nameinput").on("input",function(){
    $("#target").html("Hello "+$(this).val());
  });
  
  // Change navbar color on scroll
  $(function () {
    $(document).scroll(function () {
      var $nav = $(".navbar-fixed-top");
      $nav.toggleClass('scrolled', $(this).scrollTop() > 20);
    });
  });