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
            // first initialisation
            $(element).tagsinput({
                  tagClass: function(item) {
                      return 'label label-default'; // gray
                  }
                }
            );
            $(element).parent().addClass("cursor-not-allowed-all-children");
            
            // add ingredient tags
            $(element).tagsinput('add', scope.product.ingredientsString);
            
            // watch for changes in checked state
            scope.$watch("product.available",function(newValue,oldValue) {
                var isDisabled; 
                if(newValue == null || newValue == false) // product not selected
                {
                    isDisabled = true; 
                    $(element).parent().addClass("cursor-not-allowed-all-children");
                }
                else
                {
                    isDisabled = false; 
                    $(element).parent().removeClass("cursor-not-allowed-all-children");
                }
                // initialisation of tagsinput element
                $(element).tagsinput('destroy');
                $(element).tagsinput({
                      tagClass: function(item) {
                        switch (isDisabled) {
                          case false : return 'label label-primary'; // blue
                          case true  : return 'label label-default'; // gray
                        }
                      }
                    }
                );
            });
            
            // watch for added item
            $(element).on('itemAdded', function(event) {
                // store new ingredients string
                scope.product.ingredientsString = $(element).val();
            });
        }
    };
});

// tags input used to show allergies
panemApp.directive('toggle', function() {
    return {        
        link: function (scope, element, attrs) {   
            if($(element).data('toggle') == 'toggle') // activate only if data-toggle="toggle"
            {
                // initialisation
                $(element).bootstrapToggle({
                  on: 'I', //'<span class=\"glyphicon glyphicon-ok\"></span>',
                  off: 'O', //'<span class=\"glyphicon glyphicon-remove\"></span>'
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
        }
    };
});