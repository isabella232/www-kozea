console.log 'main js file loaded'
$ ->
    $('.nav li a').click (e) ->
        $('html, body').animate {
            scrollTop: $($(@).attr 'href').offset().top
        }, 1500
        return false
    $(document).on('scroll', ->
        console.log $(document).scrollTop()
        console.log $('#banner').offset().top
        if $(document).scrollTop() < $("#banner").offset().top
            $("#main-menu").removeClass('fixed')
        else
            $("#main-menu").addClass('fixed')
    )
    return
