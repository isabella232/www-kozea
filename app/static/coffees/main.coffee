console.log 'main js file loaded'
$ ->
    $('.nav li a').click (e) ->
        $('html, body').animate {
            scrollTop: $($(@).attr 'href').offset().top
        }, 1500
        return false
    return
