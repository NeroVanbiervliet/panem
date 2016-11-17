panemApp.controller('clConfirmOrderCtrl', function($scope, $rootScope, $window, dictionary, processDate, tokenManager, $http, requestWrapper) {

    // variables
    $scope.pyOrder;
    $scope.pyCreditBill;

    $scope.firstTimeClicked = false;

    $scope.requestStatus = {};
    $scope.smartChangeCount = 0;
	$scope.promoCheck;
	$scope.promoCode;

    // initialise dictionary
    $scope.dict = dictionary.fillClConfirmOrder("nl");

    $scope.extraCredit = 0; // NEED ambetant want als je het op nul initialiseert toont hij placeholder niet meer, maar anders flipt de GET omdat extraCredit mogelijks niet bestaat => dan op nul zetten?

    // constants
    $scope.PRODUCT_IMAGE_SOURCE = "images/products/50/";
    $scope.PRODUCT_IMAGE_EXTENSION = ".png";
    $scope.SHOP_IMAGE_SOURCE = "images/shops/800x500/"; // TODO larger image for bakery page?
    $scope.IMAGE_EXTENSION = ".png";

    // FUNCTIONS

    // load current order from endpoint
    var loadCurrentOrder = function(token) {
        $http({
            method : "GET",
            url : $rootScope.baseUrl + "/order/current/token=" + token
        }).then(function(response) {
            $scope.pyOrder = response.data;

        }, function(response) {
            $scope.pyOrder = {};
            // NEED zien wat dit geeft
        });
    };

    // load credit bill
    var loadCreditBill = function(token) {
        $http({
            method : "GET",
            url : $rootScope.baseUrl + "/order/current/bill/credit/token=" + token
        }).then(function(response) {
            $scope.pyCreditBill = response.data;
            $scope.credit = $scope.pyCreditBill.credit;
        }, function(response) {
            $scope.pyCreditBill = {};
            // NEED zien wat dit geeft
        });
    };

    // load data when token is available
    tokenManager.getToken().then(function(newToken) {
        // access endpoints
        loadCurrentOrder(newToken);
        loadCreditBill(newToken);
    });

    // set up date processing
    processDate.setLang("nl");
    $scope.getQualitative = processDate.getWordDate;

    // checks if the button is twice clicked
    $scope.checkDoubleButtonClick = function(event) {
        if(!$scope.firstTimeClicked) {
            // the button was not clicked before
            $scope.firstTimeClicked = true;
            $(event.target).blur(); // lose focus of event.target = button object
        }
        else
            if($scope.credit >= $scope.pyOrder.totalPrice)
                proceedPaymentCredit();
            else
                proceedPaymentAdyen();
    };

    // proceed to adyen payment
    function proceedPaymentAdyen() {

        skin = 'default';
        // detect if the device is mobile or not
        if(document.documentElement.clientWidth < 768) {
            skin = 'mobile';
        }

        // get bill from endpoint after obtaining a token
        tokenManager.getToken().then(function(newToken) {
            $http({
                method : "GET",
                url : $rootScope.baseUrl + '/order/current/bill/cash/extraCredit=' + $scope.extraCredit*100 + "&skin=" + skin +  "&promocode=" + $scope.promoCode + "&token=" + newToken + "/"
            }).then(function(response) {
                $scope.pyBill = response.data;
            }, function(response) {
                console.log(response.data);
                $scope.pyBill = [];
            });
        });

        // try to submit form when data is ready
        // try to submit form when data is ready
        $scope.$watch('pyBill', function() {
            if($scope.pyBill !== undefined && $scope.pyBill.merchantSig != "" && $scope.pyBill.merchantSig != null) {
                $('#hiddenForm').submit();
            }
        });
    }

    // proceed with credit payment
    function proceedPaymentCredit() {
        url = '/order/current/pay/';
        dataToSend = {};
        requestWrapper.post(url, dataToSend).then(function (newStatus) {
            // redirect page
            $window.location.href = '#/client/finalisepayment?credit=true&status='+newStatus;
        });
    }

    // promo code functions
    function checkPromoCode() {
		// perform endpoint request
		var url = '/promo/check/code=' + $scope.promoCode;
	    $scope.requestStatus.promo = requestWrapper.init();
	    requestWrapper.get(url).then(function ([newStatus,resultData]) {
	        $scope.requestStatus.promo = newStatus;
	        $scope.promoCheck = resultData;
	    });
	}

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
});
