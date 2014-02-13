$ ->
    position = $("#switch")
    lock = false


    $('.closeModal').click ->
        modalid = "#" + $(@).closest('.modal').attr('id')
        $(modalid).modal('hide')
        return

    themelist = ("#theme"+i for i in [0..$('.modal').length])
    init_address_history = ->
        is_intern = false
        State = History.getState()
        $(window).hashchange (e) ->
            hash = History.getHash()
            if hash and hash != '/'
                $('a[href=#'+hash+']').eq(0).click()
            else
                slider.goToSlide(0)
                unlock_scroll()
                scrollTo(0)
            return
        $('a').click (e) ->
            e.preventDefault()
            if e.originalEvent
                href = $(@).attr('href')
                History.pushState null, null, href
            return
        return

    init_responsive_menu = ->
        if $(document).scrollTop() > position.offset().top + position.height()
                $("#main-menu").addClass('fixed')
        $('.nav li a').click (e) ->
            e.preventDefault()
            href = $(@).attr 'href'
            unlock_scroll()
            slider.goToSlide(0)
            scrollTo($(href).offset().top - 82)
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
            e.preventDefault()
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

    slider = $('.bxslider').bxSlider({
        controls: false,
        pager: false,
        adaptiveHeight: true,
        useCSS: 'webkitRequestAnimationFrame' in window,
        touchEnabled: false,
        onSlideBefore: (elem, oldindex, newindex) ->
            if newindex == 0
                scrollTo(0,0)
            return
    })
    init_responsive_menu()
    init_click_handlers()
    init_address_history()
    $(window).hashchange()

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
