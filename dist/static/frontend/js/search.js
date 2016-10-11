function updateQueryScores(scope, reset) { // TODO te lage scores truncaten naar zero want die betekenen toch niets
    
    // split search query by spaces
    var searchSplit = scope.searchInput.split(" ");
    
    // number of words in the query
    var numWords = searchSplit.length; 
    
    // set scores of words with index > numWords to zero, or all scores if reset is true
    var resetLimit = numWords;
    if (reset)
    {
        resetLimit = 0;
        scope.locationOverrule = false;
    }
    for(var j=0; j<scope.pyBakeries.length; j++)
    {
        for(var i = resetLimit; i<scope.pyBakeries[j].queryScores.length; i++)
        {
            scope.pyBakeries[j].queryScores[i] = 0;
        }
    }
    
    // recalculate score for the last word, or for all words if reset is true
    for(var j=numWords-1; j>Math.max(resetLimit-2,-1); j--)
    {
        // get word of query
        var word = searchSplit[j];
        
        // determine the type of data for the last word: number or text
        // determine score for the last word
        if(!isNaN(parseFloat(word))) // NUMBER
        {    
            // loop over bakeries
            for(var i=0; i<scope.pyBakeries.length; i++)
            {
                var bakery = scope.pyBakeries[i];
                bakery.queryScores[numWords-1] = stringCorrelation(bakery.postcode.toString(),word);
            }   
            
            scope.locationOverrule = true;
        }
        else // TEXT
        {
            // strip characters from string
            word = word.replace(/[',&]/g,'');

            // loop over bakeries
            for(var i=0; i<scope.pyBakeries.length; i++)
            {
                var bakery = scope.pyBakeries[i];

                // TODO die replaces kunnen eenmalig vooraf gebeuren om sneller te zijn
                // note : weinig mee te winnen, kijken in chrome profiler waar bottlenecks zitten als je wil optimisen
                // let op! wel niet de originele data overwriten
                var nameScore = stringCorrelation(bakery.name.replace(/[',&]/g,''),word);
                var cityScore = stringCorrelation(bakery.city.replace(/[',&]/g,''),word);
                bakery.queryScores[numWords-1] = Math.max(nameScore,cityScore);      
            }   
        }
    } 
}

function updateTotalScore(pyBakeries, locationOverrule) {
    for(var i=0; i<pyBakeries.length; i++)
    {
        var bakery = pyBakeries[i];
        bakery.totalScore = bakery.initScore;
        
        if(!locationOverrule)
        {
            bakery.totalScore += bakery.distanceScore; 
        }
        
        for(var j=0; j<bakery.queryScores.length; j++) // TODO lengte kan 1x berekend worden ipv elke keer weer
        {
            bakery.totalScore += bakery.queryScores[j];
        }
    }
}

// initialise queryScores
function initSearch(scope) {    
    
    for(var i=0; i<scope.pyBakeries.length; i++)
    {
        var bakery = scope.pyBakeries[i];
        
        // assign distanceScore
        if(bakery.distance != -1)
        {
            bakery.distanceScore = Math.max(Math.round(200-bakery.distance),0)/40;
        }
        else
        {
            bakery.distanceScore = 0; 
        }
        
        // initialise queryScores
        bakery.queryScores = [];
    }
}

function stringCorrelation (completeWord,toMatch) {
    var lToMatch = toMatch.length;
    var lCompleteWord = completeWord.length;
    
    // TODO verplaatsen naar preprocessing voor speed
    completeWord = completeWord.toLowerCase();
    toMatch = toMatch.toLowerCase();
    
    if(lToMatch-2 > lCompleteWord)
    {
        // search query to large, no match
        return 0; 
    }
    else
    {
        var maxScore = 0; 
        var currentScore; 
        
        // shifts the toMatch string while calculating at each shift a new score
        for(var i=-1; i<lCompleteWord+1; i++)
        {
            currentScore = 0; 
            
            // loop over all characters in toMatch
            for(var j=0; j<lToMatch; j++)
            {
                if(completeWord.charAt(i+j) == toMatch.charAt(j))
                {
                    currentScore++;
                    // console.log("letter = " + completeWord.charAt(i+j) + " ++");
                    
                    if(j<2) // bonus voor als de match in het begin van het woord is
                    {
                        currentScore += 3; 
                    }
                }
            }
            
            maxScore = Math.max(currentScore,maxScore);
        }
        
        return maxScore; 
    }
}