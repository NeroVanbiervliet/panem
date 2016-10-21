var panemApp = angular.module("panemApp", ['ngRoute','ngCookies']);

// WATCH OUT: /baker/.. and /client/... -> don't forget the leading slash

panemApp.config(['$routeProvider', function($routeProvider) {
   $routeProvider

   .when('/baker/allorders', {
      templateUrl: 'views/baker/allorders.html', controller: 'bkAllOrdersCtrl'
   })

   .when('/baker/dayorder', {
      templateUrl: 'views/baker/dayorder.html', controller: 'bkDayOrderCtrl'
   })

   .when('/baker/modifyproducts', {
      templateUrl: 'views/baker/modifyproducts.html', controller: 'bkModifyProductsCtrl'
   })

   .when('/baker/register', {
      templateUrl: 'views/baker/register.html', controller: 'bkRegisterCtrl'
   })

  .when('/baker/contact', {
       templateUrl: 'views/client/contact.html', controller: 'clContactCtrl'
   })

   .when('/baker/managebakery', {
       templateUrl: 'views/baker/managebakery.html', controller: 'bkManageBakeryCtrl'
   })

   .when('/client/bakery', {
      templateUrl: 'views/client/bakery.html', controller: 'clBakeryCtrl'
   })

   .when('/client/confirmorder', {
      templateUrl: 'views/client/confirmorder.html', controller: 'clConfirmOrderCtrl'
   })

   .when('/client/finalisepayment', {
       templateUrl: 'views/client/finalisepayment.html', controller: 'clFinalisePaymentCtrl'
    })

   .when('/client/home', {
      templateUrl: 'views/client/home.html', controller: 'clHomeCtrl'
   })

   .when('/client/register', {
       templateUrl: 'views/client/register.html', controller: 'clRegisterCtrl'
   })

   .when('/client/termsconditions', {
       templateUrl: 'views/client/termsconditions.html', controller: 'clTermsConditionsCtrl'
   })

   .when('/client/verifyaccount', {
       templateUrl: 'views/client/verifyaccount.html', controller: 'clVerifyAccountCtrl'
   })

   .when('/client/contact', {
       templateUrl: 'views/client/contact.html', controller: 'clContactCtrl'
   })

   .when('/client/contactsuccess', {
       templateUrl: 'views/client/contactsuccess.html', controller: 'clContactSuccess'
   })

   .when('/client/login', {
       templateUrl: 'views/client/login.html', controller: 'clLoginCtrl'
   })

   .when('/client/forgotpassword', {
       templateUrl: 'views/client/forgotpassword.html', controller: 'clForgotPasswordCtrl'
   })

   .when('/client/resetpassword', {
       templateUrl: 'views/client/resetpassword.html', controller: 'clResetPasswordCtrl'
   })

   .when('/client/myaccount',{
       templateUrl: 'views/client/myaccount.html', controller: 'clMyAccountCtrl'
   })

   .when('/client/topupcredit', {
       templateUrl: 'views/client/topupcredit.html', controller: 'clTopUpCreditCtrl'
   })

   .otherwise({
      redirectTo: '/client/home'
   });

}]);

panemApp.run(function(userInfo, $rootScope, $location, tokenManager, dictionary, $window) {
    $rootScope.baseUrl = 'http://146.185.179.39:8000';
    $rootScope.defaultTitle = 'Panem - bestel uw brood online';

    // load navbar js
    loadNavBarLogic(userInfo, $rootScope, $location, tokenManager, dictionary, $window);
});
