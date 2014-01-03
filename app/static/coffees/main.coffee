console.log 'main js file loaded'
$ ->
    $('.nav li a').click (e) ->
        $('html, body').animate {
            scrollTop: $($(@).attr 'href').offset().top
        }, 1500
        return false
    $(document).on('scroll', ->
        title = $("#header-title")
        if $(document).scrollTop() < title.offset().top + title.height()
            $("#main-header").removeClass('fixed')
        else
            $("#main-header").addClass('fixed')
    )
    return
