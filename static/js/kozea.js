
$(document).ready(function() {

    var map;
    var marker;
    if (typeof google === 'object' && typeof google.maps === 'object') {
        $.getJSON('static/map_kozeagroup', function(data) {
            var myLatLng = {lat: 45.776999, lng: 4.859773};
            var mapOptions = {
                center: myLatLng,
                styles: data,
                zoom: 16
            };
            var markerOptions = {
                position: myLatLng,
                icon: 'static/images/icones/map_cursor.png',
                origin: new google.maps.Point(0, 0),
                animation: google.maps.Animation.DROP,
                title: 'Kozea'
            };
            map.setOptions(mapOptions);
            marker.setOptions(markerOptions);
        });
    }


    $(window).scroll(function() {
		if ($(this).scrollTop() > 500) {
			$('#back-to-top').fadeIn(400);
		} else {
			$('#back-to-top').fadeOut(400);
		}
	});

	$('#back-to-top').on('click', function() {
		$('html, body').animate({scrollTop : 0}, 900);
	});

    $('#go-to-about').on('click', function() {
        $('html, body').animate({scrollTop : $($.attr(this, 'href')).offset().top}, 900);
    });

    if ($('#map').size() > 0) {
        map = new google.maps.Map($('#map').get(0));
        marker = new google.maps.Marker();
        marker.setMap(map);

    }

});
