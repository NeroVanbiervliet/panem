panemApp.controller('bkManageBakeryCtrl', function($scope, dictionary, requestWrapper, $window) {

	// Initialize dictionary
	$scope.dict = dictionary.fillBkManageBakery("nl");

    // contants
    var ONE_DAY_MILLISECONDS = 24 * 60 * 60 * 1000;
    
    // variables
    $scope.emailNotifyNextDayOrder; 
    $scope.pyBakeryInfo; 
    $scope.pyDayOrder; 
    $scope.requestStatus = {}; 
    $scope.tomorrowDate = new Date(new Date().getTime() + ONE_DAY_MILLISECONDS).getTime();
    $scope.notFirstWatch = false; 
    
    // load pyBakeryInfo from backend
    var url = '/bakery/' + $scope.userInfo.bakery.id + '/'
    $scope.requestStatus.pyBakeryInfo = requestWrapper.init(); 
    requestWrapper.get(url).then(function ([newStatus,resultData]) {
        $scope.requestStatus.pyBakeryInfo = newStatus; 
        $scope.pyBakeryInfo = resultData; 
        if(newStatus == 'success') {
            $scope.emailNotifyNextDayOrder = resultData.emailNotifyNextDayOrder;
        }
    });

    // load pyDayOrder from backend
    var url = '/bakery/'+ $scope.userInfo.bakery.id + '/dayOrder/date=' + $scope.tomorrowDate;
    $scope.requestStatus.pyDayOrder = requestWrapper.init(); 
    requestWrapper.get(url).then(function ([newStatus,resultData]) {
        $scope.requestStatus.pyDayOrder = newStatus; 
        $scope.pyDayOrder = resultData; 
    });
    
    // watch a change in email preferences
    $scope.$watch('emailNotifyNextDayOrder', function (newValue,oldValue) {
        if($scope.emailNotifyNextDayOrder!==undefined) {
            if(!$scope.notFirstWatch) { // the first time this watch is triggered, is not by human control but by code, thus ne+eds to be ignored
                $scope.notFirstWatch = true;
            }
            else {
                saveEmailSettings(); 
            }
        }
    });
    
    // save the email preferences in the backend
    function saveEmailSettings() {
        url = '/bakery/update/emailnotifications/';
        dataToSend = {
            emailNotifyNextDayOrder : $scope.emailNotifyNextDayOrder,
            id : $scope.pyBakeryInfo.id
        };
        $scope.requestStatus.saveEmailSettings = requestWrapper.init(); 
        requestWrapper.post(url, dataToSend).then(function (newStatus) {
            $scope.requestStatus.saveEmailSettings = newStatus; 
        });
    }; 
});