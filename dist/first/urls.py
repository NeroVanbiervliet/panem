from django.conf.urls import url

from . import views

# why name='' is important : http://stackoverflow.com/questions/12818377/django-name-parameter-in-urlpatterns
urlpatterns = [
    url(r'^bakery/(?P<bakeryId>[0-9]+)/token=(?P<token>[A-Za-z0-9.-]+)/$', views.bakery, name='bakery'), #GET working
    url(r'^bakery/token=(?P<token>[A-Za-z0-9.-]+)/$', views.allBakeries, name='allBakeries'), #GET working
    url(r'^bakery/search/GPSLon=(?P<GPSLon>\d+\.\d+)&GPSLat=(?P<GPSLat>\d+\.\d+)&token=(?P<token>[A-Za-z0-9.-]+)/$', views.bakerySearch, name='bakerySearch'), #GET working
    url(r'^bakery/search/postcode=(?P<postcode>[0-9]+)&token=(?P<token>[A-Za-z0-9.-]+)/$', views.bakerySearchPostcode, name='bakerySearchPostcode'), #working GET
    url(r'^bakery/(?P<bakeryId>[0-9]+)/offer/token=(?P<token>[A-Za-z0-9.-]+)/$', views.bakeryOffer, name='bakeryOffer'), #GET working
    url(r'^bakery/(?P<bakeryId>[0-9]+)/products/token=(?P<token>[A-Za-z0-9.-]+)/$', views.bakeryProducts, name='bakeryProducts'), #GET working
    url(r'^bakery/(?P<bakeryId>[0-9]+)/products/categories/token=(?P<token>[A-Za-z0-9.-]+)/$', views.bakeryProductsCategories, name='bakeryProductsCategories'), #GET working
    url(r'^bakery/(?P<bakeryId>[0-9]+)/allDayOrders/firstDay=(?P<firstDay>[0-9]+)&lastDay=(?P<lastDay>[0-9]+)&token=(?P<token>[A-Za-z0-9.-]+)/$', views.allDayOrders, name='allDayOrders'), #GET
    url(r'^bakery/(?P<bakeryId>[0-9]+)/dayOrder/date=(?P<date>[0-9]+)&token=(?P<token>[A-Za-z0-9.-]+)/$', views.dayOrder, name='dayOrder'), #GET working
    url(r'^bakery/(?P<bakeryId>[0-9]+)/ingredients/token=(?P<token>[A-Za-z0-9.-]+)/$', views.getIngredients, name='ingredientsGet'), #GET working
    url(r'^bakery/(?P<bakeryId>[0-9]+)/ingredients/$', views.insertIngredients, name='ingredientsInsert'), # POST
    url(r'^bakery/create/$', views.createBakery, name='createBakery'), # POST
    url(r'^bakery/update/$', views.adaptBakery, name='adaptBakery'), # POST
    url(r'^bakery/update/emailnotifications/$', views.updateEmailNotifications, name='updateEmailNotifications'), # POST
    url(r'^bakery/adaptProducts/$', views.adaptProducts, name='adaptProducts'), # POST NEED dit moet komen onder baker/id/products/categories/update of zo
    url(r'^bakery/disableDates/$', views.disableDates, name='disableDates'), # POST 
    url(r'^account/create/$', views.createAccount, name='createAccount'), #POST working
    url(r'^account/verify/$', views.verifyAccount, name='verifyAccount'), #POST
    url(r'^account/verify/resendmail/email=(?P<emailIn>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})&token=(?P<token>[A-Za-z0-9.-]+)/$', views.repeatVerifyMail, name='repeatVerifyMail'), #GET working
    url(r'^account/password/change/$', views.changePassword, name='changePassword'), #POST working
    url(r'^account/password/reset/mail/$', views.resetPasswordMail, name='resetPasswordMail'), #POST working
    url(r'^account/password/reset/set/$', views.resetPasswordSet, name='resetPasswordSet'), #POST
    url(r'^order/current/token=(?P<token>[A-Za-z0-9.-]+)/$', views.currentOrderGet, name='currentOrderGet'), #GET working
    url(r'^order/current/$', views.currentOrderPost, name='currentOrderPost'), #POST 
    url(r'^order/current/bill/cash/extraCredit=(?P<extraCredit>[0-9]+)&skin=(?P<skin>[A-Za-z0-9.-]+)&token=(?P<token>[A-Za-z0-9.-]+)/$', views.currentOrderBillCash, name='currentOrderBillCash'), #GET working
    url(r'^order/(?P<orderId>[0-9]+)/bill/cash/extraCredit=(?P<extraCredit>[0-9]+)&skin=(?P<skin>[A-Za-z0-9.-]+)&token=(?P<token>[A-Za-z0-9.-]+)/$', views.orderBillCash, name='orderBillCash'), #GET working
    url(r'^order/current/bill/credit/token=(?P<token>[A-Za-z0-9.-]+)/$', views.currentOrderBillCredit, name='currentOrderBillCredit'), #GET 
    url(r'^order/(?P<orderId>[0-9]+)/bill/credit/token=(?P<token>[A-Za-z0-9.-]+)/$', views.orderBillCredit, name='orderBillCredit'), #GET 
    url(r'^order/current/receipt/$', views.currentOrderReceipt, name='currentOrderReceipt'), #POST
    url(r'^order/current/pay/$', views.currentOrderCredit, name='currentOrderCredit'), #POST
    url(r'^me/previousOrders/bakeryId=(?P<bakeryId>[0-9]+)&token=(?P<token>[A-Za-z0-9.-]+)/$', views.previousOrders, name='previousOrders'), #GET working
    url(r'^me/allPreviousOrders/token=(?P<token>[A-Za-z0-9.-]+)/$', views.previousOrdersAcrossBakeries, name='previousOrdersAcrossBakeries'), #GET working
    url(r'^me/token=(?P<token>[A-Za-z0-9.-]+)/$', views.token2account, name='token2account'), #GET working
    url(r'^me/topup/bill/amount=(?P<amount>[0-9]+)&skin=(?P<skin>[A-Za-z0-9.-]+)&token=(?P<token>[A-Za-z0-9.-]+)/$', views.topUpAccountBill, name='topUpAccountBill'), # GET
    url(r'^token/create/$', views.createToken, name='createToken'), #POST working
    url(r'^token/verify/token=(?P<token>[A-Za-z0-9.-]+)/$', views.verifyToken, name='verifyToken'), #POST working
    url(r'^adyen/notify/$', views.processAdyenNotification, name='processAdyenNotification'), #POST working
    url(r'^contact/$', views.submitContactIssue, name='submitContactIssue'), # POST working
]
