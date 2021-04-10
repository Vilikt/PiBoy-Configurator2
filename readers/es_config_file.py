import os
import sys

CONFIGS_ROOT_FOLDER = "/opt/retropie/configs/"
ES_CONFIG_FILE = CONFIGS_ROOT_FOLDER + "all/emulationstation/es_settings.cfg"

def parseOptionsAndSet(line, newValue):
	parts = line.split(' ')
	ret = []
	type = parts[0].replace("<", "")
	name = parts[1].replace('"', '').replace('name=', '')
	ret.append(type)
	ret.append(name)
	ret.append(newValue)

	return ret

def parseOptions(line):
	parts = line.split(' ')
	ret = []
	type = parts[0].replace("<", "")
	name = parts[1].replace('"', '').replace('name=', '')
	value = parts[2].replace('"', '').replace('value=', '')
	ret.append(type)
	ret.append(name)
	ret.append(value)

	return ret
	
def getOptions(params):
	line = '<' + params[0] + ' name="' + params[1] + '" value="' + params[2] + '" />'
	print(line)
	return line

def main():
	# check if file exits
	if (not os.path.exists(ES_CONFIG_FILE)):
		return

	esConfigFile = open(ES_CONFIG_FILE, 'r')
	lines = esConfigFile.readlines()
	esConfigFile.close()

	paramToSearch = str(sys.argv[1])
	action = str(sys.argv[2])

	if action == "set":
		try:
			sys.argv[3]
			value = str(sys.argv[3])
		except IndexError:
			value = str(os.environ["choice"])

		newLines = []

		for line in lines:
			if 'name="' + paramToSearch + '"' in line:
				line = getOptions(parseOptionsAndSet(line, value))
				print(line)
				
			newLines.append(line.strip()+"\n")
		
		osdConfigFile = open(ES_CONFIG_FILE, 'w')
		osdConfigFile.writelines(newLines)
		osdConfigFile.close()
	elif action == "get":
		for line in lines:
			if 'name="' + paramToSearch + '"' in line:
				ret = parseOptions(line)
				print(ret[2])
				
	sys.exit(0)

if __name__ == "__main__":
    x= main()
    print( x )