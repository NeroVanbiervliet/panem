loadNavBarLogic = function(userInfo, $rootScope, $location, tokenManager, dictionary, $window) {

    // NOTE : if you add an argument in this function, dont forget to add it also twice in the config file, where this function is called

    // EXECUTED ON REFRESH

    // create button navigation function
    $rootScope.navigate = function (url) {
        $window.location.href = url;
    };

    // initialize dictionary
	$rootScope.dict =  dictionary.fillNavbar("nl");

    // load user data if available
    userInfo.getInfo().then(function (loadedInfo) {
        $rootScope.userInfo =  loadedInfo;
        // boolean indicating what buttons to show in top right of navbar (log in / <name>)
        $rootScope.loggedIn = ($rootScope.userInfo.lastName != "") ? true:false;
    });

    // provide logout function TODO logout backend functie om token te vernietigen en meteen ook nieuwe guest token terug te krijgen?
    $rootScope.logout = function() {
        $rootScope.loggedIn = false;

        // clear user info in cookie and angular variable
        userInfo.clear();
        userInfo.getInfo().then(function (loadedInfo) {
            $rootScope.userInfo =  loadedInfo;
        });

        // get guest token
        tokenManager.forceNewToken().then(function(newToken) {
            $rootScope.token = newToken;
        });

        // redirect to home
        $window.location = '#/client/home/';
    };

    // EXECUTED ON ROUTE CHANGE AND ON REFRESH
    $rootScope.$on("$routeChangeSuccess", function($currentRoute, $previousRoute) {
        // used to redirect to the source page after successful log in on login page
        $rootScope.urlPath = $location.absUrl().split("#")[1];
    });

    // routing
    // cannot use navigate(someUrl) when the url contains ?somevar, the back function will then be broken
    $rootScope.changeUrl= function(targetUrl) {
        $location.url(targetUrl);
    };
};
