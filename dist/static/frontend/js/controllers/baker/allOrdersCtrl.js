panemApp.controller('bkAllOrdersCtrl', function($scope, $rootScope, dictionary, $window, $http, tokenManager, $location, GETUrl, processDate) {

    // define variables
    $scope.pyDayOrders; 
    
	// Initialize dictionary
	$scope.dict = dictionary.fillBkAllOrders("nl");

    // contants
    var ONE_DAY_MILLISECONDS = 24 * 60 * 60 * 1000; 
    
    // date of today
    var todayMs = (new Date()).getTime();
    
    // date of two weeks ago
    var twoWeeksAgoMs = todayMs - 14*ONE_DAY_MILLISECONDS; 
    
    // obtain parameters from url
    var GET = GETUrl.decipher(); 
    
    // initialise processDate
    processDate.setLang("nl");
    $scope.getQualitativeDate = processDate.getWordDate; 
    
    // GET pyDayOrders data when token is available
    tokenManager.getToken().then(function(newToken) {
        $http({
            method : "GET",
            url : $rootScope.baseUrl + "/bakery/"+GET.bakeryId+"/allDayOrders/firstDay=" + todayMs + "&lastDay=" + twoWeeksAgoMs + "&token=" + newToken + "/"
        }).then(function(response) {
            $scope.pyDayOrders = response.data;

        }, function(response) {
            $scope.pyDayOrders = []; // NEED niet zeker dat dit werkt
        })
    });
    
    $scope.navigateToDayOrder = function(date) {
        $window.location.href = "#/baker/dayorder?bakeryId="+GET.bakeryId+"&date="+date;
    }
});