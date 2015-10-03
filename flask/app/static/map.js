// Render the markers for cab locations on Google Maps
var pinColor = "fe7569";
var pinColor2 = "69f2fe";
var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
        new google.maps.Size(21, 34),
        new google.maps.Point(0,0),
        new google.maps.Point(10, 34));
var pinImage2 = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor2,
        new google.maps.Size(21, 34),
        new google.maps.Point(0,0),
        new google.maps.Point(10, 34));
var pinShadow = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
        new google.maps.Size(40, 37),
        new google.maps.Point(0, 0),
        new google.maps.Point(12, 35));



var NYC = new google.maps.LatLng(40.7903,-73.9597);
var markers = [];
var map;
function initialize() {
    var mapOptions = {
	zoom: 12,
	center: NYC
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
			      mapOptions);
}
function update_values() {
    $.getJSON('/real/',
        function(data) {
            user_data = data.result
		  //console.log(user_data)
		    clearMarkers();
		      for (var i = 0; i < user_data.length; i = i + 1) {
                // console.log(data.result[i].status)
                if (data.result[i].status == "False") {
	               addMarker(new google.maps.LatLng(user_data[i].latitude, user_data[i].longitude), '<p>Name: '+user_data[i].name+'</p><p> Steps: '+user_data[i].steps+'</p>');
		        }else {
                    addMarker2(new google.maps.LatLng(user_data[i].latitude, user_data[i].longitude));
            } 
          }
            });
    // $.getJSON('/real2/',
    //       console.log(user_data)
    //           function(data) {
    //               user_data = data.result
    //       clearMarkers();
    //       for (var i = 0; i < user_data.length; i = i + 1) {
    //               addMarker2(new google.maps.LatLng(user_data[i].latitude, user_data[i].longitude));
    //       }
    //         });
    window.setTimeout(update_values, 5000);
}
update_values();
function drop(lat, lng) {
    point  = new google.maps.LatLng(lat,lng);
    clearMarkers();
    addMarker(point);
    addMarker2(point);
}
// function addMarker(position) {
//     markers.push(new google.maps.Marker({
// 	position: position,
// 	map: map,
// 	icon: pinImage,
// 	shadow: pinShadow
//     }));
// }
function addMarker(position,i) {
    var m = new google.maps.Marker({
    position: position,
    map: map,
    icon: pinImage,
    shadow: pinShadow
    });
    google.maps.event.addListener(m, "click", function(event) {
        var infowindow = new google.maps.InfoWindow({
            content: i.toString()
        });
        infowindow.open(map, m);
    });
    markers.push(m);
}
function addMarker2(position) {
    markers.push(new google.maps.Marker({
    position: position,
    map: map,
    icon: pinImage2,
    shadow: pinShadow
    }));
}
function clearMarkers() {
    for (var i = 0; i < markers.length; i++) {
	markers[i].setMap(null);
    }
    markers = [];
}
google.maps.event.addDomListener(window, 'load', initialize);
