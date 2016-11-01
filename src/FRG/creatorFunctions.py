from FRG.databaseFunctions import getGpsFromAdress
import FRG.mailHandler as mhl
import GDR.baert_to_split as bts
import GDR.basicFunctions as bsf
from first.models import Bakery, Account
from django.core.exceptions import ObjectDoesNotExist
from base64 import b64encode
import os
import hashlib
import random

def create_bakery(personInfo, bakeryInfo, sendMail):
    address = bakeryInfo['street'] + ' ' + str(bakeryInfo['postcode']) +' '+ bakeryInfo['city']
    GPSLat,GPSLon = getGpsFromAdress(address)

    #Check Of bakker al bestaat
    try:
        object = Bakery.objects.get(taxNumber=bakeryInfo['taxNumber']) # NEED slechte check, want 1 typfoutje leidt tot een nieuwe bakker
        output = 'bakeryalreadyexists'
    except ObjectDoesNotExist:
        #Account Maken

        accountOutput = create_account(personInfo['firstName'], personInfo['lastName'], personInfo['email'], 'baker', address, personInfo['password'], sendMail)

        # Bakker aanmaken
        if accountOutput == 'success':
            accountId = Account.objects.get(email = personInfo['email']).id
            website = ''
            if not 'openings' in bakeryInfo:
                bakeryInfo['openings'] = "[[{\"h\": \"5\", \"m\": \"15\"}, {\"h\": \"16\", \"m\": \"28\"}, true], [{\"h\": \"7\", \"m\": \"28\"}, {\"h\": \"18\", \"m\": \"16\"}, false], [{\"h\": \"7\", \"m\": \"32\"}, {\"h\": \"18\", \"m\": \"4\"}, false], [{\"h\": \"5\", \"m\": \"13\"}, {\"h\": \"16\", \"m\": \"40\"}, true], [{\"h\": \"5\", \"m\": \"26\"}, {\"h\": \"17\", \"m\": \"1\"}, true], [{\"h\": \"5\", \"m\": \"35\"}, {\"h\": \"18\", \"m\": \"8\"}, true], [{\"h\": \"5\", \"m\": \"28\"}, {\"h\": \"20\", \"m\": \"6\"}, true]]"
            description = 'lolololololololololololololololol'
            bestelLimitTime = '17:00'
            bakeryObject = bsf.add_bakery(bakeryInfo['name'],bakeryInfo['street'],int(bakeryInfo['postcode']),bakeryInfo['city'],GPSLat,GPSLon,bakeryInfo['telephone'],website,bakeryInfo['openings'],description,bestelLimitTime,bakeryInfo['bankAccount'],bakeryInfo['taxNumber'],1,accountId)
            output = 'success'
            #initialise standard products for bakery
            bts.initStandardProducts(bakeryObject)
        else:
            output = 'account' + accountOutput

    return output


def create_account(firstnameIn, lastnameIn, emailIn, typeIn, adressIn, password, sendMail):

    try:
        #check if the account does not already exists
        account = Account.objects.get(email = emailIn)
        return 'alreadyexists'
    except ObjectDoesNotExist:

        if len(password) < 7:
            return 'passwordtooshort'
        elif not password.isalnum():
            return 'notalphanumeric'
        else:
            if sendMail:
                # normal procedure
                salt = b64encode(os.urandom(64)).decode('utf-8')
                passwordSalted = password + salt
                hashed = hashlib.sha512(passwordSalted).hexdigest()
                confirmedNumber = random.randint(1,999999)
                mhl.sendVerifyMail(emailIn,confirmedNumber)
                bsf.add_account(firstnameIn, lastnameIn, emailIn, typeIn, adressIn, hashed, confirmedNumber,salt)
            else:
                # database testing procedure
                salt = b64encode(os.urandom(64)).decode('utf-8')
                passwordSalted = password + salt
                hashed = hashlib.sha512(passwordSalted).hexdigest()
                confirmedNumber = 0
                bsf.add_account(firstnameIn, lastnameIn, emailIn, typeIn, adressIn, hashed, confirmedNumber,salt)

            return 'success'