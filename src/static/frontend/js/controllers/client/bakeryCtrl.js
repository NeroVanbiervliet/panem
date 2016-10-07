panemApp.controller('clBakeryCtrl', function($scope, $rootScope, dictionary, $window, $cookies, $http, tokenManager, processDate, GETUrl) {

	// define variables
    $scope.pyBakeryInfo;
    $scope.pyCategories;
    $scope.pyProducts;
    $scope.pyPreviousOrders;
    $scope.pyDisabledDates;
    
    $scope.dict;
    
    $scope.totalPrice = 0; 
    $scope.remarks = ""; 
    $scope.token;  

    $scope.order = {}; 
    $scope.order.products = []; 
    // initialisation is needed to prevent empty dropdown item to spawn
    $scope.order.selectedOrderId = "-1";
    
    $scope.smallDevices = (document.documentElement.clientWidth < 768);
    
    var classNameMinus; 

    // datepicker
    var datePickerVar; // to store the datepicker object
    var colProductThumbnail; 
    var pickerProps; // properties 
    
    var GET; 
    
    // define constants
    $scope.ONE_DAY_MILLISECONDS; 
    $scope.PRODUCT_IMAGE_SOURCE = "images/products_id/"; // NEED veranderen
    $scope.PRODUCT_IMAGE_EXTENSION = ".jpg";
    
    // initialise variables
    initialiseVariables();
    
    // initialise components
    initialiseDatePicker();
    initialiseTooltipsAndPopovers();
    
    /***************
     *  FUNCTIONS  *
     ***************/
    
    // event fired on window resize, updates smallDevices boolean
    $(window).resize(function(){
        $scope.$apply(function(){
           $scope.smallDevices = (document.documentElement.clientWidth < 768);
        });
    });
    
    // endpoint access
    var loadPreviousOrders = function(token) {
        $http({
            method : "GET",
            url : $rootScope.baseUrl + "/me/previousOrders/bakeryId=" + $scope.bakeryId + "&token=" + token
        }).then(function(response) {
            $scope.pyPreviousOrders = response.data;
            processPreviousOrders();
            // if orderId exist, load the order
            if("orderId" in GET)
            {
                $scope.order.selectedOrderId = GET.orderId; 
                loadOrder(); 
            }
        }, function(response) {
            $scope.pyPreviousOrders = [];
        });
    }
    
    // get pyCategories and pyProducts
    var loadProducts = function (token){
        $http({
            method : "GET",
            url : $rootScope.baseUrl + "/bakery/" + $scope.bakeryId + "/products/categories/token=" + token
        }).then(function(response) {
            $scope.pyCategories = response.data;
        }, function(response) {
            $scope.pyCategories = [];
        });
    }
    
    // get pyDisabledDates NEED afwerken
    var loadDisabledDates = function (token){
        $http({
            method : "GET",
            url : $rootScope.baseUrl + "/bakery/" + $scope.bakeryId + "/products/categories/token=" + token
        }).then(function(response) {
            $scope.pyCategories = response.data;
        }, function(response) {
            $scope.pyCategories = [];
        });
    }
    
    // get pyBakeryInfo
    var loadBakeryInfo = function(token) {
        $http({
            method : "GET",
            url : $rootScope.baseUrl + "/bakery/" + $scope.bakeryId + "/token=" + token
        }).then(function(response) {
            $scope.pyBakeryInfo = response.data;
            processOpeningHours(); 
            
        }, function(response) {
            $scope.pyBakeryInfo = {};
            // TODO dit geeft een slechte pagina
        });
    }
    
    // initialises variables
    function initialiseVariables() {
        
        // CONSTANTS
        $scope.ONE_DAY_MILLISECONDS = 24 * 60 * 60 * 1000; 
        
        // Initialize dictionary
        $scope.dict = dictionary.fillClBakery("nl");
        
        // obtain bakeryId from get in url
        GET = GETUrl.decipher(); 
        $scope.bakeryId = GET.bakeryId;         
        
        // load data when token is available
        tokenManager.getToken().then(function(newToken) {
            $scope.token = newToken; 
            // access endpoints
            loadPreviousOrders(newToken);
            loadProducts(newToken);
            loadBakeryInfo(newToken);
        });
        
        // NEED uit endpoint
        this.pickerProps = {}; 
        this.pickerProps.startDate = new Date(); 
        this.pickerProps.endDate = new Date((new Date()).getTime() + $scope.ONE_DAY_MILLISECONDS*34); // limit booking to 34 days in advance 
        this.pickerProps.disabledDates = [new Date((new Date()).getTime() + $scope.ONE_DAY_MILLISECONDS*2), new Date((new Date()).getTime() + $scope.ONE_DAY_MILLISECONDS)];
        $scope.disabledDatesInt = [1,2,4];
        
    }
    
    // process previous order data
    function processPreviousOrders() {
        for(var i = 0; i < $scope.pyPreviousOrders.length; i++)
        {
            var previousOrder = $scope.pyPreviousOrders[i];

            // set up date processing
            processDate.setLang("nl");            

            // convert 12-12-16 to saturday 12 december - three weeks ago
            previousOrder.dropDownText = processDate.getWordDate(previousOrder.date, false) + ' - ' + processDate.getTimePastIndication(previousOrder.numDaysPast);
        }
    }
        
    // processes the openingHours
    function processOpeningHours() {
        if($scope.pyBakeryInfo.openingHours == "") // no opening hours available
        {
            var processedOpeningHours = $scope.dict.bakeryDescription.noOpeningHours; 
        }
        else   
        {
            // parse json data from string
            var inputOpeningHours = JSON.parse($scope.pyBakeryInfo.openingHours);
            var processedOpeningHours = ""; 

            var dict = $scope.dict; 

            var currentDayOfTheWeek = (new Date()).getDay(); // counts as sunday=0, monday=1...
            if (currentDayOfTheWeek==0) currentDayOfTheWeek=7; 

            // process
            for(var i=0; i<inputOpeningHours.length; i++)
            {
                var dayHours = inputOpeningHours[i];
                var opening = dayHours[0]; 
                var closing = dayHours[1];

                if(i+1==currentDayOfTheWeek)
                {
                    // bold
                    processedOpeningHours += "<strong>" + dict.weekDaysNew[i].charAt(0).toUpperCase() + dict.weekDaysNew[i].substring(1) + " " + opening.h + dict.hourAbbr + opening.m + "-" + closing.h + dict.hourAbbr + closing.m + "</strong>";
                }
                else
                {
                    // no bold
                    processedOpeningHours += "<div>" + dict.weekDaysNew[i].charAt(0).toUpperCase() + dict.weekDaysNew[i].substring(1) + " " + opening.h + dict.hourAbbr + opening.m + "-" + closing.h + dict.hourAbbr + closing.m + "</div>";
                }
            } 
        }
        
        // replace openingHours variable
        $scope.pyBakeryInfo.openingHours = processedOpeningHours;
    }
    
    // initialises the bootstrap tooltips
    function initialiseTooltipsAndPopovers() {
        
        $("[data-toggle=tooltip]").tooltip();
        

        $("[data-toggle=popover]")
        .popover({ // initialise popover + options
            animation: true,
            trigger: 'hover',
            html: true // allows <strong> and <br> tags
          })
        .click(function(e) {
            e.preventDefault();
            $(this).popover('toggle');
            e.stopPropagation();
        });
    }
    
    // initialise datapicker
    function initialiseDatePicker() {

        // store a datepicker object in the calendar div
        datePickerVar = $('#calendarDiv').datepicker({
            startDate : this.pickerProps.startDate,
            endDate : this.pickerProps.endDate,
            datesDisabled : this.pickerProps.disabledDates,
            todayHighlight : true,
            language : $scope.dict.IETF, // e.g. nl-BE
            format: {
                /*
                 * custom panem format
                 */
                toDisplay: function (date, format, language) { // returns a string
                    var options = { weekday: 'long', month: 'long', day: 'numeric' }; 
                    return date.toLocaleDateString($scope.dict.IETF, options); // e.g. maandag 6 februari, voc.IETF = nl-BE
                },
                toValue: function (date, format, language) { // returns a date object
                    var d = new Date(date);
                    return d; 
                }
            } // format
        }) // datepicker initialisation

        // set the date of tomorrow as the default date
        var tomorrowDate = new Date(new Date().getTime() + $scope.ONE_DAY_MILLISECONDS);
        datePickerVar.datepicker('setDate',tomorrowDate);
    }
    
    // returns the string of the date of today + moreDays AS IT'S NAME
    // e.g. monday
    $scope.getDateName = function(moreDays) {
        var dateMoreDays = new Date(new Date().getTime() + $scope.ONE_DAY_MILLISECONDS*moreDays);
        var dateNumber = dateMoreDays.getDay(); 
        return $scope.dict.weekDays[dateNumber];
    };
    
    // loads a previous order into the current order div
    function loadOrder() {
        
        if($scope.order.selectedOrderId != -1)
        {
            var prevOrder; 
            // search for the order with the correct id
            for(var i=0; i<$scope.pyPreviousOrders.length; i++)
            {
                prevOrder = $scope.pyPreviousOrders[i];
                if(prevOrder.id == $scope.order.selectedOrderId)
                {
                    // break when id found
                    break; 
                }
            }
        
            if(prevOrder != undefined)
            {
                $scope.order.products = prevOrder.products;
            }
        }
        else // no previous order selected
        {
            $scope.order.products = [];
        }
        
    };
    
    $scope.loadOrder = loadOrder;
    
    // increase the amount of a product in an order
    $scope.increaseAmount = function(product) {
        product.amount++;
    };
    
    $scope.decreaseAmount = function(product) {
        product.amount--;
    };
    
    // changes the date of the date displayed in calendarDiv to the date of today + moreDays
    $scope.setCalenderDivDate = function(moreDays) {
        var dateMoreDays = new Date(new Date().getTime() + $scope.ONE_DAY_MILLISECONDS*moreDays);
        datePickerVar.datepicker('setDate',dateMoreDays);
    };
    
    // add product to order
    $scope.addProductToOrder = function(product) {
        // TODO kan mss beter met jQuery, maar jQuery.inArray werkt niet ...
        var inOrder = false; 
        var i;
        
        for(i=0; i<$scope.order.products.length; i++)
        {
            if($scope.order.products[i].productData.id == product.id) 
            {
                inOrder = true; 
                break;
            }     
        }
        
        if(inOrder) // product is present in order
        {
            // increase amount in order
            $scope.order.products[i].amount++;
        }
        else // product is not present in order
        {
            // add product to order
            $scope.order.products.push({ 
                'productData' : product,
                'amount' : 1
            });
        }
    };
    
    // remove product from order
    $scope.removeProductFromOrder = function(product) {
        for(var i=0; i<$scope.order.products.length; i++)
        {
            if($scope.order.products[i].productData.id == product.id) 
            {
                // remove product from order.products
                $scope.order.products.splice(i,1);
                break;
            } 
        }
    };
    
    // stores the current order in the backend
    // redirects to the confirm order page
    $scope.proceedToConfirmOrder = function() {
        
        // refactor $scope.order.products
        var productArray = [];
        for(var i=0; i<$scope.order.products.length; i++)
        {
            var orderedProduct = $scope.order.products[i];
            var productToStore = {
                "productId" : orderedProduct.productData.id,
                "amount" : orderedProduct.amount
            };
            productArray.push(productToStore);
        }
        
        // prepare to store order in backend
        var requestData = $.param({
            json: JSON.stringify({
                productArray: productArray,
                bakeryId: parseInt($scope.bakeryId),
                timePickup: $('#calendarDiv').datepicker('getDate').getTime(),
                remarks: $scope.remarks,
                token : $scope.token
            })
        });
        
        // store order in backend
        $http.post($rootScope.baseUrl + '/order/current/',requestData)
            .then(
                function(response){ // successful request to backend
                    $scope.requestStatus = response.data; 
                    // redirect page
                    $window.location.href = "#/client/confirmorder";
                }, 
                function(response){ // failed request to backend
                    $scope.requestStatus = "backenderror"; 
                    // TODO notify user that something whent wrong
                }
            );
    };
    
    /***********
     *  WATCH  *
     ***********/
    
    $scope.$watch('order.products', function() { 
        if ($scope.order.products != null){
            var totPrice = 0; 
        
            // update totalPrice
            for(var i=0; i<$scope.order.products.length; i++)
            {
                var product = $scope.order.products[i];
                totPrice += product.productData.price * product.amount;
            }

            $scope.totalPrice = totPrice;
        }
    }, true);
    
});