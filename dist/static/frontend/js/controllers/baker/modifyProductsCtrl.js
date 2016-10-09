panemApp.controller('bkModifyProductsCtrl', function($scope, $rootScope, dictionary, tokenManager, $http) {

    // VARIABLES
    $scope.pyCategories;
    $scope.pyBakeryInfo; 
    $scope.deleteList = [];
    
    $scope.bakeryId = 151; // NEED dynamisch
    
    // define constants
    $scope.DEFAULT_PRODUCT_IMAGE_SOURCE = "images/default_products/"; // NEED veranderen
    $scope.PRODUCT_IMAGE_EXTENSION = ".png";
    
	// Initialize dictionary
	$scope.dict = dictionary.fillBkModifyProducts("nl"); // NEED vervangen

    // FUNCTIONS 
    
    // show category of items
    $scope.showCategory = function (catIndex) {
        $scope.productCategory = $scope.pyCategories[catIndex];
    }
    
    // get pyCategories and pyProducts
    var loadProducts = function (token){
        $http({
            method : "GET",
            url : $rootScope.baseUrl + "/bakery/" + $scope.bakeryId + "/products/categories/token=" + token
        }).then(function(response) {
            $scope.pyCategories = response.data;
            // show 0th category
            $scope.showCategory(0);
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
            decodeOpeningHours();
            
        }, function(response) {
            $scope.pyBakeryInfo = {};
            // TODO dit geeft een slechte pagina
        });
    }
    
    // load data when token is available
    tokenManager.getToken().then(function(newToken) {
        $scope.token = newToken; 
        // access endpoints
        loadBakeryInfo(newToken);
        loadProducts(newToken);
    });
    
    // adds a new product to a category
    $scope.addProduct = function(category) {
        var newProduct = {
            "id" : "-1", 
            "name" : "",
            "fotoId" : 1, // NEED moet categorie default foto zijn
            "available" : true,
            "price" : 160,
            "ingredientsString" : ""
        }
        category.products.push(newProduct);
    };
    
    // remove a product from a category
    $scope.removeProduct = function(category,index) {
        // remove item from products array in its category
        var removedProduct = category.products.splice(index,1)[0]; // assings and modifies source array at the same time, [0] because return value is an array with the one item
        
        // add product id to delteList
        $scope.deleteList.push(removedProduct.id);
    };
    
    // decodes backend opening hours to array
    function decodeOpeningHours() {
        $scope.pyBakeryInfo.openingHours = JSON.parse($scope.pyBakeryInfo.openingHours); 
    }
    
    // save bakeryInfo to backend
    function saveBakeryInfo(token) {
        // NEED
    }
    
    // save products to backend 
    function savePyCategories(newToken) {
        // prepare data
        var requestData = $.param({
            json: JSON.stringify({
                token : newToken,
                productUpdate : $scope.pyCategories,
                bakeryId : 151, // NEED aanpassen
                deleteList : $scope.deleteList
            })
        });
        
        console.log(requestData);
        
        // perform endpoint request
        $http.post($rootScope.baseUrl + '/bakery/adaptProducts/',requestData)
        .then(
            function(response){ // successful request to backend
                $scope.requestStatus = response.data; 
                // NEED nog verwerken, mss fout in token of zo? 
            }, 
            function(response){ // failed request to backend
                $scope.requestStatus = "backenderror"; 
                alert('error');
                // NEED notify user that something whent wrong
            }
        );
    }
    
    // save all data to backend
    $scope.saveAllData = function() {
        tokenManager.getToken().then(function(newToken) {
            saveBakeryInfo(newToken);
            savePyCategories(newToken); 
        });
    };
});
