panemApp.controller('clMyAccountCtrl', function($scope, $rootScope, dictionary, $http, tokenManager, processDate, $window, userInfo) {


    // VARIABLES

    $scope.pyPreviousOrders;

    // MAIN

    loadPyPreviousOrders();

    // initialize dictionary
	$scope.dict =  dictionary.fillClMyAccount("nl");

    // reload userInfo, information can be outdated
    userInfo.updateInfo().then(function (loadedInfo) {
        $rootScope.userInfo =  loadedInfo;
    });


    // FUNCTIONS

    // loads the pyPreviousOrders variable
    function loadPyPreviousOrders() {
        tokenManager.getToken().then(function(newToken) {
            $http({
                method : "GET",
                url : $rootScope.baseUrl + "/me/allPreviousOrders/token=" + newToken
            }).then(function(response) {
                $scope.pyPreviousOrders = response.data;
                processPreviousOrders();

            }, function(response) {
                $scope.pyPreviousOrders = [];
                // NEED zien wat dit geeft
            })
        });
    }

    // process previous order data
    function processPreviousOrders() {
        for(var i = 0; i < $scope.pyPreviousOrders.length; i++)
        {
            var previousOrder = $scope.pyPreviousOrders[i];

            // set up date processing
            processDate.setLang("nl");

            // convert 12-12-16 to saturday 12 december - three weeks ago
            previousOrder.date = processDate.getWordDate(previousOrder.date, true);
        }
    }

    // redirects to the bakery of the order
    $scope.navigateToOrder = function(orderId, bakeryId) {
        $window.location.href = "#/client/bakery?bakeryId="+bakeryId+"&orderId="+orderId;
    };

});
