$(document).ready(function () {

    // Markdownify
    $("table").addClass("ui striped celled table");

    // Semantic UI
    $(".ui.dropdown").dropdown();
    $("#open-sidebar").click(function () {
        $(".ui.sidebar").sidebar("toggle");
    });

    // $(".ui.dropdown").dropdown({
    //     allowCategorySelection: true,
    //     transition: "fade up",
    //     context: 'sidebar',
    //     on: "hover"
    //   });

    // $('.ui.accordion').accordion('behavior', 'duration', 0);

      $('.ui.accordion').accordion();


});
