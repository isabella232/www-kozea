$ ->
    position = $("#switch")
    lock = false


    $('.closeModal').click ->
        modalid = "#" + $(@).closest('.modal').attr('id')
        $(modalid).modal('hide')
        return

    themelist = ("#theme"+i for i in [0..$('.modal').length])
    init_address_history = ->
        $('a').click (e) ->
            $.address.value($(@).attr('href'))
            return
        $.address.externalChange (e) ->
            if e.value.replace('/', '') in themelist
                e.value='/'
                $.address.value e.value
            if e.value.search('^\/#') is -1
                e.value = '/'
                $.address.value e.value
                slider.goToSlide(0)
                unlock_scroll()
                scrollTo(0)
                return
            $('[href='+e.value.replace('/', '')+']').trigger('click')
            return
        return

    init_responsive_menu = ->
        if $(document).scrollTop() > position.offset().top + position.height()
                $("#main-menu").addClass('fixed')
        $('.nav li a').click (e) ->
            slider.goToSlide(0)
            href = $(@).attr 'href'
            if $('body').hasClass('stop-scrolling')
                timeanimation = true
            unlock_scroll()
            if timeanimation
                setTimeout(() ->
                    scrollTo($(href).offset().top - 82)
                    return
                , 700)
            else
                    scrollTo($(href).offset().top - 82)
            timeanimation = false
            e.preventDefault()
            return
        $(document).on('scroll', ->
            if $(document).scrollTop() < position.offset().top + position.height()
                $("#main-menu").removeClass('fixed')
            else
                $("#main-menu").addClass('fixed')
            return
        )
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
        return

    init_click_handlers = ->
        $("#main-header-link-icon").click (e) ->
            e.preventDefault()
            slider.goToSlide(0)
            return
        $('#web .more').click (e) ->
            e.preventDefault()
            lock_scroll()
            scrollTo()
            slider.goToSlide($(@).data('slide'))
            return
        $('.backToFirstSlide').click (e) ->
            e.preventDefault()
            slider.goToSlide(0)
            unlock_scroll()
            return
        return

    init_address_history()
    init_responsive_menu()
    init_click_handlers()


    slider = $('.bxslider').bxSlider({
        controls: false,
        pager: false,
        adaptiveHeight: true,
        useCSS: 'webkitRequestAnimationFrame' in window
    })
    return

scrollTo = (position=null, speed=500)->
    prevent_flickering()
    if (!position and position != 0)
        position = $($('.nav li a').eq(1).attr 'href').offset().top - 82
    $('html, body').animate {
        scrollTop: position
    }, speed, () ->
        $('body').off('mousewheel')
        return
    return

lock_scroll = ->
    $('body').addClass('stop-scrolling')
    return

unlock_scroll = ->
    $('body').removeClass('stop-scrolling')
    return

prevent_flickering = () ->
    $('body').on('mousewheel', (e) ->
        e.preventDefault()
        return
    )
    return
