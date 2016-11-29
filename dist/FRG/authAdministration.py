from GDR.basicFunctions import add_token
from first.models import Account, Token, Bakery
from django.core.exceptions import ObjectDoesNotExist
import hashlib
from base64 import b64encode
import os
import random
import string
import datetime


def check_login(emailIn,password):
    #check if account does exist
    try:
        account = Account.objects.get(email = emailIn)
        salt = account.salt
        passwordSalted = password + salt
        if account.password == hashlib.sha512(passwordSalted).hexdigest():
            return 'success'
        else:
            return 'wrongpassword'

    except ObjectDoesNotExist:
        return 'accnotfound'


def change_password(emailIn,passwordOriginal,passwordNew):
    #check if account exists
    #send mail if password is reset?
    if len(passwordNew) < 7 or not passwordNew.isalnum():
        return 'requirements-not-met'
    else:
        try:
            account = Account.objects.get(email = emailIn)
            salt = account.salt
            passwordSalted = passwordOriginal + salt
            if account.password == hashlib.sha512(passwordSalted).hexdigest(): # given password is correct
                salt = b64encode(os.urandom(64)).decode('utf-8')
                passwordSalted = passwordNew + salt
                hashed = hashlib.sha512(passwordSalted).hexdigest()
                account.password = hashed
                account.salt = salt
                account.save()
                return 'success'
            else:
                return 'wrong-password'

        except ObjectDoesNotExist:
            return 'accnotfound'


def resetPasswordSet(code,accountId, passwordNew):
    try:
        account = Account.objects.get(id = accountId)
        if account.password == code:
            return storeNewPassword(accountId,passwordNew)

        else:
            return 'wrongcode'

    except ObjectDoesNotExist:
        return 'accnotfound'


def resetPassword(emailIn,token):
    #check if account exists
    #send mail if password is reset?
    try:
        account = Account.objects.get(email = emailIn)
        name = account.firstname
        code = random.randint(10**5,10**7)
        account.password = code
        link = 'localhost:9000/#/client/resetpassword?code=' + str(code) + '&token=' + token + '/' # NEED: zorg dat link goed is
        resetPasswordSendMail(emailIn,name,link)

        account.save()
        return 'success'

    except ObjectDoesNotExist:
        return 'accnotfound'


def storeNewPassword(accountId,passwordNew):
    if len(passwordNew) < 7:
        return 'passwordtooshort'
    elif not passwordNew.isalnum():
        return 'notalphanumeric'
    else:
        try:
            account = Account.objects.get(id = accountId)
            salt = b64encode(os.urandom(64)).decode('utf-8')
            passwordSalted = passwordNew + salt
            hashed = hashlib.sha512(passwordSalted).hexdigest()
            account.password = hashed
            account.salt = salt
            account.save()
            return 'success'

        except ObjectDoesNotExist:
            return 'accnotfound'


def verify_account(emailIn,code):
    #check if account exists
    try:
        account = Account.objects.get(email = emailIn)
        if account.confirmed == 0:
            return 'already-verified'
        elif int(code) == account.confirmed:
            #if confirmed value is zero, then the account is confirmed
            account.confirmed = 0
            account.save()

            # create login token
            valueIn = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(14))
            accountId = account.id
            expiry = datetime.datetime.now() + datetime.timedelta(hours=2)
            add_token(valueIn,accountId,expiry)
            return valueIn
        else:
            return 'wrong-code'

    except ObjectDoesNotExist:
        return 'acc-not-found'


def createToken(emailIn,password):
    if emailIn == '':
        valueIn = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(14))
        expiry = datetime.datetime.now() + datetime.timedelta(hours=2)
        add_token(valueIn,0,expiry)
        output = valueIn

    else:
        try:
            a = Account.objects.get(email = emailIn)

            state = check_login(emailIn,password)
            if state == 'success':
                valueIn = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(14))
                accountId = a.id
                expiry = datetime.datetime.now() + datetime.timedelta(hours=2)
                add_token(valueIn,accountId,expiry)
                output = valueIn
            else:
                output = 'wrongpassword'

        except ObjectDoesNotExist:
            output = 'accnotfound'

    return output


def verifyToken(token):

    try:
        a = Token.objects.get(value=token)
        if a.expiry > datetime.datetime.now():
            output = a.accountId
            a.expiry = datetime.datetime.now() + datetime.timedelta(hours=2)
            a.save()

        else:
            output = 'tokenexpired'

    except ObjectDoesNotExist:
        output = 'tokennotexist'

    return output


def token2account(accountId):
    try:
        output = {}
        account = Account.objects.get(id = accountId)
        output['firstName'] = account.firstname
        output['lastName'] = account.lastname
        output['email'] = account.email
        output['adress'] = account.adress
        output['type'] = account.type
        output['id'] = account.id
        output['credit'] = account.credit
        if account.type == 'baker':
            # check what baker has this account id registered
            resultList = Bakery.objects.filter(bakerAccountId=account.id)
            bakery = resultList[0] # there should only be one
            output['bakery'] = {}
            output['bakery']['name'] = bakery.name
            output['bakery']['id'] = bakery.id

    except ObjectDoesNotExist:
        output = 'accnotfound'


    return output