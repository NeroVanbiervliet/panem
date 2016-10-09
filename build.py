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

# auxiliary function
# replaces the first line of 
def replaceFirstLineOfFile(filePath, newText):
	with open(filePath) as currentFile:
		lines = currentFile.readlines()
	lines[0] = newText

	with open(filePath, 'w') as currentFile:
		for line in lines:
		    currentFile.write(line)

# relative path to src and dist directory
srcPath = 'src/'
distPath = 'dist/'
serverIp = '146.185.179.39'
serverEnvPath = '/home/sysadmin/panem/dist/panem_env/'

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

# TODO mss virtual env steeds van scratch terug herinstalleren en ook pip libraries automatishc herinstalleren (zie asana voor meer info)
print 'replacing first line of env files'
filesToModify = ['bin/django-admin','bin/django-admin.py', 'bin/f2py','bin/gunicorn','bin/gunicorn_django','bin/gunicorn_paster']
newText = '#!' + serverEnvPath + 'bin/python \n'
for i in range(len(filesToModify)): 
	currentFilePath = 'dist/panem_env/' + filesToModify[i]
	replaceFirstLineOfFile(currentFilePath, newText)

print 'build completed'








