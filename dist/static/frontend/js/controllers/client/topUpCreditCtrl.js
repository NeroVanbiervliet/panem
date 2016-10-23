panemApp.controller('clTopUpCreditCtrl', function($scope, dictionary, requestWrapper) {

    // initialize dictionary
	$scope.dict =  dictionary.fillClTopUpCredit("nl");

    // VARIABLES
    $scope.pyBill;
    $scope.requestStatus;

    // proceed to adyen payment
    $scope.proceedPaymentAdyen = function() {

        skin = 'default';
        // detect if the device is mobile or not
        if(document.documentElement.clientWidth < 768) {
            skin = 'mobile'
        }

        // get bill from endpoint
        var url = '/me/topup/bill/amount=' + $scope.amountTopUp*100 + '&skin=' + skin
        $scope.requestStatus = requestWrapper.init();
        requestWrapper.get(url).then(function ([newStatus,resultData]) {
            $scope.requestStatus = newStatus;
            $scope.pyBill = resultData;
        });

        // try to submit form when data is ready
        $scope.$watch('pyBill', function() {
            if($scope.pyBill !== undefined && $scope.pyBill.merchantSig != "" && $scope.pyBill.merchantSig != null) {
                $('#hiddenForm').submit();
            }
        });
    };

});
