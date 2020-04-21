$(document).ready(function () {

    // striped tabulky kvuli markdown strankam
    $("table").addClass("ui striped celled table");

    // inicializace dropdownu
    $(".ui.dropdown").dropdown();

    // otevirani sidebaru ma mobilu
    $("#open-sidebar").click(function () {
        $(".ui.sidebar").sidebar("toggle");
    });

    // inicializace accordions
    $(".ui.accordion").accordion();

    // kazdymu linku pridat target, aby se oteviral v novem okne
    $(".content-wrapper a").each(function () {
        $(this).attr("target", "_blank");
    });
});
