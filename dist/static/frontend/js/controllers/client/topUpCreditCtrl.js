panemApp.controller('clTopUpCreditCtrl', function($scope, dictionary, requestWrapper) {

    // initialize dictionary
	$scope.dict =  dictionary.fillClTopUpCredit("nl");

    // VARIABLES
    $scope.pyBill;
    $scope.requestStatus = {};
	$scope.smartChangeCount = 0;
	$scope.promoCheck;
	$scope.promoCode;

    function parsedPromoCode() {
        return $scope.promoCode.toUpperCase().replace(/\W/g, '');
    }

    // proceed to adyen payment
    $scope.proceedPaymentAdyen = function() {

        skin = 'default';
        // detect if the device is mobile or not
        if(document.documentElement.clientWidth < 768) {
            skin = 'mobile';
        }

        // get bill from endpoint
        var url = '/me/topup/bill/amount=' + $scope.amountTopUp*100 + '&skin=' + skin + '&promocode=' + parsedPromoCode();
        $scope.requestStatus.bill = requestWrapper.init();
        requestWrapper.get(url).then(function ([newStatus,resultData]) {
            $scope.requestStatus.bill = newStatus;
            $scope.pyBill = resultData;
        });

        // try to submit form when data is ready
        $scope.$watch('pyBill', function() {
            if($scope.pyBill !== undefined && $scope.pyBill.merchantSig != "" && $scope.pyBill.merchantSig != null) {
                $('#hiddenForm').submit();
            }
        });
    };

	// checks for changes in an input in a smart way
	$scope.checkChangeSmart = function() {
		// get my count
		var myCount = $scope.smartChangeCount +1;
		$scope.smartChangeCount++;

		// wait for one seconds
		setTimeout(function(){
		    if ($scope.smartChangeCount == myCount)
				checkPromoCode();
		}, 1000);
	};

	function checkPromoCode() {
		// perform endpoint request
		var url = '/promo/check/code=' + parsedPromoCode();
	    $scope.requestStatus.promo = requestWrapper.init();
	    requestWrapper.get(url).then(function ([newStatus,resultData]) {
	        $scope.requestStatus.promo = newStatus;
	        $scope.promoCheck = resultData;
	    });
	}

});
