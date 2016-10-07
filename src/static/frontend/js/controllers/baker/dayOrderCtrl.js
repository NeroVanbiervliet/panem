panemApp.controller('bkDayOrderCtrl', function($scope, $rootScope, dictionary, $location, $window, $http, tokenManager, GETUrl, processDate) {

    // variables
    $scope.pyOrder; 
    
    // contants
    var ONE_DAY_MILLISECONDS = 24 * 60 * 60 * 1000; 
    var TOMORROW_DATE = new Date(new Date().getTime() + ONE_DAY_MILLISECONDS);
    
	// Initialize dictionary
	$scope.dict =  dictionary.fillBkDayOrder("nl");
    
    
    // obtain parameters from url
    var GET = GETUrl.decipher(); 
    
    // GET pyDayOrders data when token is available
    tokenManager.getToken().then(function(newToken) {
        $http({
            method : "GET",
            url : $rootScope.baseUrl + "/bakery/"+GET.bakeryId+"/dayOrder/date=" + GET.date + "&token=" + newToken + "/"
        }).then(function(response) {
            $scope.pyOrder = response.data;

            // qualitative date
            processDate.setLang("nl");
            $scope.pyOrder.dateString = processDate.getWordDate($scope.pyOrder.date, true);

        }, function(response) {
            $scope.pyOrder = []; // NEED niet zeker dat dit werkt
        });
    }); 
    
    // print page
    $scope.printPage = function() {
        $window.print(); 
    };
    
    // check if remarks not empty string
    $scope.remarksNotEmpty = function(order) {
        return (order.remarks != "") && (order.remarks != null);
    };
});