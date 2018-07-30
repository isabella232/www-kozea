$(document).ready(function() {
  var mymap = L.map('map').setView([45.776999, 4.859773], 15);
  L.tileLayer('https://api.mapbox.com/styles/v1/kozea/cjig50ice3m2r2smh70d2q70a/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data © <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1Ijoia296ZWEiLCJhIjoiY2ppZzRncmliMGM3MjN3bzV3dXN4dm9lNiJ9.XR70vL5oT1vDpZ3JryRZDA'
  }).addTo(mymap);
  L.marker(
    [45.776999, 4.859773],
    {'icon': L.icon({iconUrl: 'static/images/icones/map_cursor.png', iconAnchor: [20, 61]})}
  ).addTo(mymap);
});
