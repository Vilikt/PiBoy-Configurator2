import os
import sys

BOOT_CONFIG_FILE = "/boot/config.txt"

def main():
	bootConfigFile = open(BOOT_CONFIG_FILE, 'r')
	lines = bootConfigFile.readlines()
	bootConfigFile.close()

	action = str(sys.argv[1])

	newLines = []

	if action == "set":
		value = str(sys.argv[2])

		if value == "enable":
			for line in lines:
				if line.strip() != "dtoverlay=disable-bt":
					newLines.append(line.strip()+"\n")
		elif value == "disable":
			for line in lines:
				newLines.append(line.strip()+"\n")

			newLines.append("dtoverlay=disable-bt".strip())

		bootConfigFile = open(BOOT_CONFIG_FILE, 'w')
		bootConfigFile.writelines(newLines)
		bootConfigFile.close()
	elif action == "get":
		if lines[len(lines)-1].strip() == "dtoverlay=disable-bt":
			print("Disable")
			sys.exit(0)
		else:
			print("Enable")
			sys.exit(0)
		
if __name__ == "__main__":
    x= main()
    print( x )
