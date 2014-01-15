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

    lock = false
    $(window).bind 'load, resize', ->
        if (!matchMedia('all and (max-width: 970px)').matches)
            if ($('#main-menu').is(':hidden'))
                $('#main-menu').show()
            lock = false
            return
        else
            if ($('#main-menu').is(':visible'))
                if (!lock)
                    $('#main-menu').hide()
                    lock = true
                    return

    $('#navigation-dropdown').on 'click', ->
        $(@).toggleClass('active')
        $('#main-menu').slideToggle()
    return
