panemApp.controller('bkRegisterCtrl', function($scope, $rootScope, dictionary, requestWrapper, $window) {

	// Initialize dictionary
	$scope.dict = dictionary.fillBkRegister("nl");

    // VARIABLES
    $scope.person;
    $scope.bakery;

    // FUNCTIONS

    // performs the backend request
    $scope.performRequest = function() {
        $scope.requestStatus = requestWrapper.init();

        var dataToSend = {
            'personInfo' : $scope.person,
            'bakeryInfo' : $scope.bakery
        };

        requestWrapper.post('/bakery/create/',dataToSend).then(function (newStatus) {
            $scope.requestStatus = newStatus;

            // show alert bar and redirect to home
            if (newStatus == 'success') {
                $rootScope.feedbackMessage = $scope.dict.status.success;
                $rootScope.showFeedbackMessage = true;
                $window.location.href = '#/client/home';
            }
        });
    };
});
