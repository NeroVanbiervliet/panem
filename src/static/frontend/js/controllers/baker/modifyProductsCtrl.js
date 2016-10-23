panemApp.controller('bkModifyProductsCtrl', function($scope, $rootScope, dictionary, tokenManager, $http, $window, requestWrapper, $q) {

    // VARIABLES
    $scope.pyCategories;
    $scope.pyBakeryInfo;
    $scope.pyIngredients;
    $scope.bloodhound;
    $scope.deleteList = [];
    $scope.pyNewIngredients = [];

    $scope.requestStatus = {
        'updateBakery' : 'init',
        'adaptProducts' : 'init'
    };
    $scope.bakeryId = $scope.userInfo.bakery.id;

    // define constants
    $scope.PRODUCT_IMAGE_SOURCE = 'images/products/50/';
    $scope.PRODUCT_IMAGE_EXTENSION = '.png';

	// Initialize dictionary
	$scope.dict = dictionary.fillBkModifyProducts("nl");

    // FUNCTIONS

    // show category of items
    $scope.showCategory = function (catIndex) {
        $scope.productCategory = $scope.pyCategories[catIndex];
    }

    // get pyCategories
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

    // get pyIngredients
    loadIngredients = function() {
        var deferred = $q.defer();

        $scope.requestStatus.loadIngredients = requestWrapper.init();
        url = '/bakery/' + $scope.bakeryId + '/ingredients/';
        requestWrapper.get(url).then(function ([newStatus,resultData]) {
            $scope.requestStatus.loadIngredients = newStatus;

            // TODO code kan netter, geen herhaling

            // process resultData
            $scope.pyIngredients = {'standard' : [], 'custom' : []};
            for(var i=0; i<resultData.standard.length; i++) {
                $scope.pyIngredients.standard.push({'name' : resultData.standard[i].name, 'id' : resultData.standard[i].id, 'type' : 'standard'});
            }
            for(var i=0; i<resultData.custom.length; i++) {
                $scope.pyIngredients.custom.push({'name' : resultData.custom[i].name, 'id' : resultData.custom[i].id, 'type' : 'custom'});
            }

            $scope.bloodhound = {'standard' : {}, 'custom' : {}};

            // create bloodhound for standard products
            $scope.bloodhound.standard = new Bloodhound({
                datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                local : $scope.pyIngredients.standard
            });
            $scope.bloodhound.standard.initialize();

            // create bloodhound for custom products
            $scope.bloodhound.custom = new Bloodhound({
                datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                local : $scope.pyIngredients.custom
            });
            $scope.bloodhound.custom.initialize();

            deferred.resolve();
        });

        return deferred.promise;
    }

    // load data when token is available
    tokenManager.getToken().then(function(newToken) {
        $scope.token = newToken;
        // access endpoints
        loadIngredients().then(function() {
            loadBakeryInfo(newToken);
            loadProducts(newToken);
        });
    });

    // adds a new product to a category
    $scope.addProduct = function(category) {
        var newProduct = {
            "id" : "-1",
            "name" : "",
            "photoId" : category.defaultPhotoId,
            "available" : true,
            "price" : 160,
            "ingredients" : [],
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

        // convert opening hours to a string
        $scope.pyBakeryInfo.openingHoursString = JSON.stringify($scope.pyBakeryInfo.openingHours);

        // prepare data
        var requestData = $.param({
            json: JSON.stringify({
                token : token,
                bakeryInfo : $scope.pyBakeryInfo
            })
        });

        // perform endpoint request
        $http.post($rootScope.baseUrl + '/bakery/update/',requestData)
        .then(
            function(response){ // successful request to backend
                $scope.requestStatus.updateBakery = response.data;
            },
            function(response){ // failed request to backend
                $scope.requestStatus.updateBakery = "backenderror";
                alert('error');
            }
        );
    }

    // save products to backend
    function savePyCategories(newToken) {
        // prepare data
        var requestData = $.param({
            json: JSON.stringify({
                token : newToken,
                productUpdate : $scope.pyCategories,
                bakeryId : $scope.bakeryId,
                deleteList : $scope.deleteList
            })
        });

        // perform endpoint request
        $http.post($rootScope.baseUrl + '/bakery/adaptProducts/',requestData)
        .then(
            function(response){ // successful request to backend
                $scope.requestStatus.adaptProducts = response.data;
            },
            function(response){ // failed request to backend
                $scope.requestStatus.adaptProducts = "backenderror";
            }
        );
    }

    // save all data to backend
    $scope.saveAllData = function() {
        $scope.requestStatus.updateBakery = 'working';
        $scope.requestStatus.adaptProducts = 'working';
        tokenManager.getToken().then(function(newToken) {
            saveBakeryInfo(newToken);
            savePyCategories(newToken);
        });
    };
});
