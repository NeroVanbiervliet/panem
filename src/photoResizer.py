# photoResizer
# version 1 : Matthias Baert
# version 2 : Nero Vanbiervliet


import os
from PIL import Image
from resizeimage import resizeimage

topDirectory = 'static/images/'

productDir = 'products/'
shopDir = 'shops/'
brandDir = 'brand/'

for directory in [productDir, shopDir]:

	# the directory of images that will be processed    
	totalDir = topDirectory + directory
    
	# determine the desired output sizes
	sizeList = [name for name in os.listdir('./' + totalDir) if os.path.isdir('./' + totalDir + name)]
	sizeList.remove('original')
	parsedSizeList = []
	for size in sizeList:
		if 'x' in size:
			parsedSizeList.append([int(size.split('x')[0]),int(size.split('x')[1])])
		else: # 1 number indicates a square photo
			parsedSizeList.append([int(size),int(size)])	

	imageDirectory = totalDir + 'original/'
	imageLinks = os.listdir(totalDir + 'original/')
    
	for imageLink in imageLinks:
		for size in parsedSizeList:
			imagelinkUnitless = imageLink.split('.')[0]
			saveDirectory = totalDir + sizeList[parsedSizeList.index(size)] + '/' + imagelinkUnitless + '.png'

			img = Image.open(imageDirectory + imageLink) # image extension *.png,*.jpg
			new_width  = size[0]
			new_height = size[1]
			img = img.resize((new_width, new_height), Image.ANTIALIAS)
			img.save(saveDirectory) # format may what u want ,*.png,*jpg,*.gif

print 'done'
