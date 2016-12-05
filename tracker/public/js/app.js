angular.module('TrackerApp', [])
.factory('LocationService', function($http, $q){
	var apiUrl = "http://localhost:3000/api"
	var o = {};

	o.getCurrLocation = function(){
		var deferred = $q.defer();

		$http.get(apiUrl + '/tracker/location/data').then(function(response){
			console.log(response.data[0]);
			deferred.resolve({ status: 'SUCCESS', location: response.data[0]});
		}, function(err){
			console.log(err);
			deferred.reject({ status: 'ERROR', error: err });
		});

		return deferred.promise;
	}

	return o;
})
.controller('MainCtrl', function($scope, $interval, LocationService){
	var initializeMap = function(centerPos){
		console.log(centerPos);
		var center = new google.maps.LatLng(centerPos.coords.latitude, centerPos.coords.longitude);

		var mapProp = {
			center: center,
    		zoom:14,
    		mapTypeId:google.maps.MapTypeId.ROADMAP
		}

		$scope.map = new google.maps.Map($("#googleMap")[0], mapProp);
		$scope.locations = [];

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

	$interval(function(){
		LocationService.getCurrLocation().then(function(result){
			var lastLoc = $scope.locations[$scope.locations.length - 1];
			console.log(lastLoc);
			if($scope.locations.length == 0 || result.location.timestamp > lastLoc.timestamp){
				$scope.locations.push(result.location);
				console.log($scope.locations);
			}
		});
	}, 2000);
});