import smtplib
from email.mime.text import MIMEText

# NEED wordt niet gebruikt in project
from first.models import Account


def resetPasswordSendMail(email,name,code):

    msg = "Hallo " + name +", klik op deze link om uw wachtwoord te resetten: " + str(code)
    me = 'help@panem.be'
    you = email
    subject = 'Reset Password'

    sendMail(me,you,subject,msg)

    return code


def sendVerifyMail(receiverEmail,code):

    # relative from manage.py
    f = open('email_templates/registration.html','r')
    html = f.read()
    html = html.replace('(code_input)',str(code))
    html = html.replace('(email_input)',str(receiverEmail))
    f.close()

    me = 'help@panem.be'
    you = receiverEmail
    subject = 'Verify Code'

    sendMail(me,you,subject,html)

    return code

# sends an email using the sendgrid API
def sendMail(senderEmail, receiverEmail, subject, contentHtml):

    msg = MIMEText(contentHtml, 'html')
    me = senderEmail
    you = receiverEmail

    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    s = smtplib.SMTP_SSL('smtp.sendgrid.net', 465, timeout=10)
    s.set_debuglevel(0)
    s.login('panem_python','rosbeiaard1')
    s.sendmail(me, [you], msg.as_string())
    s.quit()

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