panemApp.controller('clBakeryCtrl', function($scope, $rootScope, dictionary, $window, $cookies, $http, tokenManager, processDate, GETUrl, requestWrapper) {

    window.scope = $scope; // NEED weg doen

	// define variables
    $scope.pyBakeryInfo;
    $scope.pyCategories;
    $scope.pyPreviousOrders;
    $scope.pyDisabledDatesInt;

    $scope.dict;

    $scope.totalPrice = 0;
    $scope.remarks = "";
    $scope.token;

    $scope.openingsToday;

    $scope.order = {};
    $scope.order.products = [];
    // initialisation is ne-eded to prevent empty dropdown item to spawn
    $scope.order.selectedOrderId = "-1";

    $scope.smallDevices = (document.documentElement.clientWidth < 768);

    $scope.pastLimitTime;
    $scope.pickUpTime = {};

    var classNameMinus;

    // datepicker
    var datePickerVar; // to store the datepicker object
    var colProductThumbnail;
    var pickerProps; // properties

    var GET;

    // define constants
    $scope.ONE_DAY_MILLISECONDS;
    var ONE_MIN_MS = 1000*60;
    var ONE_HOUR_MS = 1000*60*60;
    $scope.SHOP_IMAGE_SOURCE = "images/shops/800x500/"; // TODO larger image for bakery page?
    $scope.IMAGE_EXTENSION = ".png";
    if (document.documentElement.clientWidth < 768) {
        $scope.PRODUCT_IMAGE_SOURCE = "images/products/50/"; // for mobile devices
    }
    else {
        $scope.PRODUCT_IMAGE_SOURCE = "images/products/100/";
    }
    var LIMIT_ADVANCE_BOOKING = 34;

    // initialise variables
    initialiseVariables();

    // initialise components
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
            if("orderId" in GET) {
                $scope.order.selectedOrderId = GET.orderId;
            }
            loadOrder();
        }, function(response) {
            $scope.pyPreviousOrders = [];
        });
    }

    // get pyCategories
    var loadProducts = function (token){
        $http({
            method : "GET",
            url : $rootScope.baseUrl + "/bakery/" + $scope.bakeryId + "/products/categories/token=" + token
        }).then(function(response) {
            $scope.pyCategories = response.data;
            generateDisplayNames();
            checkForEmtpyCategories();
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
            loadDatePicker();

            // complete page title
            $rootScope.title += $scope.pyBakeryInfo.name;

        }, function(response) {
            $scope.pyBakeryInfo = {};
            // TODO dit geeft een slechte pagina
        });
    }

    // generate displayNames
    function generateDisplayNames() {
        for(var i=0; i<$scope.pyCategories.length; i++) {
            var currentCat = $scope.pyCategories[i];

            for(var j=0; j<currentCat.products.length; j++) {
                var currentProduct = currentCat.products[j];

                addDisplayNamesToProduct(currentProduct);
            }
        }
    }

    function checkForEmtpyCategories() {
        for(var i=0; i<$scope.pyCategories.length; i++) {
            var currentCat = $scope.pyCategories[i];

            var noRenderedItems = true;
            for(var j=0; j<currentCat.products.length; j++) {
                if (currentCat.products[j].available) {
                    noRenderedItems = false;
                    break;
                }
            }
            currentCat.noRenderedItems = noRenderedItems;
        }
    }

    function addDisplayNamesToProduct(product) {
        // displayName
        var displayName = cutNamesSmart(product.name.split(' '),20);

        // displayNameMobile
        var displayNameMobile = cutNamesSmart(product.name.split(' '),11);

        // used in order
        product.displayNameOrder = displayName;

        // used in tabs
        if($scope.smallDevices) {
            product.displayNameTabs = displayNameMobile;
        }
        else {
            product.displayNameTabs = displayName;
        }
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
    }

    function loadDatePicker() {
        // GET disabled dates from endpoint
        var url = '/bakery/' + GET.bakeryId + '/disabledates/';
        $scope.requestStatusDisableDates = requestWrapper.init();
        requestWrapper.get(url).then(function ([newStatus,resultData]) {
            $scope.requestStatusDisableDates = newStatus;
            $scope.pyDisabledDatesInt = resultData;
            $scope.pyDisabledDatesIntOriginal = resultData.slice(); // value copy

            checkPastLimitTime();

            // process disabledDates
            this.pickerProps = {};
            this.pickerProps.startDate = new Date((new Date()).getTime() + $scope.ONE_DAY_MILLISECONDS);
            this.pickerProps.endDate = new Date((new Date()).getTime() + $scope.ONE_DAY_MILLISECONDS*LIMIT_ADVANCE_BOOKING); // limit booking to LIMIT_ADVANCE_BOOKING days in advance

            this.pickerProps.disabledDates = [];
            if ($scope.pastLimitTime && $scope.pyDisabledDatesInt.indexOf(1) == -1) // tomorrow not yet in disabledDatesInt
                $scope.pyDisabledDatesInt.push(1)
            // add disabledDates to calendar
            for(var i=0; i<$scope.pyDisabledDatesInt.length; i++) {
                var numDays = $scope.pyDisabledDatesInt[i];
                var currentDisabledDate = new Date((new Date()).getTime() + $scope.ONE_DAY_MILLISECONDS*numDays);
                this.pickerProps.disabledDates.push(currentDisabledDate);
            }

            // search for first available date
            this.pickerProps.defDate = this.pickerProps.startDate;
            if(this.pickerProps.disabledDates.length > 0) {
                for(var i=0; i <= LIMIT_ADVANCE_BOOKING; i++) {
                    if ($scope.pyDisabledDatesInt.indexOf(i+1) == -1) {
                        this.pickerProps.defDate = new Date(this.pickerProps.startDate.getTime() + $scope.ONE_DAY_MILLISECONDS*i);
                        $scope.selectedDateInt = i +1;
                        // set hour default selection
                        $scope.pickUpTime.hour = $scope.getValidHourChoices()[0];
                        $scope.pickUpTime.minutes = $scope.getValidMinuteChoices()[0];
                        break;
                    }
                }
            }

            if (!$scope.smallDevices) {
                initialiseDatePicker(); // initialise beautiful calendar
            }
            else
                initialiseNativeCalendar(); // initialise native html5 calendar

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
            $scope.pyBakeryInfo.parsedOpenings = inputOpeningHours;
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
                var isOpen = dayHours[2];

                if(i+1==currentDayOfTheWeek)
                {
                    // set current day bold
                    if (isOpen) {
                        $scope.openingsToday = opening.h + dict.hourAbbr + opening.m + "-" + closing.h + dict.hourAbbr + closing.m;
                        processedOpeningHours += "<strong>" + dict.weekDaysNew[i].charAt(0).toUpperCase() + dict.weekDaysNew[i].substring(1) + " " + $scope.openingsToday + "</strong>";
                    }
                    else {
                        $scope.openingsToday = dict.closed;
                        processedOpeningHours += "<strong>" + dict.weekDaysNew[i].charAt(0).toUpperCase() + dict.weekDaysNew[i].substring(1) + " " + $scope.openingsToday + "</strong>";
                    }
                }
                else
                {
                    // other days no bold
                    if (isOpen)
                        processedOpeningHours += "<div>" + dict.weekDaysNew[i].charAt(0).toUpperCase() + dict.weekDaysNew[i].substring(1) + " " + opening.h + dict.hourAbbr + opening.m + "-" + closing.h + dict.hourAbbr + closing.m + "</div>";
                    else
                        processedOpeningHours += "<div>" + dict.weekDaysNew[i].charAt(0).toUpperCase() + dict.weekDaysNew[i].substring(1) + " " + dict.closed + "</div>";
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
            language : $scope.dict.IETF, // e.g. nl-BE
            autoclose : true,
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
        })
        .on('changeDate', function(e) {
            var newDate = $('#calendarDiv').datepicker('getDate');
            newDate.setHours(0,0,0,0);
            var today = (new Date());
            today.setHours(0,0,0,0);
            $scope.selectedDateInt = (newDate - today)/$scope.ONE_DAY_MILLISECONDS; // datepicker initialisation
            // set hour default selection
            $scope.pickUpTime.hour = $scope.getValidHourChoices()[0];
            $scope.$apply();
        });

        // set the default date
        setPickerDate(this.pickerProps.defDate);
    }

    // sets the date of the picker, dependent if the picker is mobile or desktop
    function setPickerDate(date) {
        if($scope.smallDevices) { // mobile
            $('#nativeCalendar').attr('value', date.toISOString().split('T')[0]);
        }
        else
            datePickerVar.datepicker('setDate',date);
    }

    // checks if it is already past the limit time to order for tomorrow
    function checkPastLimitTime() {
        if ($scope.pyDisabledDatesInt.indexOf(1) > -1) // tomorrow is already disabled by disabledates
            $scope.pastLimitTime = false;
        else {
            [limitHour,limitMinute] = $scope.pyBakeryInfo.bestelLimitTime.split(":");
            var now = new Date();
            $scope.pastLimitTime = (now.getHours() >= limitHour) && (now.getMinutes() >= limitMinute);
        }
    }

    // initialises the native html 5 calendar
    function initialiseNativeCalendar() {
        // set limits to min and maximum order date format e.g. 2016-11-21
        $('#nativeCalendar').attr('min', this.pickerProps.startDate.toISOString().split('T')[0]);
        $('#nativeCalendar').attr('max', this.pickerProps.endDate.toISOString().split('T')[0]);
        // set default date
        $('#nativeCalendar').attr('value', this.pickerProps.defDate.toISOString().split('T')[0]);

        $('#nativeCalendar').on('change', function() {
            var newSelectedDate = new Date($('#nativeCalendar').val());
            newSelectedDate.setHours(0,0,0,0);
            var today = new Date();
            today.setHours(0,0,0,0);
            $scope.selectedDateInt = (newSelectedDate-today)/$scope.ONE_DAY_MILLISECONDS;
            // set hour default selection
            $scope.pickUpTime.hour = $scope.getValidHourChoices()[0];
            $scope.$apply();
        });
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
                // add products one by one
                for(var i=0; i<prevOrder.products.length; i++) {
                    // add display names
                    addDisplayNamesToProduct(prevOrder.products[i]);

                    // add products to order
                    $scope.addProductToOrder(prevOrder.products[i]);
                }
            }
        }
        else // no previous order selected
        {
            // check if a current order is present in the backend
            var currentOrderBackend;
            var url = '/order/current/';
            $scope.requestStatus = requestWrapper.init();
            requestWrapper.get(url).then(function ([newStatus,resultData]) {
                $scope.requestStatus = newStatus;
                currentOrderBackend = resultData;

                if(typeof(currentOrderBackend) != "string" && currentOrderBackend.bakery.id == $scope.bakeryId) {
                    // add products one by one
                    for(var i=0; i<currentOrderBackend.products.length; i++) {
                        // add display names
                        addDisplayNamesToProduct(currentOrderBackend.products[i]);

                        // add to order
                        $scope.addProductToOrder(currentOrderBackend.products[i]);
                    }
                }
                else { // response is nocurrentorder OR tokennotauthorised
                    // set empty current order
                    $scope.order.products = [];
                }
            });
        }
    };

    $scope.loadOrder = loadOrder;

    // increase the amount of a product in an order
    $scope.increaseAmount = function(product) {
        product.amount++;
    };

    $scope.decreaseAmount = function(product) {
        if (product.amount > 1) {
            product.amount--;
        }
        else { // next count will be zero
            // remove product from order
            $scope.removeProductFromOrder(product);
        }
    };

    // changes the date of the date displayed in calendarDiv to the date of today + moreDays
    $scope.setCalenderDivDate = function(moreDays) {
        var dateMoreDays = new Date(new Date().getTime() + $scope.ONE_DAY_MILLISECONDS*moreDays);
        setPickerDate(dateMoreDays);
    };

    // add product to order
    $scope.addProductToOrder = function(product) {
        // TODO kan mss beter met jQuery, maar jQuery.inArray werkt niet ...
        var inOrder = false;
        var i;

        for(i=0; i<$scope.order.products.length; i++)
        {
            if($scope.order.products[i].id == product.id)
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
            $scope.order.products.push($.extend({ // extend joins two {} {} dictionaries
                'amount' : 1
            },product));
        }
    };

    // remove product from order
    $scope.removeProductFromOrder = function(product) {
        for(var i=0; i<$scope.order.products.length; i++)
        {
            if($scope.order.products[i].id == product.id)
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
                "productId" : orderedProduct.id,
                "amount" : orderedProduct.amount
            };
            productArray.push(productToStore);
        }

        // create the time to pickup
        var timePickupToStore = new Date((new Date()).getTime() + $scope.ONE_DAY_MILLISECONDS*$scope.selectedDateInt);
        timePickupToStore.setHours(0,0,0,0);
        timePickupToStore = timePickupToStore.getTime();
        timePickupToStore += ONE_HOUR_MS*parseInt($scope.pickUpTime.hour) + ONE_MIN_MS*parseInt($scope.pickUpTime.minutes);

        console.log(timePickupToStore);

        // prepare to store order in backend
        var requestData = $.param({
            json: JSON.stringify({
                productArray: productArray,
                bakeryId: parseInt($scope.bakeryId),
                timePickup: timePickupToStore,
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

    // displayNames cutting function
    // spl is an array of words
    function cutNamesSmart(spl, maxWidth) {

        // JOIN PARTS IF POSSIBLE
    	var joinFinish = true;
    	for(var i=1; i<spl.length; i++) {
    		if (spl[i].length + spl[i-1].length <= maxWidth-1) { // -1 because a space will be added
    			spl[i-1] = spl[i-1] + " " + spl[i];
    			spl.splice(i, 1);
    			joinFinish = false;
    			break;
            }
        }

    	if (!joinFinish)
    		cutNamesSmart(spl, maxWidth);

        // SPLIT TOO LARGE WORDS
    	var cutFinish = true;
    	for(var i=0; i<spl.length; i++) {
    		if (spl[i].length > maxWidth) {

    			// check if at least 4 characters could be added to the previous line
    			if(i-1>=0 && spl[i-1].length + 4 < maxWidth) {
    				var extraSpace = maxW-2-spl[i-1].length;
    				var originalStr = spl[i];
    				spl[i] = originalStr.substring(0,extraSpace) + "-";
    				spl.splice(i+1,0,originalStr.substring(extraSpace));
    				cutFinish = false;
    				break;
                }
    			else {
    				var originalStr = spl[i];
    				spl[i] = originalStr.substring(0,maxWidth-1) + "-";
    				spl.splice(i+1,0,originalStr.substring(maxWidth));
    				cutFinish = false;
    				break;
                }
            }
        }
    	if (!cutFinish)
    		cutNamesSmart(spl, maxWidth);
        else
            return spl
    }

    // get valid hour choices
    $scope.getValidHourChoices = function() {
        var output = [];

        // get current day of the week
        var curDayWeek  = (new Date()).getDay(); // 0=sunday, 1=monday, 6=saturday
        var selectedDayWeek = ((curDayWeek + $scope.selectedDateInt)-1)%7; // 0=monday, 6=sunday

        if (typeof $scope.pyBakeryInfo !== 'undefined' && typeof $scope.selectedDateInt !== 'undefined') {
            var openingsSelectedDay = $scope.pyBakeryInfo.parsedOpenings[selectedDayWeek];
            for(var i=0; i<25; i++) {
                if (i >= parseInt(openingsSelectedDay[0].h) && i <= parseInt(openingsSelectedDay[1].h))
                    output.push(i);
            }

            $scope.selectedDayOpenings = openingsSelectedDay;
        }

        return output;
    };

    // get valid minute choices
    $scope.getValidMinuteChoices = function() {
        output = [];

        var minChoices = ['00','15','30','45'];

        // TODO gaat fout als opening en sluitingsuur in het zelfde uur zijn
        if (typeof $scope.selectedDayOpenings !== 'undefined') {
            var openingsSelectedDay = $scope.selectedDayOpenings;
            if($scope.pickUpTime.hour != openingsSelectedDay[0].h && $scope.pickUpTime.hour != openingsSelectedDay[1].h) // not opening or closing our, so everything is possible
                output = minChoices;
            else if ($scope.pickUpTime.hour == openingsSelectedDay[0].h) { // opening hour
                for(var i=0; i<4; i++) {
                    if (i*15 >= openingsSelectedDay[0].m)
                        output.push(minChoices[i]);
                }
            }
            else if ($scope.pickUpTime.hour == openingsSelectedDay[1].h) { // closing hour
                for(var i=0; i<4; i++) {
                    if (i*15 <= openingsSelectedDay[1].m)
                        output.push(minChoices[i]);
                }
            }
        }

        return output;
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
                totPrice += product.price * product.amount;
            }

            $scope.totalPrice = totPrice;
        }
    }, true);

    $scope.$watch('selectedDateInt', function() {
        $scope.pickUpTime.minutes = $scope.getValidMinuteChoices()[0];
    },true)


});
