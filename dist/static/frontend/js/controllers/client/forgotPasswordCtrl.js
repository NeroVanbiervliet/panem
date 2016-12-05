panemApp.controller('clForgotPasswordCtrl', function($scope, dictionary, requestWrapper, GETUrl, tokenManager, $rootScope, requestWrapper, $window) {

    // initialize dictionary
	$scope.dict =  dictionary.fillClForgotPassword("nl");

    // VARIABLES
    $scope.email;

    // obtain parameters from url
    var GET = GETUrl.decipher();

    if ('email' in GET) {
        $scope.email = GET.email;
    }

    // performs the forgot password request to the database
    $scope.performRequest = function() {
        postData = {
            email : $scope.email
        }
        $scope.requestStatus = requestWrapper.init();
        requestWrapper.post('/account/password/reset/mail/', postData).then(function (newStatus) {
            $scope.requestStatus = newStatus;
            if (newStatus == 'success') {
                $rootScope.feedbackMessage = $scope.dict.status.success + ' ' + $scope.email;
                $rootScope.showFeedbackMessage = true;
                $window.location.href = '#/client/home';
            }
        });
    }
});
