# builds the source (src) into the distribution (dist)
# @param version number

# requirements
import sys
import os
import shutil
import re
import tempfile

# auxiliary function
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

# auxiliary function
# removes comments from html and js files
def stripFiles(dirToClean):
	for root, dirs, files in os.walk(dirToClean):
		for file in files:
			# read file 
			lines = tuple(open(os.path.join(root, file), "r"))
			extension = file.split('.')[-1]
			name = file.split('.')[0]

			with open(os.path.join(root, file), "w") as f:
				for line in lines: 
					if extension == 'js':
						# remove js // comments
						# NEED lijn hieronder is broken want  ook http:// past hij aan
						# line = re.sub("//.*?\n",'\n',line)					
						a = 6 # NEED moet weg (anders werkt if nie meer)					

					elif extension == 'html':
						# remove html <!-- comments -->
						line = re.sub("<!--(.*?)-->", '', line)
					f.write(line)


# auxiliary function
def clearDirectory(dirToClear):
	for the_file in os.listdir(dirToClear):
		filePath = os.path.join(dirToClear, the_file)
		try:
		    if os.path.isfile(filePath):
		        os.unlink(filePath)
		    elif os.path.isdir(filePath): shutil.rmtree(filePath)
		except Exception as e:
		    print(e)

# auxiliary function
def replaceCodeInFile(filePath, toReplace, newText):
	#Create temp file
	fh, absPath = tempfile.mkstemp()
	with open(absPath,'w') as newFile:
		with open(filePath) as oldFile:
			for line in oldFile:
				newFile.write(line.replace(toReplace, newText))
	os.close(fh)
	# remove original file
	os.remove(filePath)
	# move new file
	shutil.move(absPath, filePath)

# relative path to src and dist directory
srcPath = 'src/'
distPath = 'dist/'
serverIp = '146.185.179.39'

# obtain version number from command line arguments
versionNumber = sys.argv[1]
# TODO check if version number is higher than previous

print 'starting build of version ' + versionNumber

print 'removing previous dist files'
clearDirectory(distPath)

print 'writing version.txt'
# edit version file
with open(distPath + 'version.txt', 'w') as f:
    f.write('version = ' + versionNumber)

print 'copying source files'
copytree(srcPath,distPath)

print 'removing comments'
stripFiles(distPath)

# TODO remove block comments from js files
# TODO concatenate scripts

print 'replacing server specific script entries'
# TODO netter maken door bvb op zoek te gaan naar // build replace (localhost) to (146.185.179.39)? 
replaceCodeInFile(distPath + 'static/frontend/js/config.js', 'localhost',serverIp)


print 'build completed'








