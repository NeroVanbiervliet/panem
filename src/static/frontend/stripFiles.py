import os
import re

prompt = '> '
jsCount = 0
htmlCount = 0

print "Do you realy want to clean the code? y/n"
decision = raw_input(prompt)

if decision == 'y':
	for root, dirs, files in os.walk('.'):
		for file in files:
			# read file 
			lines = tuple(open(os.path.join(root, file), "r"))
			extension = file.split('.')[-1]
			
			if extension == 'js':
				jsCount+=1
			elif extension == 'html':
				htmlCount+=1

			with open(os.path.join(root, file), "w") as f:
				for line in lines: 
					if extension == 'js':
						# remove js // comments
						line = re.sub("//.*?\n",'\n',line)
					elif extension == 'html':
						# remove html <!-- comments -->
						line = re.sub("<!--(.*?)-->", '', line)
					f.write(line)
	print 'finished processing ' + str(jsCount) + ' js and ' + str(htmlCount) + ' html files.'

else:
	print 'cancelled'
