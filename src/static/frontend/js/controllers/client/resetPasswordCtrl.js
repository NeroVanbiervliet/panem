panemApp.controller('clResetPasswordCtrl', function($scope, dictionary, $http, tokenManager, $rootScope, GETUrl, $window) {

    // initialize dictionary
	$scope.dict =  dictionary.fillClResetPassword("nl");

    // obtain parameters from url
    var GET = GETUrl.decipher();

    if (GET.code != null) {
        $scope.formData = {};
        $scope.formData.code = GET.code;
        $scope.formData.email = GET.email;
    }

    // try to set new password in endpoint
    $scope.performRequest = function() {
        tokenManager.getToken().then(function(newToken) {
            var formData = $.param({
            json: JSON.stringify({
                    code : $scope.formData.code,
                    email : $scope.formData.email,
                    passwordNew : $scope.formData.password,
                    token : newToken
                })
            });

            $http.post($rootScope.baseUrl + '/account/password/reset/set/',formData)
               .then(
                   function(response){ // successful request to backend
                        $scope.requestStatus = response.data;
                        if (response.data == 'success') {
                            $rootScope.feedbackMessage = $scope.dict.status.success;
                            $rootScope.showFeedbackMessage = true;
                            $window.location.href = '#/client/login';
                        }
                   },
                   function(response){ // failed request to backend
                        $scope.requestStatus = "backenderror";
                   }
                );

            $scope.requestInProgress = false;
        });
    }
});
