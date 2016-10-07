import geopy
import geopy.distance
import numpy as np

#a0 = [naam,adres,tel,GPS]
a1 = ['Jan'         ,'Droomlaan 14'     , '8200 Sint-Andries'   ,geopy.Point(40, 2.)]
a2 = ['Piet'        ,'Achterwerk 12'    , '8000 Brugge'         ,geopy.Point(46.853,2)]
a3 = ['Henk'        ,'Linksstraat 69'   , '2800 Mechelen'       ,geopy.Point(47.853, 2.549)]
a4 = ['Hendrik'     ,'Coolway 8'        , '6500 China'          ,geopy.Point(48.853, 2.349)]
a5 = ['Louis'       ,'Maanweg 16'       , '7200 Maan'           ,geopy.Point(49.853, 2.349)]
a6 = ['Nero'        ,'Tochtlaan 87'     , '9700 Willebroek'     ,geopy.Point(50.853, 2.349)]
a7 = ['Michiel'     ,'Omastraat'        , '4100 Mortsel'        ,geopy.Point(46.853, 2.349)]
a8 = ['Matthias'    ,'Westplantsoen 51' , '1200 Portugal'       ,geopy.Point(47.853, 2.349)]
a9 = ['Sloewie'     ,'OchtendReet 2'    , '6520 Kortrijk'       ,geopy.Point(48.853, 2.349)]
a10 = ['Suzy'       ,'Mannekesveere 41' , '8200 Sint-Andries'   ,geopy.Point(49.853, 2.349)]
a11 = ['Irina'      ,'RusLaan 1'        , '8200 Sint-Andries'   ,geopy.Point(50.853, 2.349)]
a12 = ['Helena'     ,'Wasmachineweg 33' , '8200 Sint-Andries'   ,geopy.Point(51.853, 2.349)]

search_query = 'handrik'

selfPosition = geopy.Point(48.1,2.)

data = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12]
score = np.zeros(len(data))

## Combination Score               
weights = np.array([6.,0.,4.])
norm_weights = weights/sum(weights)
for k in range(len(data)):
    bakkerij = data[k]
    for i in range(len(search_query)):
        length = i+1
        for offset in range(len(search_query) - length +1):
            for j in range(3):
                if search_query[offset:offset+length].lower() in bakkerij[j].lower():
                    #print search_query[offset:offset+length].lower(), bakkerij[j].lower()
                    score[k] += norm_weights[j]*float(length)**2
                    
## geo location score
geoGain = 1000.
length = len(search_query) + 1
for k in range(len(data)):
    bakkerij = data[k]
    dist = geopy.distance.distance(selfPosition, bakkerij[3]).km
    score[k] += 1/max(dist,1)*geoGain/float(length)**2
                    
scoreSorted, dataSorted = zip(*sorted(zip(score, data)))

for i in range(6):
    print dataSorted[::-1][i][0], round(scoreSorted[::-1][i]/sum(scoreSorted)*100.,2), round(scoreSorted[::-1][i],2)