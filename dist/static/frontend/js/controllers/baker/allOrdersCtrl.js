panemApp.controller('bkAllOrdersCtrl', function($scope, $rootScope, dictionary, $window, requestWrapper, tokenManager, $location, GETUrl, processDate) {

    // define variables
    $scope.pyDayOrders;

	// Initialize dictionary
	$scope.dict = dictionary.fillBkAllOrders("nl");

    // contants
    var ONE_DAY_MILLISECONDS = 24 * 60 * 60 * 1000;

    // date of today
    var todayMs = (new Date()).getTime();

    // date of two weeks ago
    var oneWeekAgoMs = todayMs - 7*ONE_DAY_MILLISECONDS;
    var oneWeekFutureMS = todayMs + 7*ONE_DAY_MILLISECONDS;

    // obtain parameters from url
    var GET = GETUrl.decipher();

    // initialise processDate
    processDate.setLang("nl");
    $scope.getQualitativeDate = processDate.getWordDate;

    // GET pyDayOrders data when token is available
    var url = '/bakery/' + GET.bakeryId + '/allDayOrders/firstDay=' + oneWeekFutureMS + '&lastDay=' + oneWeekAgoMs;
    $scope.requestStatus = requestWrapper.init();
    requestWrapper.get(url).then(function ([newStatus,resultData]) {
        $scope.requestStatus = newStatus;
        $scope.pyDayOrders = resultData;
    });


    $scope.navigateToDayOrder = function(date) {
        $window.location.href = "#/baker/dayorder?bakeryId="+GET.bakeryId+"&date="+date;
    };
});
