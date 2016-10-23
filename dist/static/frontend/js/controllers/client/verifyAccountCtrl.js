panemApp.controller('clVerifyAccountCtrl', function($scope, $rootScope, dictionary, requestWrapper, $location, tokenManager, GETUrl) {
    
    // VARIABLES
    $scope.GET; 
    $scope.requestStatus; 
    
    // initialize dictionary
	$scope.dict =  dictionary.fillClVerifyAccount("nl");
        
    // obtain variables from url
    GET = GETUrl.decipher(); 
    
    // try to confirm account in backend    
    url = '/account/verify/';
    dataToSend = {
        code: GET.code,
        email : GET.email
    };
    $scope.requestStatus = requestWrapper.init(); 
    requestWrapper.post(url, dataToSend).then(function (newStatus) {
        $scope.requestStatus = newStatus; 
    });
});