angular.module('TrackerApp', [])
.factory('LocationService', function($http){
	var o = {};

	o.getLocations = function(){
		return {};
	}

	return o;
})
.controller('MainCtrl', function($scope, LocationService){
	var initializeMap = function(centerPos){
		console.log(centerPos);
		var center = new google.maps.LatLng(centerPos.coords.latitude, centerPos.coords.longitude);

		var mapProp = {
			center: center,
    		zoom:14,
    		mapTypeId:google.maps.MapTypeId.ROADMAP
		}

		$scope.map = new google.maps.Map($("#googleMap")[0], mapProp);

		var marker = new google.maps.Marker({
    		position: center,
    		map: $scope.map,
    		title: 'GZ'
  		});
	}

	var geoCenter = {
		coords: {
			latitude: 6.9344,
			longitude: 79.8428
		}
	}

	if(navigator.geolocation){
		navigator.geolocation.getCurrentPosition(initializeMap);
	}
	else{
		initializeMap(geoCenter);
	}
});