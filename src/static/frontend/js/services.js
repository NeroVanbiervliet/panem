panemApp.service('tokenManager', function($cookies, $http, $rootScope, $q) {
    // constant
    var expiryTime = 2*60*60*1000 - 5000; // 2 hours in milliseconds (minus 5000 to be sure)

    // to access this later
    var oldThis = this;

    // auxiliary function
    this.setToken = function(tokenToSet) {
        $cookies.put('panemToken',tokenToSet);
        this.resetTimer();
    };

    // auxiliary function
    this.resetTimer = function() {
        $cookies.put('panemTokenTimer',(new Date()).getTime());
    };

    // check if the token has expired
    this.isExpired = function() {
        var lastAccessed = $cookies.get('panemTokenTimer');
        var currentTime = (new Date()).getTime();
        return ((currentTime - lastAccessed) > expiryTime || lastAccessed == null);
    };

    // force new token
    this.forceNewToken = function() {
        var deferred = $q.defer();
        $cookies.remove('panemTokenTimer');
        this.getToken().then(function(newToken) {
            deferred.resolve(newToken);
        });
        return deferred.promise;
    };

    // getter for token
    this.getToken = function() {
        var deferred = $q.defer();

        if(this.isExpired())
        {
            this.generateGuestToken().then(function(generatedToken) {
                deferred.resolve(generatedToken);
            });
        }
        else
        {
            this.resetTimer();
            deferred.resolve($cookies.get('panemToken'));
        }

        // TODO deferred.reject() als het fout loopt en er geen token kan gemaakt worden?
        return deferred.promise;
    };

    this.generateGuestToken = function(generatedToken) {

        var deferred = $q.defer();

        var formData = $.param({
            json: JSON.stringify({
                email : "",
                password : ""
            })
        });

        $http.post($rootScope.baseUrl + '/token/create/',formData)
        .then(
            function(response){ // successful request to backend
                oldThis.setToken(response.data);
                // reset timer
                oldThis.resetTimer();
                // reset userInfo
                $cookies.put('panemUserInfo',JSON.stringify({lastName : "", firstName : ""}));
                // return token
                deferred.resolve(response.data);
            },
            function(response){ // failed request to backend
                console.log("backend request failed");
                deferred.reject('NOVALIDTOKEN');
            }
        );

        return deferred.promise;
    };
});

// stores user information
panemApp.service('userInfo', function($cookies, $rootScope, $http, tokenManager, $q) {
    // updates the user info based on the current token stored in the cookies

    this.emptyUserInfo = {lastName : "", firstName : ""};

    this.updateInfo = function() {
        var deferred = $q.defer();

        // get token
        tokenManager.getToken()
        .then(function (newToken) {
            // endpoint access
            $http({
                method : "GET",
                url : $rootScope.baseUrl + "/me/token=" + newToken
            }).then(function(response) {
                $cookies.put('panemUserInfo',JSON.stringify(response.data));
                deferred.resolve(response.data);
            }, function(response) {
                $cookies.put('panemUserInfo',JSON.stringify(this.emptyUserInfo));
                deferred.resolve(this.emptyUserInfo);
            });
        });

        return deferred.promise;
    }

    this.getInfo = function() {
        var deferred = $q.defer();
        try
        {
            deferred.resolve(JSON.parse(decodeURIComponent($cookies.get('panemUserInfo'))));
        }
        catch(error)
        {
            deferred.resolve(this.emptyUserInfo);
        }
        return deferred.promise;
    };

    this.clear = function() {
        $cookies.put('panemUserInfo',JSON.stringify(this.emptyUserInfo));
    };
});


// obtains GET parameters from url
panemApp.service('GETUrl', function($location) {
    this.valuesDict = {};

    this.decipher = function() {
        var url = $location.url();
        // variables start after ? sign
        if(url.indexOf("?") != -1) // contains a ?
        {
            url = url.split("?")[1]
            var dataSegments = url.split("&");

            for(var i=0; i<dataSegments.length; i++)
            {
                var segment = dataSegments[i];

                // add pair to valuesDict
                this.valuesDict[segment.split("=")[0]] = segment.split("=")[1];
            }
            return this.valuesDict;
        }
        else
        {
            return {};
        }

    };
});

// transforms a date in ms to a qualitative indication in the provided language
// e.g. english: yesterdag,today, tomorrow  dutch: gisteren,vandaag,morgen
// always first set IETF before calling any other function
panemApp.service('processDate', function(dictionary) {

    // set constants
    var ONE_DAY_MILLISECONDS = 24 * 60 * 60 * 1000;

    // setter for IETF language code
    this.setLang = function(lang) {
        this.lang = lang;

        // fill dictionary
        var dict = dictionary.fillServices(lang,"processDate");

        // load data from dictionary
        this.nextDayNames = dict.nextDayNames;
        this.qualitativeStrings = dict.qualitativePastTime;
        this.IETF = dict.IETF;
    };

    // default language
    this.setLang("nl");

    // auxiliary function that compares dates
    // if firstDate < secondDate, then the result will be positive
    function datesDayDifference(firstDateMs, secondDateMs) {
        // initiate moment to compare dates
        moment().format();

        // a duration asDays is still a float : e.g. 0.36 days. solution : convert dates to the start of their day, removing the time aspect
        return Math.round(moment.duration(moment(secondDateMs).startOf('day').diff(moment(firstDateMs).startOf('day'))).asDays());
    }

    // to access this later
    var oldThis = this;

    // get string indicating the date e.g. vrijdag 6 mei (morgen)
    // (morgen) only enabled if qualitative = true
    this.getWordDate = function(dateMs, qualitative) {
        var dateToProcess = new Date(dateMs);
        var options = { weekday: 'long', month: 'long', day: 'numeric' };
        var dateToDisplay = dateToProcess.toLocaleDateString(oldThis.IETF, options);

        // compare number of days between today and dateToṔrocess
        var diff = datesDayDifference((new Date()).getTime(),dateMs);
        if(diff >= -1 && diff <=2 && qualitative)
        {
            dateToDisplay += ' (' + oldThis.nextDayNames[diff.toString()] + ')';
        }
        return dateToDisplay;
    };

    // get string indicating how long ago the date is from today, given that daysElapsed is the number of days elapsed untill today
    // e.g. three weeks ago
    this.getTimePastIndication = function(daysElapsed) {

        var resultString;

        if(daysElapsed < 0) { // in the future
            resultString = this.qualitativeStrings['future'];
        }

        // in the past or today
        for(var i=0; i<Object.keys(this.qualitativeStrings).length; i++)
        {
            var limit = Object.keys(this.qualitativeStrings)[i];
            if(parseInt(daysElapsed) >= parseInt(limit))
            {
                resultString = this.qualitativeStrings[limit];
            }
            else
            {
                break;
            }
        }

        return resultString;
    }
});

// performs requests (post/get) to a given url, relative to the baseUrl
panemApp.service('requestWrapper', function($rootScope, $http, tokenManager, $q) {

    // initialises a requestStatus string
    this.init = function() {
        return 'working';
    };

    // performs a get request
    this.get = function(relUrl) {
        var deferred = $q.defer();

        tokenManager.getToken().then(function(newToken) {
            // add token to relative url
            var fullUrl = relUrl;
            if(relUrl.substr(relUrl.length-1) != '/') // check if last character of relUrl is a slash
            {
                fullUrl += '&'
            }
            fullUrl += 'token=' + newToken;

            // endpoint access
            $http({
                method : "GET",
                url : $rootScope.baseUrl + fullUrl
            }).then(function(response) {
                if (typeof(response.data) == 'object') { // data is returned
                    deferred.resolve(['success',response.data]);
                }
                else if (typeof(response.data) == 'string') {
                    if (response.data == 'tokennotexist') { // this should not happen in normal circumstances
                        $rootScope.requestStatus = 'error'; // so alert message in navbar will be displayed
                        deferred.resolve(['error-requestWrapper-tokenNotExist',{}]);
                    }
                    else if (response.data.split('-')[0] == 'success')
                        deferred.resolve([response.data,{}])
                    else // pass the error message on
                        deferred.resolve(['error-message-'+response.data,response.data]);
                }
                else {
                    // no string no object, fail
                    $rootScope.requestStatus = 'error'; // so alert message in navbar will be displayed
                    deferred.resolve(['error-requestWrapper-noObjectNorString',{}]);
                }
            }, function(response) {
                $rootScope.requestStatus = 'error'; // so alert message in navbar will be displayed
                deferred.resolve(['error-requestWrapper-requestFailed',{}]);
            });
        });

        return deferred.promise;
    };

    // performs a post request
    this.post = function(relUrl, data) {
        var deferred = $q.defer();

        tokenManager.getToken().then(function(newToken) {
            // add token to data
            data.token = newToken;

            var postData = $.param({
                json : JSON.stringify(data)
            });

            $http.post($rootScope.baseUrl + relUrl,postData)
            .then(function(response) {
                if (response.data == 'tokennotexist') { // this should not happen in normal circumstances
                    $rootScope.requestStatus = 'error'; // so alert message in navbar will be displayed
                    deferred.resolve('error-requestWrapper-tokenNotExist');
                }
                else if (response.data.split('-')[0] == 'success') {
                    deferred.resolve(response.data);
                }
                else { // pass the error message on
                    deferred.resolve('error-message-' + response.data);
                }
            }, function(response) {
                $rootScope.requestStatus = 'error'; // so alert message in navbar will be displayed
                deferred.resolve('error-requestWrapper-requestFailed');
            });
        });

        return deferred.promise;
    };
});
