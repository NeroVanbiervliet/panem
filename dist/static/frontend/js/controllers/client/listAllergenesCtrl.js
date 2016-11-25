panemApp.controller('clListAllergenesCtrl', function($scope, dictionary, GETUrl) {

	// initialize dictionary
	$scope.dict =  dictionary.fillClListAllergenes("nl");

	// obtain parameters from url
    var GET = GETUrl.decipher();
});
