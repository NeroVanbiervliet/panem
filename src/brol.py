# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 22:38:43 2016

@author: matthias
"""

from first.models import Product,Bakery

#products = Product.objects.all()
#for products in products:
#    products.fotoId = 1
#    products.save()
bakeries = Bakery.objects.all()
for bakery in bakeries:
    bakery.openings = '[[{"h": "6", "m": "30"}, {"h": "19", "m": ""},false], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},false], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},false], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},false], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},false], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},false], [{"h": "6", "m": "30"}, {"h": "19", "m": ""},false]]'
    bakery.save()
    
print 'success'