console.log 'main js file loaded'
$ ->
    $('.content').onepage_scroll {
        sectionContainer: '.fullpage-item',
        easing: 'ease',
        animationTime: 1000,
        pagination: true,
        updateURL: false,
        loop: false,
        responsiveFallback: false }
    return
