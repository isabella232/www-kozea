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
    $(window).bind 'load resize', ->
        if (matchMedia('all and (max-width: 970px)').matches)
            if ($('.nav.menu').is(':visible'))
                if (!lock)
                    $('.nav.menu').hide()
                    lock = true
                    return
        else
            if ($('.nav.menu').is(':hidden'))
                $('.nav.menu').show()
            lock = false
            return

    $('#navigation-dropdown').on 'click', ->
        $('#main-header-link').hide()
        $(@).toggleClass('active')
        if ($('.nav.menu').is(':visible'))
            $('#main-header-link').hide()
            $('.nav.menu').slideUp()
        else
            $('.nav.menu').slideDown()
            $('#main-header-link').fadeIn(1000)
        return

