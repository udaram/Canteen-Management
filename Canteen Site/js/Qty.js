$(document).ready(function () {
    $('.dropdown-toggle').dropdown();
});

$(".dropdown-menu li a").click(function () {
    var item = $(this).text();   
    var current_row = $(this).parent();
    var current_btn = $(current_row).find(".btn:first-child");

 console.log($(current_row));     
    $(current_btn).text(item);
    $(current_btn).val(item);

 
});