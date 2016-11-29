panemApp.controller('clVerifyAccountCtrl', function($scope, $rootScope, dictionary, requestWrapper, $location, tokenManager, GETUrl, userInfo, $window) {

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
        var newStatusStripped = newStatus.replace('error-message-','');
        var errorMessages = ['wrong-code','acc-not-found','already-verified'];
        if (errorMessages.indexOf(newStatusStripped) > -1) {
            // show error message
            $scope.requestStatus = newStatusStripped;
        }
        else {
            // store token in cookie
            tokenManager.setToken(newStatusStripped);

            // service userInfo
            userInfo.updateInfo().then(function (loadedInfo) {
                $rootScope.userInfo =  loadedInfo;

                // set boolean logged in
                $rootScope.loggedIn = true;

                // set alert bar
                $rootScope.feedbackMessage = $scope.dict.confirmed;
        		$rootScope.showFeedbackMessage = true;

                // if client login, redirect to where page the user came from, elsewise redirect to managebakery
                if($rootScope.userInfo.type == 'normal') {
                    $window.location.href = '#/client/home';
                }
                else { // baker login
                    $window.location = '#/baker/managebakery/';
                }
            });
        }


    });
});
