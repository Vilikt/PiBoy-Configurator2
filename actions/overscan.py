#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(1, '../')
import tools

BOOT_CONFIG_FILE = "/boot/config.txt"

def main():
	bootConfigFile = open(BOOT_CONFIG_FILE, 'r')
	lines = bootConfigFile.readlines()
	bootConfigFile.close()

	action = str(sys.argv[1])

	newLines = []

	if action == "set":
		value = str(sys.argv[2])

		if value == "no":
			amount = tools.getOptionFromPiboyconfFile('overscan_value')
		
			for line in lines:
				if line.strip() != "overscan_left=" + amount and line.strip() != "overscan_right=" + amount  and line.strip() != "overscan_top=" + amount  and line.strip() != "overscan_bottom=" + amount :
					newLines.append(line.strip()+"\n")
		elif value == "yes":
			amount = str(sys.argv[3])
			
			tools.setOptionFromPiboyconfFile('overscan_value', amount)
			
			for line in lines:
				newLines.append(line.strip()+"\n")

			newLines.append(("overscan_left=" + amount).strip())
			newLines.append(("overscan_right=" + amount).strip())
			newLines.append(("overscan_top=" + amount).strip())
			newLines.append(("overscan_bottom=" + amount).strip())

		bootConfigFile = open(BOOT_CONFIG_FILE, 'w')
		bootConfigFile.writelines(newLines)
		bootConfigFile.close()
	elif action == "get":
		if lines[len(lines)-1].startswith() == "overscan_":
			print("Enable")
			sys.exit(0)
		else:
			print("Disable")
			sys.exit(0)
		
if __name__ == "__main__":
    x= main()
    print( x )
