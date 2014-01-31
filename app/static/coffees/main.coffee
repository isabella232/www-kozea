$ ->
    $('a').click () ->
        $.address.value($(@).attr('href'))
    $.address.change (e) ->
        if e.value == '/#' or e.value == '/'
            slider.goToSlide(0)
            unlock_scroll()
            $('html, body').animate {
                scrollTop: 0
            }, 500
        $('[href='+e.value.replace('/', '')+']').trigger('click')

    position = $("#switch")
    if $(document).scrollTop() > position.offset().top + position.height()
            $("#main-menu").addClass('fixed')
    $('.nav li a').click (e) ->
        slider.goToSlide(0)
        unlock_scroll()
        prevent_flickering()
        $('html, body').animate {
            scrollTop: $($(@).attr 'href').offset().top - 82
        }, 500, () ->
            restore_mousewheel()
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

    slider = $('.bxslider').bxSlider({
        controls: false,
        pager: false,
        adaptiveHeight: true,
        useCSS: true
    })

    $("#main-header-link-icon").click (e) ->
        e.preventDefault()
        slider.goToSlide(0)

    $('#web .more').click (e) ->
        e.preventDefault()
        lock_scroll()
        slider.goToSlide($(@).data('slide'))
        return
    $('.backToFirstSlide').click (e) ->
        e.preventDefault()
        slider.goToSlide(0)
        unlock_scroll()
        return
    return

lock_scroll = ->
    prevent_flickering()
    $('html, body').animate {
        scrollTop: $($('.nav li a').eq(1).attr 'href').offset().top - 82
    }, 500, () ->
        restore_mousewheel()
    $('body').addClass('stop-scrolling')

unlock_scroll = ->
    prevent_flickering()
    $('html, body').animate {
        scrollTop: $($('.nav li a').eq(1).attr 'href').offset().top - 82
    }, 500 , () ->
        restore_mousewheel()
    $('body').removeClass('stop-scrolling')

prevent_flickering = () ->
    $('body').on('mousewheel', (e) ->
        e.preventDefault()
        return
    )
restore_mousewheel = () ->
    $('body').off('mousewheel')
    return
