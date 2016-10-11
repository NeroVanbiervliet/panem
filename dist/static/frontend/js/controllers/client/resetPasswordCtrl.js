panemApp.controller('clResetPasswordCtrl', function($scope, dictionary, $http, tokenManager, $rootScope, GETUrl) {
    
    // initialize dictionary
	$scope.dict =  dictionary.fillClResetPassword("nl");
    
    // obtain parameters from url
    var GET = GETUrl.decipher(); 
    
    if (GET.code != null) {
        $scope.formData = {}; 
        $scope.formData.code = GET.code; 
    }
    
    // try to set new password in endpoint
    $scope.performRequest = function() {
        tokenManager.getToken().then(function(newToken) {
            var formData = $.param({
            json: JSON.stringify({
                    code : $scope.formData.code,
                    passwordNew : $scope.formData.password,
                    token : newToken
                })
            });

            $http.post($rootScope.baseUrl + '/account/password/reset/set/',formData)
               .then(
                   function(response){ // successful request to backend
                        $scope.requestStatus = response.data; 
                   }, 
                   function(response){ // failed request to backend
                        $scope.requestStatus = "backenderror"; 
                   }
                );

            $scope.requestInProgress = false; 
        });
    }
}); 