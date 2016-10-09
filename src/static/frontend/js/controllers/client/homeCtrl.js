panemApp.controller('clHomeCtrl', function($scope, dictionary, $http, $rootScope, tokenManager, $q, $location) {
    
	// variables
    $scope.lastQuerySplit = []; 
    $scope.locationOverrule = false;
    // default value is very far from belgium => geolocation does not contribute to score
    $scope.geoLocation = { 
        'lon' : 179.1,
        'lat' : 89.1
    };
    
    // contants
    $scope.IMAGE_SOURCE = "images/shops/800x500/"; 
    $scope.IMAGE_EXTENSION = ".png";
    
    // Initialize dictionary
	$scope.dict = dictionary.fillClHome("nl");
 
    // load bakeries data from backend 
    $scope.getPyBakeries = function(token) {
        $http({
            method : "GET",
            url : $rootScope.baseUrl + "/bakery/search/GPSLon=" + $scope.geoLocation.lon + "&GPSLat=" + $scope.geoLocation.lat + "&token=" + token
        }).then(function(response) {
            $scope.pyBakeries = response.data;

            // function from search.js
            initSearch($scope);
            updateTotalScore($scope.pyBakeries,$scope.locationOverrule);

        }, function(response) {
            $scope.pyBakeries = [];
            // TODO message tonen dat er iets fout gelopen is als pyBakeries leeg is
        });
    }
    
    // loads the bakery data
    loadData = function(token) {
        // first load the data without geoLocation knowledge
        $scope.getPyBakeries(token);

        // attempt to obtain geolocation data
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition( function(position) {
                $scope.geoLocation = {
                    'lon' : position.coords.longitude,
                    'lat' : position.coords.latitude
                };
                $scope.getPyBakeries(token);
            });
        } 
    } 
    
    // get geolocation as soon as token is available
    tokenManager.getToken().then(function(newToken) {
        loadData(newToken); 
    });
    
    // executed on ng-change of search input field
    $scope.updateSearchResults = function () {        
        var suspiciousChangeDetected = false; 
        var searchInputSplit = $scope.searchInput.split(" ");
        for(var i=0; i<searchInputSplit-1; i++)
        {
            if($scope.lastQuerySplit[i] != searchInputSplit[i])
            {
                suspiciousChangeDetected = true;
                break;
            }
        }
        
        if ($scope.lastQuerySplit.length > searchInputSplit.length) suspiciousChangeDetected = true; // there is a word less in the query
        
        $scope.lastQuerySplit = $scope.searchInput.split(" ");
        
        if(suspiciousChangeDetected)
        {
            // function from search.js
            updateQueryScores($scope,true);
        }
        else
        {
            // function from search.js
            updateQueryScores($scope,false);
        }
        
        // function from search.js
        updateTotalScore($scope.pyBakeries,$scope.locationOverrule);
    };
    
    // focus on search input element
    document.getElementById('searchInput').focus();
  
});