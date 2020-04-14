// Markdownify

$("table").addClass("ui striped celled table");

// Semantic UI

$(".ui.dropdown").dropdown();

$(".navigation .menu .browse").popup({
    inline: true,
    on: "click",
    hoverable: false,
    position: "bottom left",
    delay: {
        show: 200,
        hide: 800
    }
});

$(document)
    .ready(function () {
        // fix menu when passed
        $('.masthead')
            .visibility({
                once: false,
                onBottomPassed: function () {
                    $('.fixed.menu').transition('fade in');
                },
                onBottomPassedReverse: function () {
                    $('.fixed.menu').transition('fade out');
                }
            });

        // create sidebar and attach to menu open
        $('.ui.sidebar').sidebar('attach events', '.toc.item');
    });
