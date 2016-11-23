from first.models import Order,Bakery
from django.db.models import Q
import time,datetime



def runUpdater():

    running = True
    
    updateDeltaT = 60 #s
    tLast = time.time() - 60.
    
    while running:
        
        if time.time() - tLast > updateDeltaT:
            
            runOrderFreezer()
            tLast = time.time()
            
def runOrderFreezer():
    
    
    interestingOrders = Order.objects.filter(~Q(status='frozen'))
    for order in interestingOrders:
        
        bakery = Bakery.objects.get(id=order.bakeryId)
        bestelLimitTime = (bakery.bestelLimitTime).split(':')
        
        timePickup = order.timePickup

        limitDate = datetime.datetime(timePickup.year,timePickup.month,timePickup.day-1,int(bestelLimitTime[0]),int(bestelLimitTime[1]),0)
        
        limitTime = time.mktime(limitDate.timetuple())
        
        if limitTime < time.time():
            
            order.status = 'freeze'
            order.save()
            
            