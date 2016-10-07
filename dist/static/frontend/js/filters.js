panemApp.filter('moneyFilter', function() {
    return function(input) {
        var priceInCents = parseInt(input);
        if(priceInCents%100 == 0) // don't display the comma
        {
            return Math.floor(priceInCents/100);
        }
        else if(priceInCents%100 <10) // add a leading zero to the part after the comma
        {
            return Math.floor(priceInCents/100) + ',0' + priceInCents%100;
        }
        else
        {
            return Math.floor(priceInCents/100) + ',' + priceInCents%100;
        }
    };
});