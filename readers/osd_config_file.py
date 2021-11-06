import os
import sys

PIBOY_OSD_ROOT_FOLDER = "/home/pi/osd/"
OSD_CONFIG_FILE = "/boot/osd.cfg"

osdConfigFile = open(OSD_CONFIG_FILE, 'r')
lines = osdConfigFile.readlines()
osdConfigFile.close()

paramToSearch = str(sys.argv[1])
type = str(sys.argv[2])
action = str(sys.argv[3])

if action == "set":
	try:
		sys.argv[4]
		value = str(sys.argv[4])
	except IndexError:
		value = str(os.environ["choice"])

	newLines = []
	ignore_next = False

	for line in lines:
		if ignore_next == False:
			if type == "comment":
				if line.strip() == paramToSearch or line.strip() == '#'+paramToSearch:
					if value == 'yes':
						line = paramToSearch
					elif value == 'no':
						line = '#'+paramToSearch
			elif type == "value_below":
				if line.strip().startswith(paramToSearch):
					line = paramToSearch + "\n" + value
					ignore_next = True
			
			newLines.append(line.strip()+"\n")
		else:
			ignore_next = False
	
	osdConfigFile = open(OSD_CONFIG_FILE, 'w')
	osdConfigFile.writelines(newLines)
	osdConfigFile.close()
elif action == "get":
	line_index = -1
	for line in lines:
		line_index += 1
		if type == "comment":
			if line.strip() == paramToSearch or line.strip() == '#'+paramToSearch:
				if line.strip().startswith('#'):
					print("no")
				else:
					print("yes")
		elif type == "value_below":
			if line.strip().startswith(paramToSearch):
				print(lines[line_index+1].replace(paramToSearch,"").strip())
			
sys.exit(0)