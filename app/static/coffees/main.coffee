$ ->
    position = $("#switch")
    if $(document).scrollTop() > position.offset().top + position.height()
            $("#main-menu").addClass('fixed')
    $('.nav li a').click (e) ->
        $('html, body').animate {
            scrollTop: $($(@).attr 'href').offset().top - 82
        }, 1500
        return false

    $(document).on('scroll', ->
        if $(document).scrollTop() < position.offset().top + position.height()
            $("#main-menu").removeClass('fixed')
        else
            $("#main-menu").addClass('fixed')
    )

    if (matchMedia('all and (max-width: 678px)').matches)
        $('#main-menu').wrap("<div id='XL-burger-menu'/>")
        $('#XL-burger-menu').children().hide()
        $('#XL-burger-menu').on 'click', ->
            $(@).toggleClass('active')
            $(@).children().slideToggle()
        return
