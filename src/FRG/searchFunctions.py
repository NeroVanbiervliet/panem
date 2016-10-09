from FRG.databaseFunctions import getGpsFromAdress
from first.models import Bakery, Order, Logging
import geopy
from django.core.exceptions import ObjectDoesNotExist

# Returns all bakeries with some extra parameters especially for the search function
def get_bakery_search(GPSLon,GPSLat,accountId):

    try:
        output = []
        objects = Bakery.objects.all()
        for bakery in objects:
            tempDict = {}
            tempDict['name'] = bakery.name
            tempDict['id'] = bakery.id
            #tempDict['adress'] = bakery.adress
            tempDict['postcode'] = bakery.postcode
            tempDict['city'] = bakery.city
            tempDict['photoId'] = bakery.photoId
            #tempDict['member'] = bakery.member
            if abs(bakery.GPSLon) > 0.1 and abs(bakery.GPSLat) > 0.1:
                selfPosition = geopy.Point(GPSLon,GPSLat)
                bakeryPosition = geopy.Point(bakery.GPSLon,bakery.GPSLat)
                distance = geopy.distance.distance(selfPosition, bakeryPosition).km
            else:
                distance= -1

            tempDict['distance'] = distance
            tempDict['initScore'] = initScoreCalculator(accountId,bakery.id) # + user preferences
            output.append(tempDict)

    except ObjectDoesNotExist:
        output = 'NA'
    return output


def initScoreCalculator(accountId,bakeryId):

    ## Amount of orders
    amountOfOrders = len(Order.objects.filter(accountId__exact=int(accountId),bakeryId__exact=int(bakeryId)))

    ## Amount of visits
    amountOfVisits = len(Logging.objects.filter(accountId__exact=int(accountId),event_text__exact=str(bakeryId),kind__exact='visit'))

    initScore = amountOfOrders + amountOfVisits

    #TODO: filter

    return initScore


def get_bakery_search_postcode(postcode,accountId):

    searchString = str(postcode) + ' Belgie' # NEED werkt dit nog zonder de twee puntjes op de e?
    GPSLat,GPSLon = getGpsFromAdress(searchString)

    output = get_bakery_search(GPSLon,GPSLat,accountId)

    return output