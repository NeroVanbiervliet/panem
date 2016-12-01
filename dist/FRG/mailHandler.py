import smtplib
from email.mime.text import MIMEText
import requests

SERVER_ADDRESS = 'http://95.85.20.119'

# NEED wordt niet gebruikt in project
from first.models import Account


def resetPasswordSendMail(email,name,code):

    msg = "Hallo " + name +", klik op deze link om uw wachtwoord te resetten: " + str(code)
    you = email
    subject = 'Reset Password'

    sendMail(you,subject,msg,msg)

    return code


def sendVerifyMail(destinationMail,code):

    # relative from manage.py
    f = open('email_templates/registration.html','r')
    html = f.read()
    html = html.replace('(code_input)',str(code))
    html = html.replace('(email_input)',str(destinationMail))
    f.close()

    text = 'Gelieve de volgende link te openen in uw browser: ' + SERVER_ADDRESS + '/#/client/verifyaccount?code=%s&email=%s' % (code,destinationMail)
    subject = 'Welkom bij Panem!'


    sendMail(destinationMail,subject,text,html)

    return code

# sends an email using the mailgun API
def sendMail(destinationEmail, subject, contentText, contentHtml):

    request = requests.post(
        "https://api.mailgun.net/v3/panem.be/messages",
        auth=("api", "key-2a2676fbda0ce7bc2aedd5824e341168"),
        data={"from": "Panem Help <help@panem.be>",
              "to": [destinationEmail],
              "subject": subject,
              "text": contentText,
              "html": contentHtml})

    # TODO check of request.status_code == 200 (OK)

    return "done"


def repeatVerifyMail(emailIn,token):

    try:
        account = Account.objects.get(email = emailIn)
        if account.confirmed == 0:
            return 'alreadyverified'
        else:
            name = account.firstname
            code = account.confirmed
            sendVerifyMail(emailIn,code)

            return 'success'

    except ObjectDoesNotExist:
        return 'accountnotfound'

# NEED wordt nergens gebruikt
def forgot_password(email):

    #Email with link to page where one can choose a new password

    return 0