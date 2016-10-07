panemApp.controller('clConfirmOrderCtrl', function($scope, $rootScope, $window, dictionary, processDate, tokenManager, $http) {
    
    // variables 
    $scope.pyOrder; 
    $scope.pyCreditBill; 
    
    $scope.extraCredit = 0; // NEED ambetant want als je het op nul initialiseert toont hij placeholder niet meer, maar anders flipt de GET omdat extraCredit mogelijks niet bestaat => dan op nul zetten? 
    
    // constants 
    $scope.PRODUCT_IMAGE_SOURCE = "images/products_id/"; // NEED veranderen
    $scope.PRODUCT_IMAGE_EXTENSION = ".jpg";
    
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
        })
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
        })
    };
    
    // load data when token is available
    tokenManager.getToken().then(function(newToken) {
        // access endpoints
        loadCurrentOrder(newToken); 
        loadCreditBill(newToken);
    });
    
    // initialise dictionary
    $scope.dict = dictionary.fillClConfirmOrder("nl");

    // set up date processing
    processDate.setLang("nl");
    $scope.getQualitative = processDate.getWordDate; 
    
    $scope.returnToEditOrder = function() {
        $window.location.href = "#/client/bakery?bakeryId="+$scope.pyOrder.bakeryId;
    }
    
    $scope.proceedPayment = function() {
        
        // convert input in euro to eurocent
        $scope.extraCredit = $scope.extraCredit*100;
        
        // get bill from endpoint after obtaining a token
        tokenManager.getToken().then(function(newToken) {
            $http({
                method : "GET",
                url : $rootScope.baseUrl + '/order/current/bill/cash/extraCredit=' + $scope.extraCredit + "&token=" + newToken + "/"
            }).then(function(response) {
                $scope.pyBill = response.data;
            }, function(response) {
                console.log(response.data);
                $scope.pyBill = [];
                // NEED hoe backend errors handlen, alert dat ze moeten pagina herladen?
            });
        }); 
        
        // try to submit form when data is ready    
        function trySubmitForm() {
            $scope.$watch('pyBill', function() {
                if($scope.pyBill.merchantSig != "" && $scope.pyBill.merchantSig != null)
                {
                    $('#hiddenForm').submit();
                }
                else
                {
                    // wait again for changes in pyBill
                    trySubmitForm();
                }
            });
        };
        
        trySubmitForm();
    }; 
});