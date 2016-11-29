var CHAR_COUNT_WEIGHT = 0.5; 

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
        scope.pyBakeries[j].queryScoreType = [];
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
                bakery.queryScoreType[numWords-1] = 'number';
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
                var nameScore = stringCorrelation(bakery.name.replace(/[',&]/g,''),word) + CHAR_COUNT_WEIGHT*charCount(bakery.name.replace(/[',&]/g,''),word);
                var cityScore = stringCorrelation(bakery.city.replace(/[',&]/g,''),word) + CHAR_COUNT_WEIGHT*charCount(bakery.city.replace(/[',&]/g,''),word);;
                bakery.queryScores[numWords-1] = Math.max(nameScore,cityScore);
                if(nameScore > cityScore)
                    bakery.queryScoreType[numWords-1] = 'name';
                else
                    bakery.queryScoreType[numWords-1] = 'city';
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
            bakery.distanceScore = Math.max(Math.round(200-bakery.distance),0)/80;
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
        var bonusScore = 1;

        // shifts the toMatch string while calculating at each shift a new score
        for(var i=-1; i<lCompleteWord+1; i++)
        {
            currentScore = 0;

            //console.log('----- shift ' + i.toString());

            // loop over all characters in toMatch
            for(var j=0; j<lToMatch; j++)
            {

                if(completeWord.charAt(i+j) == toMatch.charAt(j))
                {
                    currentScore++;
                    // console.log("letter = " + completeWord.charAt(i+j) + " ++");

                    if(j<2) // bonus voor als de match in het begin van het woord is
                    {
                        currentScore += bonusScore;
                    }

                    //console.log('char ' + toMatch.charAt(j));
                }
            }

            //console.log('curscore = ' + currentScore);
            maxScore = Math.max(currentScore,maxScore);
        }

        // if the score is very low, it wil rather be by accident than a real match
        if (maxScore < (1+bonusScore))
            maxScore = 0;

        return maxScore;
    }
}

// counts the number of the same characters in two string, indifferent of the order
function charCount(sOne, sTwo) {
    sOneList = {}
    for(var i=0; i<sOne.length; i++) {
        var curChar = sOne[i];
        if (sOneList[curChar] != undefined)
            sOneList[curChar] = sOneList[curChar] +1;
        else
            sOneList[curChar] = 1;
    }

    var score = 0;
    for(var i=0; i<sTwo.length; i++) {
        var curChar = sTwo[i];
        if (sOneList[curChar] != undefined && sOneList[curChar] != 0) {
            sOneList[curChar] = sOneList[curChar] - 1;
            score++;
        }
    }

    return score;
}
