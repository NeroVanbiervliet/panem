panemApp.controller('clChangePasswordCtrl', function($scope, $rootScope, dictionary, requestWrapper, $window) {

	// VARIABLES
	$scope.requestStatus;

	// initialize dictionary
	$scope.dict =  dictionary.fillClChangePassword("nl");

	// backend call
	$scope.saveNewPass = function() {
		$scope.requestStatus = requestWrapper.init();
		url = '/me/password/change/';
        dataToSend = {
			'passwordOriginal' : $scope.user.passwordOld,
			'passwordNew' : $scope.user.passwordNew,
			'email' : $scope.userInfo.email
		};
        requestWrapper.post(url, dataToSend).then(function (newStatus) {
			handleStatus(newStatus);
        });
	};

	function handleStatus(status) {
		if (status == 'success') {
			// redirect page
			$window.location.href = '#/client/myaccount';
		}
		$scope.requestStatus = status;
		$rootScope.feedbackMessage = $scope.dict.feedbackMessage;
		$rootScope.showFeedbackMessage = true;
	}
});
