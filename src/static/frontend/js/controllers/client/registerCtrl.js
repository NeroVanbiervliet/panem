panemApp.controller('clRegisterCtrl', function($scope, dictionary, $http, $rootScope, tokenManager) {

	// initialize dictionary
	$scope.dict =  dictionary.fillClRegister("nl");
    
    $scope.requestInProgress = false;
    
    $scope.submitForm = function() {
        if(!$scope.requestInProgress)
        {
            $scope.performRequest();
        }
    };
    
    $scope.performRequest = function() {        
        $scope.requestInProgress = true;
        $scope.requestStatus = "inProgress";
        
        var user = $scope.user;
        
        if(angular.isUndefined(user.adress))
        {
            user.adress = ""; 
        }
        
        var formData = $.param({
            json: JSON.stringify({
                firstname: user.firstName,
                lastname : user.lastName,
                email : user.email,
                adress : user.adress,
                type : "normal", // NEED removen uit endpoint requirement
                password : user.password,
                token : tokenManager.getToken()
            })
        });
        
        $http.post($rootScope.baseUrl + '/account/create/',formData)
           .then(
               function(response){ // successful request to backend
                    $scope.requestStatus = response.data; 
               }, 
               function(response){ // failed request to backend
                    $scope.requestStatus = "backenderror"; 
               }
            );
        
        $scope.requestInProgress = false;
    };
});