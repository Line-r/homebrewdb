$('document').ready(function(){
  $('body').on("show.bs.collapse", ".qr-collapse", function(event){
    var title = angular.element(event.target).scope().title;
    $(event.target).qrcode({text:'https://raw.githubusercontent.com/Line-r/homebrewdb/master/v0.html' + title.name});
  });

  $('body').on("hidden.bs.collapse", ".qr-collapse", function(event){
    $(event.target).empty();
  });
});
