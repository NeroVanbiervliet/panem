panemApp.controller('clFinalisePaymentCtrl', function($scope, dictionary, GETUrl, $rootScope, tokenManager, requestWrapper, $window) {
    window.scope = $scope; // NEED remove
    
    // initialize dictionary
	$scope.dict =  dictionary.fillClFinalisePayment("nl");
    
    // variables
    $scope.status = "loading"; 
    $scope.paymentCode; 
    
    // obtain parameters from url
    $scope.GET = GETUrl.decipher(); 
    
    // analyse url data
    if('credit' in $scope.GET) { // credit variable is present in url => credit payment
        // example for $scope.status : 'success-194'
        if($scope.status.split('-')[0] == 'success') { 
            $scope.status = 'success';
            $scope.paymentCode = 'credit' + $scope.status.split('-')[1];
        }
        else {
            $scope.status = 'refusedPanem';
            $scope.paymentCode = 'creditnotexecuted';
        }
    }
    else { // credit variable is not present in url => adyen payment
        // set payment code for helpdesk
        $scope.paymentCode = $scope.GET.merchantReference;
        
        if($scope.GET.merchantReturnData == 'topUp') { // the payment was to top up the account
            $scope.status = "topUpSuccess";
        }
        else {
            switch($scope.GET.authResult) {
                case "CANCELLED":
                    $scope.status = "cancelled";
                    break;
                case "REFUSED":
                    $scope.status = "refusedAdyen";
                    break;
                case "PENDING": 
                    $scope.status = "pending";
                    break;
                case "ERROR":
                    $scope.status = "adyenerror";
                    break;
                default:
                    // AUTHORISED is also default, further checking in backend is needed
                    $scope.status = "loading";
            }
            
            // verify adyen payment in backend
            verifyAdyenPayment(); // NEED dit buiten de else zetten zodat ook voor topUp in de backend de betaling wordt geverifieerd
        } 
    }
        
    // FUNCTIONS
    
    // verify the adyen payment in the backend
    function verifyAdyenPayment() {
        tokenManager.getToken().then(function(newToken) {
            // add login token to GET
            $scope.GET['token'] = newToken; 
            
            url = '/order/current/receipt/';
            dataToSend = $scope.GET;
            $scope.status = requestWrapper.init(); 
            requestWrapper.post(url, dataToSend).then(function (newStatus) {
                $scope.status = newStatus.split('-')[0]; 
                if(newStatus.split('-')[1] !== undefined) {
                    $scope.paymentCode = 'adyen' + newStatus.split('-')[1]; 
                }
                else
                {
                    $scope.paymentCode = 'adyenfailed'; 
                }
            });
        });
    }
    
    // reloads the page
    $scope.reloadPage = function() {
        $window.location.reload();  
    };
}); 