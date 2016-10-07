panemApp.controller('clFinalisePaymentCtrl', function($scope, dictionary, GETUrl, $http, $rootScope, tokenManager) {
    
    // variables
    $scope.status = "loading"; 
    
    // obtain parameters from url
    $scope.getParams = GETUrl.decipher(); 
    
    // analyse adyen data
    switch($scope.getParams.authResult) {
        case "CANCELLED":
            $scope.status = "cancelled";
            break;
        case "REFUSED":
            $scope.status = "refused";
            break;
        case "PENDING": 
            $scope.status = "pending";
            break;
        case "ERROR":
            $scope.status = "adyenerror";
            break;
        default:
            // AUTHORISED is also default, further checking in backend is needed
            $scope.status = "loading";
    }
    
    // add login token to getParams
    tokenManager.getToken().then(function(newToken) {
        $scope.getParams['token'] = newToken; 
        
        // pass data on to endpoint for further analysis
        var requestData = $.param({
            json: JSON.stringify($scope.getParams)
        });

        // store order in backend
        // NEED iets mee doen als het fout gaat
        $http.post($rootScope.baseUrl + '/order/current/receipt/',requestData)
           .then(
               function(response){ // successful request to backend
                    $scope.status = response.data; 
               }, 
               function(response){ // failed request to backend
                    $scope.status = "backenderror"; 
               }
            ); 
    });
}); 