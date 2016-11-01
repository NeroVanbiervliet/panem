from GDR import basicFunctions as bsf
from GDR.basicFunctions import add_product, add_hasProduct, update_product, update_hasProduct
from first.models import HasProduct, Product, Ingredient
from django.db import transaction

def adaptProducts(bakeryId, productUpdate, deleteList):
    output = 'success'
    hasproducts = HasProduct.objects.all()

    newCreatedIngredients = {}

    # transaction.atomic() maakt dat alle databaseoperaties in een keer worden uitgevoerd ipv in aparte databasecalls
    # zoals autocommit die even af staat en pas op het einde alles commit
    with transaction.atomic():

        for category in productUpdate:

            for product in category['products']:

                productId = product['id']
                name = product['name']
                category_id = category['id']
                standard = 0
                price = product['price']

                ingredientObjects = product['ingredients']
                ingredientIds = []
                for i in range(len(ingredientObjects)):
                    curIng = ingredientObjects[i]
                    if 'id' in curIng: # key exists, known ingredient
                        ingredientIds.append(curIng['id'])
                    else: # new ingredient
                        if curIng['name'] in newCreatedIngredients: # already created a new ingredient
                            ingredientIds.append(newCreatedIngredients[curIng['name']])
                        else:
                            # create new ingredient
                            newId = bsf.addBakeryIngredient(bakeryId,curIng['name'])
                            # add name and id to new created ingredients array
                            newCreatedIngredients[curIng['name']] = newId
                            # add id to product
                            ingredientIds.append(newId)

                if productId == str(-1): # betekent een nieuw product dat nog niet bestond

                    available = (str(product['available']) == 'True') # this is the conversion of a string to a boolean
                    fotoId = category['defaultPhotoId']

                    productIdNew = add_product(name,category_id,standard,fotoId,str(ingredientIds))
                    add_hasProduct(bakeryId,productIdNew,price,available)

                else:
                    available = product['available'] # NEED waarom verschillend met in if hierboven?

                    fotoId = product['photoId']

                    hasProductId = -1 #temp

                    # TODO slechte code, je moet gewoon zoeken naar hasproduct waar bakeryId = ... en productId = ... (kan in databases)
                    for hasproduct in hasproducts:
                        if str(hasproduct.bakeryId) == str(bakeryId) and str(hasproduct.productId) == str(productId):
                            hasProductId = hasproduct.id
                            break

                    if not hasproduct == -1:
                        update_product(productId,name,category_id,standard,fotoId,str(ingredientIds)) # toString for ingredientIds array!
                        update_hasProduct(hasProductId,bakeryId,productId,price,available)
                    else:
                        output = 'dikkeerror'

        for productId in deleteList:
            hasProductId = -1 #temp

            for hasproduct in hasproducts:
                if str(hasproduct.bakeryId) == str(bakeryId) and str(hasproduct.productId) == str(productId):
                    hasProductId = hasproduct.id
                    break

            if not hasProductId == -1:

                object = HasProduct.objects.get(id=hasProductId)
                object.delete()

            object = Product.objects.get(id=productId)
            object.delete()

    return output

# NEED niet zeker of dit nog werkt
def ingredients2Allergenes(allIngredients,ingredients):
    allergenes = []
    for ingredient in eval(ingredients):
        for ingredientObject in allIngredients:
            if ingredientObject.id  == ingredient:
                for allergene in eval(ingredientObject.allergenes):
                    if not allergene in allergenes:
                        allergenes.append(allergene)

    return allergenes

# returns the ingredients known for a bakery
def getIngredients(bakeryId):

    standardIngredientsNames = []

    # find standard ingredients
    standardIngredients = Ingredient.objects.all().filter(isStandard=True)
    for ingredient in standardIngredients:
        standardIngredientsNames.append({'name' :ingredient.name, 'id' : ingredient.id})

    bakeryIngredientsNames = []

    # find bakery specific ingredients
    bakeryIngredients = Ingredient.objects.all().filter(bakeryId=bakeryId).filter(isStandard=False)
    for ingredient in bakeryIngredients:
        bakeryIngredientsNames.append({'name' :ingredient.name, 'id' : ingredient.id})

    return {
                'standard' : standardIngredientsNames,
                'custom' : bakeryIngredientsNames
            }

# stores new ingredients
# a task in asana is created to fill in the allergene details of those ingredients NEED
def insertIngredients(bakeryId, ingredientArray):

    for i in range(len(ingredientArray)):
        ingredient = ingredientArray[i]
        bsf.addBakeryIngredient(bakeryId,ingredient['name'])

    return "success"