panemApp.controller('clContactCtrl', function($scope, $rootScope, dictionary, tokenManager, $http, $window) {

    // VARIABLES
    $scope.form = {};

    // initialise
    $scope.form.name = "";
    $scope.form.email = "";
    $scope.form.telephone = "";
    $scope.form.question = "";
    $scope.requestStatus = "init";

	// initialize dictionary
	$scope.dict =  dictionary.fillClContact("nl");

    // fills the email form with know data if someone is logged in
    if($rootScope.loggedIn)
    {
        $rootScope.$watch('userInfo', function() {
            $scope.form.name = $rootScope.userInfo.firstName + ' ' + $rootScope.userInfo.lastName;
            $scope.form.email = $rootScope.userInfo.email;
        }, true);
    }

    // submits form to backend
    $scope.submitForm = function() {

        var requestData;

        tokenManager.getToken().then(function(newToken) {
            // prepare data
            requestData = $.param({
                json: JSON.stringify({
                token : newToken,
                name : $scope.form.name,
                email : $scope.form.email,
                telephone : $scope.form.telephone,
                question : $scope.form.question
                })
            });

            // perform endpoint request
            $http.post($rootScope.baseUrl + '/contact/',requestData)
            .then(
                function(response){ // successful request to backend
                    $scope.requestStatus = response.data;
                    if(response.data == 'success') {
                        $window.location.href = '#/client/contactsuccess';
                    }
                },
                function(response){ // failed request to backend
                    $scope.requestStatus = "backenderror";
                    // NEED notify user that something whent wrong
                }
            );
        })
    }
});
