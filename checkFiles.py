from os import listdir
from os.path import isfile, join

# dit script is geschreven door Nero Vanbiervliet <nero.vanbiervliet@gmail.com>
# plaats te negeren directories in dirIgnore hieronder

# directories to ignore (with leading slash!)
# e.g. a directory testSuite in the same directory as checkFiles
# must be added as following : "/testSuite"
dirIgnore = ["/.git",'/src/panem_env','/dist']

def getOccurrences(dir,numTabs,prevPath):
	
	#tabstring generation
	tabString = ""
	for i in range(0,numTabs):
		tabString += "    " 	

	consoleOutput = ""
	
	totalNeed = 0
	totalTodo = 0	

	dirList = []
	fileList = []

	for item in listdir(dir):

		if isfile(join(dir,item)):
			fileList.append(item)
		else: # het is een dir
			totalPathCurrentItem = prevPath + '/' + item
			if not totalPathCurrentItem in dirIgnore:
				dirList.append(item)

	# eerst dirs itereren
	for item in dirList:

		[currentNeed,currentTodo, currentConsoleOutput] = getOccurrences(join(dir,item),numTabs+1,prevPath + '/' + item)
		
		if currentNeed>0 or currentTodo>0:
			totalNeed += currentNeed
			totalTodo += currentTodo
			consoleOutput += tabString + item + " " + str(currentNeed) + ' (' + str(currentTodo) + ')\n'
			consoleOutput += currentConsoleOutput
			consoleOutput += '\n' 

	# files itereren
	for item in fileList:

		f = open(join(dir,item))
		contents = f.read()
		f.close()

		currentNeed = contents.count('NE'+'ED')
		currentTodo = contents.count('TO'+'DO')

		totalNeed += currentNeed
		totalTodo += currentTodo

		if currentNeed>0: # rood en wit
			consoleOutput += tabString + "\033[0;31m" + item + "\033[0m " + str(currentNeed) + ' (' + str(currentTodo) + ')\n'
		elif currentTodo>0: # wit (standaard)
			consoleOutput += tabString + item + " " + str(currentNeed) + ' (' + str(currentTodo) + ')\n'

	return [totalNeed,totalTodo, consoleOutput]

# main execution
[totalNeed,totalTodo, consoleOutput] = getOccurrences('.',1,'')
if totalNeed >0:
	print "Do not build, still NE"+"ED left!"
	
print "Total: " + str(totalNeed) + ' (' + str(totalTodo) + ')\n'
print "Breakdown:\n"
print consoleOutput




