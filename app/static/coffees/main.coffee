console.log 'main js file loaded'
$ ->
    $('.nav li a').click (e) ->
        $('html, body').animate {
            scrollTop: $($(@).attr 'href').offset().top
        }, 1500
        return false
    $("#main-menu").on('activate.bs.scrollspy', (e) ->
        console.log($(e.target).children('a').attr('href'))
        if $(e.target).children('a').attr('href') != "#web"
            $(@).addClass('fixed')
        else
            $(@).removeClass('fixed')
        return
        )
    return
