panemApp.controller('clConfirmRegisterCtrl', function($scope, $rootScope, dictionary, $http, $location, tokenManager, GETUrl) {
    
    // NEED rename heel dit boeltje naar verifyAccount
    
    // VARIABLES
    $scope.GET; 
    
    // initialize dictionary
	$scope.dict =  dictionary.fillClConfirmRegister("nl");
    
    // obtain variables from url
    GET = GETUrl.decipher(); 
    var code = GET.code; 
    var email = GET.email; 
    
    // try to confirm account in backend
    tokenManager.getToken().then(function(newToken) {
        $http({
            method : "GET",
            url : $rootScope.baseUrl + "/account/verify/code=" + code + "&email=" + email + "&token=" + newToken
        }).then(function(response) {
            $scope.confirmStatus = response.data;
        }, function(response) {
            $scope.confirmStatus = "backenderror"; 
        });
    }); 
});