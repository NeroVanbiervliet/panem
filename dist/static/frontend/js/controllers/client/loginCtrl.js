panemApp.controller('clLoginCtrl', function($scope, dictionary, $http, $rootScope, tokenManager, userInfo, GETUrl, $window) {

    // initialize dictionary
	$scope.dict =  dictionary.fillClLogin("nl");

    // obtain parameters from url
    var GET = GETUrl.decipher();
    if("source" in GET) // TODO ook resetten naar /client/home als de source /client/login is
    {
        // generate path to return to after login
        var returnPath = 'http://' + $window.location.host + '/#' + decodeURIComponent(GET.source);
    }
    else
    {
        // default return path is home
        var returnPath = 'http://' + $window.location.host + '/#/client/home';
    }

    $scope.submitForm = function() {
        var user = $scope.user;

        var formData = $.param({
            json: JSON.stringify({
                email : user.email,
                password : user.password
            })
        });

        $http.post($rootScope.baseUrl + '/token/create/',formData)
        .then(
            function(response){ // successful request to backend
                if(response.data == "accnotfound" || response.data == "wrongpassword")
                {
                    $scope.requestStatus = response.data;
                }
                else
                {
                    $scope.requestStatus = "success";

                    // store token in cookie
                    tokenManager.setToken(response.data);

                    // service userInfo
                    userInfo.updateInfo().then(function (loadedInfo) {
                        $rootScope.userInfo =  loadedInfo;

						// set boolean logged in
	                    $rootScope.loggedIn = true;

						// if client login, redirect to where page the user came from, elsewise redirect to managebakery
						if($rootScope.userInfo.type == 'normal') {
							$window.location.href = returnPath;
						}
						else { // baker login
							$window.location = '#/baker/managebakery/';
						}
                    });
                }
            },
            function(response){ // failed request to backend
                $scope.requestStatus = "backenderror";
            }
        );
    };
});
