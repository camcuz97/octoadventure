var map;
var service;


function initialize(location) {
  var mapOptions = {
    center: new google.maps.LatLng(location.coords.latitude, location.coords.longitude),
    zoom: 15
  }

  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  console.log(new google.maps.LatLngBounds);
  console.log(map.getBounds());

  service = new google.maps.places.PlacesService(map);

  google.maps.event.addListenerOnce(map, 'bounds_changed', getRequest);
}

function getRequest() {
  var request = {
    // bounds: map.getBounds(),
    query: 'starbucks'
  }
  service.textSearch(request, callback);
}

function callback(results, status) {
  if(status == google.maps.places.PlacesServiceStatus.OK) {
    console.log(results);
    for (var i = 0; i < results.length; i++) {
      var place = results[i];
      createMarker(results[i], results[i].name);
    }
  }
}

function createMarker(place, name) {
  console.log(name);
  var marker = new google.maps.Marker({
    map: map,
    position: place.geometry.location
  });
  var infoWindow = new google.maps.InfoWindow();
  infoWindow.setContent('<strong>' + name + '</strong>');
  google.maps.event.addListener(
    marker,
    'click',
    function() {infoWindow.open(map, marker);}
  );
}

$(document).ready(
  function() {
    navigator.geolocation.getCurrentPosition(initialize); //sends user's location to initialize()
    $("h1").click(function(){
      $(this).fadeOut(1000).delay(3000).fadeIn(1000);
  });
});

// testing jQuery

function stickIt() {

  var orgElementPos = $('.original').offset();
  orgElementTop = orgElementPos.top;

  if ($(window).scrollTop() >= (orgElementTop)) {
    // scrolled past the original position; now only show the cloned, sticky element.

    // Cloned element should always have same left position and width as original element.
    orgElement = $('.original');
    coordsOrgElement = orgElement.offset();
    leftOrgElement = coordsOrgElement.left;
    widthOrgElement = orgElement.css('width');
    $('.cloned').css('left',leftOrgElement+'px').css('top',0).css('width',widthOrgElement).show();
    $('.original').css('visibility','hidden');
  } else {
    // not scrolled past the menu; only show the original menu.
    $('.cloned').hide();
    $('.original').css('visibility','visible');
  }
}

$(document).ready(function() {
  $('.menu').addClass('original').clone().insertAfter('.menu').addClass('cloned').css('position','fixed').css('top','0').css('margin-top','0').css('z-index','500').removeClass('original').hide();
  scrollIntervalID = setInterval(stickIt, 10);
})
