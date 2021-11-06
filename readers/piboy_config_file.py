import subprocess
import xml.etree.ElementTree as ET
import os
import sys

autoconfigCfgPath = "/home/pi/PiBoy-Configurator/piboy.cfg"

def indent(elem, level=0):
	i = "\n" + level*"  "
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			indent(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i

def main():
	param = str(sys.argv[1])
	action = str(sys.argv[2])

	if action == "set":
		try:
			sys.argv[3]
			value = str(sys.argv[3])
		except IndexError:
			value = str(os.environ["choice"])

		treeOptions = ET.parse(autoconfigCfgPath)
		root = treeOptions.getroot()
		for child in root:
			if (child.tag == param):
				child.text = value
				treeOptions.write(autoconfigCfgPath)
				os.system("sudo python /home/pi/PiBoy-Configurator/autoconfig.py")
				sys.exit(0)

		# element not exists --> create it
		elt = ET.Element(param)
		elt.text = value
		root.insert(0, elt)
		indent(root)
		treeOptions.write(autoconfigCfgPath)
		sys.exit(0)

	elif action == "get":
		treeOptions = ET.parse(autoconfigCfgPath)
		root = treeOptions.getroot()
		for child in root:
			if (child.tag == param):
				print(child.text)
				sys.exit(0)

		# element not exists --> return 0
		print(0)
		sys.exit(0)

if __name__ == "__main__":
    x= main()