#! /usr/bin/python
import os, time, shutil, datetime, shutil

WORKPATH = "/Volumes/Workvolume"
ITUNES_AUTOADD = '/Users/hmm/iTunes/Automatically Add to iTunes.localized/'
UNRAR = "/use/bin/unrar"

os.chdir(WORKPATH)

while True:

	listUnprocessedRARs = []
	dictFileToFlag = {}
	for (dirpath, dirnames, filOBenames) in os.walk('Torrents'):
		for fn in filenames:
			fullname = os.path.join(dirpath, fn)
			fullnameFlagFile = fullname + '.processed'
			if not os.path.exists(fullnameFlagFile):
				if ((time.time() - os.stat(fullname).st_mtime) > 2*60): # if file was not modified in last two minutes
					(fname, fnext) = os.path.splitext(fn)
					if fnext.lower() == ".rar" and not fname.lower().endswith('sample') and not fname.lower().endswith('subs'):
						listUnprocessedRARs.append(os.path.join(dirpath, fn))
					elif fnext.lower() in [".avi", ".mpg", ".mkv", ".mp4"] and not fname.endswith('sample'):
						os.close(os.open(fullname, os.O_RDONLY | os.O_EXLOCK))
						shutil.copy(fullname, 'Torrents.In.Process/')
						open(fullnameFlagFile, "w").close()
						print "Flag file for " + fn + " is " + fullnameFlagFile
						dictFileToFlag[fn] = fullnameFlagFile

	for rar in listUnprocessedRARs:
		result = os.spawnv(
			os.P_WAIT,
			UNRAR, 	
			[
				"unrar",
				"x",
				"-y",
				rar,
				"Torrents.In.Process/"
			]
		)
		if result == 0:
			open(rar + ".processed", "w").close()

	for (filename) in os.listdir('Torrents.In.Process'):
		if not filename.startswith('.'):
			print filename
			fnIn = os.path.join('Torrents.In.Process/', filename)
			(fnnameIn, fnextIn) = os.path.splitext(filename)

			fnOut = ""
			if fnextIn.lower() == '.mp4':
				fnOut = fnIn # just copy it straight on
			elif fnextIn.lower() in [".avi", ".mpg", ".mkv"]:
				fnOut = os.path.join('Torrents.In.Process/', fnnameIn) + '.mp4'
				result = os.spawnv(
					os.P_WAIT,
					"/Applications/HandBrakeCLI",
					[
						"HandBrakeCLI",
						"-i", fnIn,
						"-o", fnOut,
						"-Z", "Normal"
					]
				)
				print "Result of conversion for " + fnOut + " is " , result
				print "Does " + fnOut + " exist?", os.path.exists(fnOut)
				if not os.path.exists(fnOut):
					print fnOut + " does not exist - removing " + fnIn
					os.remove(fnIn)
					print "Is " + filename + " in ", dictFileToFlag
					if filename in dictFileToFlag:
						print "Conversion failed, removing " + dictFileToFlag[filename]
						os.remove(dictFileToFlag[filename])
			else:
				print "Ignoring " + filename

			if fnOut != "" and os.path.exists(fnOut):
				os.chmod(fnOut, 0777)
				shutil.copy(fnOut, 
					os.path.join(ITUNES_AUTOADD, fnnameIn) + '.mp4') 
				os.remove(fnOut)
				if os.path.exists(fnIn): os.remove(fnIn)
	print datetime.datetime.now(), " sleep..."
	time.sleep(60)
