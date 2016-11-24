panemApp.controller('clRegisterCtrl', function($scope, dictionary, $http, $rootScope, tokenManager, $window) {

	// initialize dictionary
	$scope.dict =  dictionary.fillClRegister("nl");

    $scope.performRequest = function() {
        $scope.requestStatus = "working";

        var user = $scope.user;

        if(angular.isUndefined(user.adress))
        {
            user.adress = "";
        }

        tokenManager.getToken().then(function(newToken) {
            var formData = $.param({
            json: JSON.stringify({
                    firstname: user.firstName,
                    lastname : user.lastName,
                    email : user.email,
                    adress : user.adress,
                    type : "normal", // NEED removen uit endpoint requirement
                    password : user.password,
                    token : newToken
                })
            });

            $http.post($rootScope.baseUrl + '/account/create/',formData)
               .then(
                   function(response){ // successful request to backend
                        $scope.requestStatus = response.data;
                        // show alert bar and redirect to home
                        if (response.data == 'success') {
                            $rootScope.feedbackMessage = $scope.dict.requestStatus.success + ' ' + user.email;
                    		$rootScope.showFeedbackMessage = true;
                            $window.location.href = '#/client/home';
                        }
                   },
                   function(response){ // failed request to backend
                        $scope.requestStatus = "backenderror";
                   }
                );
        });
    };
});
