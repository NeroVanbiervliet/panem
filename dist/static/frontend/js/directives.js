panemApp.directive('tooltip', function(){
    return {
        restrict: 'A',
        link: function(scope, element, attrs){
            $(element).hover(function(){
                // on mouseenter
                $(element).tooltip('show');
            }, function(){
                // on mouseleave
                $(element).tooltip('hide');
            });
        }
    };
});

panemApp.directive('showTab', function () {
    return {
        link: function (scope, element, attrs) {
            $(element).click(function(e) {
                e.preventDefault();
                $(element).tab('show');
            });
        }
    };
});

// tags input used to show allergies
panemApp.directive('tagsInput', function() {    
    return { 
        link: function (scope, element, attrs) {  
            var bloodhoundVarName = attrs.bloodhound; 
            
            // first initialisation
            $(element).tagsinput({
                    itemValue : 'name',
                    tagClass: function(item) {
                        return 'label label-default'; // gray
                    }
                }
            );
            $(element).parent().addClass("cursor-not-allowed-all-children");
            
            // add ingredient tags
            for(var i=0; i < scope.product.ingredients.length; i++) {
                $(element).tagsinput('add', scope.product.ingredients[i]);
            } 
            
            // watch for changes in checked state
            scope.$watch("product.available",function(newValue,oldValue) {
                var isDisabled; 
                if(newValue == null || newValue == false) { // product not selected
                    isDisabled = true; 
                    $(element).parent().addClass("cursor-not-allowed-all-children");
                }
                else { // product is selected
                    isDisabled = false; 
                    $(element).parent().removeClass("cursor-not-allowed-all-children");
                }
                // initialisation of tagsinput element
                $(element).tagsinput('destroy');
                $(element).tagsinput({
                    itemValue : 'name',
                    freeInput: true,
                    tagClass: function(item) {
                        switch (isDisabled) {
                            case false : 
                                if(item.type == 'standard') 
                                    return 'label label-primary'; // blue
                                else
                                    return  'label label-warning'; // orange
                                   
                            case true  : return 'label label-default'; // gray
                        }
                    },
                    typeaheadjs : [
                        // options
                        {
                            highlight : true
                        },
                        // datasets
                        [
                            // first dataset containing standard products
                            {
                                name: 'standard-products',
                                display: 'name',
                                valueKey: 'name',
                                source: scope[bloodhoundVarName].standard.ttAdapter(),
                                templates: {
                                    header: '<div class="suggestions-header-standard">Standaard</div>'
                                }
                            },
                            // second dataset containing the custom products
                            {
                                name: 'custom-products',
                                display : 'name',
                                valueKey : 'name',
                                source: scope[bloodhoundVarName].custom.ttAdapter(),
                                templates: {
                                    header: '<div class="suggestions-header-custom">Eigen</div>'
                                }
                            }
                        ]
                    ]
                    }
                ); 
                
                // add ingredient tags
                for(var i=0; i < scope.product.ingredients.length; i++) {
                    $(element).tagsinput('add', scope.product.ingredients[i]);
                } 
            });
            
            // watch for added item
            $(element).on('itemAdded', function(event) {
                // check if not yet present in array
                if(scope.product.ingredients.indexOf(event.item) == -1) {
                    scope.product.ingredients.push(event.item);
                }
            });
            
            // watch for added item
            $(element).on('itemRemoved', function(event) {
                // store new ingredients string
                scope.product.ingredients.splice(scope.product.ingredients.indexOf(event.item),1);
            });
            
            // watch for a new added item, not yet known
            $(element).on('unknownItemAdded', function(event) {
                scope.pyIngredients.custom.push(event.item);
                scope[bloodhoundVarName].custom.initialize(true);
                scope.pyNewIngredients.push(event.item);
            });
        }
    };
});

// toggle to enable a product in modifyproducts
panemApp.directive('toggleProducts', function() {
    return {        
        link: function (scope, element, attrs) {   
            // initialisation
            $(element).bootstrapToggle({
              on: 'I', // alternative : '<span class=\"glyphicon glyphicon-ok\"></span>',
              off: 'O', // alternative : '<span class=\"glyphicon glyphicon-remove\"></span>'
            });

            // if boolean is true, set toggle button accordingly
            if(scope.product.available == true)
            {
                $(element).bootstrapToggle('on');
            }

            // event listener for changes
            $(element).change(function() {
                scope.$apply(function () {
                    scope.product.available = $(element).prop('checked'); 
                });
            })
        }
    };
});

// general toggle button that can be used everywhere
// check state is stored in the variable provided in the data-linkvar attribute
// if the linkvariable is in the parent scope, set the data-linkvar-in-parent attribute to true
// -> this is usefull when the toggle creates a seperate scope when used in combination with ng-if
panemApp.directive('toggleGeneral', function() {
    return {        
        link: function (scope, element, attrs) {  
            // initialisation
            $(element).bootstrapToggle({
              on: 'I', //'<span class=\"glyphicon glyphicon-ok\"></span>',
              off: 'O', //'<span class=\"glyphicon glyphicon-remove\"></span>'
            });

            // if boolean is true, set toggle button accordingly
            if(scope[attrs.linkvar] == 'true' || scope[attrs.linkvar])
            {
                $(element).bootstrapToggle('on');
            }
            
            // event listener for changes in toggle state
            $(element).change(function() {
                scope.$apply(function () {
                    if(attrs.linkvarInParent == 'true') {
                        scope.$parent[attrs.linkvar] = $(element).prop('checked'); 
                    }
                    else {
                        scope[attrs.linkvar] = $(element).prop('checked'); // NEED not tested
                    }                    
                });
            })
        }
    };
});

// creates a link <a> tag inside the given element, with the provided information
// needed data-... in source tag: 
//      data-to-substitute : the text to replace by a link
//      data-base-text : the basic text, including the substring that needs to be replaced
//      data-destination : the url corresponding to the link
panemApp.directive('subLink', function() {
    return {        
        link: function (scope, element, attrs) {   
            
            // create link element 
            linkText = "<a href=\"" + attrs.destination + "\">" + attrs.toSubstitute + "</a>";  
            
            // substitute text
            newText = attrs.baseText.replace(attrs.toSubstitute,linkText);
            
            // store new text
            $(element).html(newText);
        }
    };
});

// redirects the angular app to an other page on click
// data-href contains the destination relative url
panemApp.directive('buttonLink', function($window) {
    return {        
        link: function (scope, element, attrs) {   
            $(element).click(function() {
                $window.location.href = attrs.href;
            });
        }
    };
});

panemApp.directive('timepicker', function () {
    return {
        link: function (scope, element, attrs) { 
            var defTime = '00:00'; // default
        
            if($(element).hasClass("timepicker-opening-hours"))
            {
                defTime = (scope.day[0].h + ':' + scope.day[0].m); // e.g. 07:30
            }
            else if($(element).hasClass("timepicker-closing-hours"))
            {
                defTime = (scope.day[1].h + ':' + scope.day[1].m); // e.g. 07:30
            }
            else if($(element).hasClass("timepicker-orderlimit-hours"))
            {
                defTime = scope.pyBakeryInfo.bestelLimitTime;    
            }
            
            // initialise timepicker
            $(element).timepicker({
                minuteStep: 10,
                template: false,
                showSeconds: false,
                showMeridian: false, // 24h mode
                defaultTime: defTime
            });
            
            // add event handler
            $(element).timepicker().on('changeTime.timepicker', function(e) {
                if($(element).hasClass("timepicker-opening-hours"))
                {
                    scope.day[0].h = e.time.hours;
                    scope.day[0].m = e.time.minutes;
                }
                else if($(element).hasClass("timepicker-closing-hours"))
                {
                    scope.day[1].h = e.time.hours;
                    scope.day[1].m = e.time.minutes;
                }
                else if($(element).hasClass("timepicker-orderlimit-hours"))
                {
                    scope.pyBakeryInfo.bestelLimitTime = e.time.hours + ":" + e.time.minutes;    
                }  
            });
        }
    };
});


// data-key needs to provided if requestStatus is a dictionary
panemApp.directive('requestStatusHandler', function (dictionary) {
    return {
        link: function (scope, element, attrs) {
            
            // check if the dictionary contains feedback messages
            if(scope.dict.status == undefined)
            {
                // if no status present, store the default status messages
                var dict = dictionary.fillDirectives('nl',"requestStatusHandler"); // TODO language moet gehaald kunnen worden uit de huidige rootScope of zo
                scope.dict.status = dict.status; 
            }
            
            // auxiliary function
            this.reset = function() {
                $(element).removeClass(); // removes all classes
                element.empty(); 
                $(element).addClass('request-status'); 
                // add user defined classes
                $(element).addClass(attrs.classes);
            };
            
            // generate string of variable to watch
            varToWatch = 'requestStatus'; 
            if(attrs.key !== undefined) {
                varToWatch += '.' + attrs.key
            }
            
            // execute on change in requestStatus
            scope.$watch(varToWatch,function(newValue,oldValue) {
                // reset previous message
                this.reset(); 
                
                if(newValue == null) {
                    // empty div
                }
                else {      
                    
                    var splitStatus; 
                    
                    // differentiate between handling a post request or other get (=default)
                    // split status string in parts
                    if(attrs.requestType == 'post') { // POST
                        splitStatus = newValue.split('-');
                    }
                    else { // GET 
                        splitStatus = newValue[0].split('-');  
                    }
 
                    // set appropriate div text 
                    if(splitStatus[0] == 'working') {
                        element.addClass('loader-small');
                    }
                    else if(splitStatus[0] == 'success') {
                        element.addClass('text-success');
                        chilToAppend = "<span class=\"glyphicon glyphicon-ok\"></span> " + scope.dict.status.success; 
                        element.append(chilToAppend);
                    }
                    else { // splitStatus[0] == 'error'
                        if(splitStatus[1] = 'message' && splitStatus[2] !== undefined && splitStatus[2] in scope.dict.status) { // error-message-<errMsg>
                            // show the error message related to the given <errMsg>
                            element.addClass('text-danger');
                            chilToAppend = "<span class=\"glyphicon glyphicon-flash\"></span> " + scope.dict.status[splitStatus[2]]; // splitStatus[2] == errMsg
                            element.append(chilToAppend);
                        }
                        else { // splitStatus[1] == 'requestWrapper'
                            element.addClass('text-danger');
                            chilToAppend = "<span class=\"glyphicon glyphicon-flash\"></span> " + scope.dict.status.failure; 
                            element.append(chilToAppend);
                        }
                    }
                }
            })   
        }
    };
});