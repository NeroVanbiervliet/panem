panemApp.controller('bkRegisterCtrl', function($scope, dictionary, requestWrapper) {

	// Initialize dictionary
	$scope.dict = dictionary.fillBkRegister("nl");

    // VARIABLES
    $scope.requestInProgress = false;
    $scope.person;
    $scope.bakery;

    // FUNCTIONS

    // attempts to start a backend request
    $scope.submitForm = function() {
        if(!$scope.requestInProgress)
        {
            $scope.performRequest();
        }
    };

    // performs the backend request
    $scope.performRequest = function() {
        $scope.requestInProgress = true;
        $scope.requestStatus = requestWrapper.init();

        var dataToSend = {
            'personInfo' : $scope.person,
            'bakeryInfo' : $scope.bakery
        };

        requestWrapper.post('/bakery/create/',dataToSend).then(function (newStatus) {
            $scope.requestStatus = newStatus;
            $scope.requestInProgress = false;
        });
    };
});
