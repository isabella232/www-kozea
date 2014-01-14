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

    $(window).bind 'load resize', ->
        $('#navigation-dropdown').on 'click', ->
            $(@).toggleClass('active')
            $('#main-menu').slideToggle()
        return
