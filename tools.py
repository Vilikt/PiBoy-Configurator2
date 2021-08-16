#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
import subprocess

PIBOY_CONFIGURATOR_ROOT_FOLDER = "/home/pi/PiBoy-Configurator/"
READERS_FOLDER = PIBOY_CONFIGURATOR_ROOT_FOLDER + "readers/"
CONFIGS_ROOT_FOLDER = "/opt/retropie/configs/"
EMULATIONSTATION_CONFIG_FOLDER = CONFIGS_ROOT_FOLDER + "all/emulationstation/"
RETROARCHJOYPADS_CONFIG_FOLDER = CONFIGS_ROOT_FOLDER + "all/retroarch-joypads/"
OVERLAYS_FOLDER = CONFIGS_ROOT_FOLDER + "all/retroarch/overlay/"
OVERLAYS_LCD_FOLDER = OVERLAYS_FOLDER + "LCD/"
OVERLAYS_TV_FOLDER = OVERLAYS_FOLDER + "TV/"
OVERLAYS_TV_CLEAN_FOLDER = OVERLAYS_TV_FOLDER + "clean/"
OVERLAYS_TV_GRID_FOLDER = OVERLAYS_TV_FOLDER + "grid/"
RETROPIE_MENU_FOLDER = "/home/pi/RetroPie/retropiemenu/"

PIBOY_SCRIPTNAME_MENU = "./PiBoy-Configurator.sh"
PIBOY_NAME_MENU = "PiBoy Configuration"
PIBOY_DESC_MENU = "Change the PiBoy options."
PIBOY_DESC_IMAGE = "./icons/PiBoy-Configurator.png"
PIBOY_CONTROLLER_NAME = "PiBoy DMG Controller"

BOOT_CONFIG_FILE = "/boot/config.txt"

def setWiFi(on):
	if (on == True):
		action = 'unblock'
		value = 'yes'
	else:
		action = 'block'
		value = 'no'

	p2 = subprocess.Popen("sudo rfkill " + action + " wifi", stdout=subprocess.PIPE, shell=True)
	out, err = p2.communicate() 
	result = out.split('\n')
	
	setOptionFromPiboyconfFile('wifi_enable', value)
	
def setBluetooth(on):
	if (on == True):
		action = 'unblock'
		value = 'yes'
	else:
		action = 'block'
		value = 'no'

	p2 = subprocess.Popen("sudo rfkill " + action + " bluetooth", stdout=subprocess.PIPE, shell=True)
	out, err = p2.communicate() 
	result = out.split('\n')
	
	setOptionFromPiboyconfFile('bt_enable', value)

def getOptionFromPiboyconfFile(option):
	path = PIBOY_CONFIGURATOR_ROOT_FOLDER + 'piboy.cfg'

	# check if config file exits
	if (not os.path.exists(path)):
		return -1

	treeOptions = ET.parse(path)
	root = treeOptions.getroot()
	for child in root:
		if (child.tag == option):
			value_returned = child.text
			
			if value_returned is None:
				value_returned = ""
			
			return value_returned

def setOptionFromPiboyconfFile(option, value):
	path = PIBOY_CONFIGURATOR_ROOT_FOLDER + 'piboy.cfg'

	# check if config file exits
	if (not os.path.exists(path)):
		return -1

	treeOptions = ET.parse(path)
	root = treeOptions.getroot()
	for child in root:
		if (child.tag == option):
			child.text = value
			treeOptions.write(path)
			return 0

def checkPiboyConfiguratorEntryExists():
	path = RETROPIE_MENU_FOLDER + 'gamelist.xml'
	
	# check if config file exits
	if (not os.path.exists(path)):
		return -1
		
	treeOptions = ET.parse(path)
	gamelist = treeOptions.getroot()
	for game in gamelist:
		if (game.find('name').text == PIBOY_NAME_MENU):
			return True
	
	return False

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

def createPiboyCfg():
	uid = 1000
	gid = 1000

	path = PIBOY_CONFIGURATOR_ROOT_FOLDER + 'piboy.cfg'

	# check if config file exits
	if (os.path.exists(path)):
		return -1
	
	piboycfg = ET.Element("config")
	
	overlay_style = ET.Element("overlay_style")
	overlay_style.text = "grid"
	wifi_enable = ET.Element("wifi_enable")
	bt_enable = ET.Element("bt_enable")
	theme_lcd = ET.Element("theme_lcd")
	theme_tv = ET.Element("theme_tv")
	onboard_controller_hdmi = ET.Element("onboard_controller_hdmi")
	onboard_controller_hdmi.text = "yes"
	wifi_always_enable_hdmi = ET.Element("wifi_always_enable_hdmi")
	wifi_always_enable_hdmi.text = "undefined"
	bt_always_enable_hdmi = ET.Element("bt_always_enable_hdmi")
	bt_always_enable_hdmi.text = "undefined"
	wifi_always_enable_lcd = ET.Element("wifi_always_enable_lcd")
	wifi_always_enable_lcd.text = "undefined"
	bt_always_enable_lcd = ET.Element("bt_always_enable_lcd")
	bt_always_enable_lcd.text = "undefined"
	overscan_enable = ET.Element("overscan_enable")
	overscan_enable.text = "no"
	overscan_value = ET.Element("overscan_value")
	overscan_value.text = "0"
	
	piboycfg.insert(0, overlay_style)
	piboycfg.insert(0, wifi_enable)
	piboycfg.insert(0, bt_enable)
	piboycfg.insert(0, theme_lcd)
	piboycfg.insert(0, theme_tv)
	piboycfg.insert(0, onboard_controller_hdmi)
	piboycfg.insert(0, wifi_always_enable_hdmi)
	piboycfg.insert(0, bt_always_enable_hdmi)
	piboycfg.insert(0, wifi_always_enable_lcd)
	piboycfg.insert(0, bt_always_enable_lcd)
	piboycfg.insert(0, overscan_enable)
	piboycfg.insert(0, overscan_value)
	
	indent(piboycfg)
	
	tree = ET.ElementTree(piboycfg)
	tree.write(path, encoding="utf-8", xml_declaration=True)
	
	# set the owner to "pi"
	os.chown(path, uid, gid)
	
def addRetropieMenuEntry():
	path = RETROPIE_MENU_FOLDER + 'gamelist.xml'
	
	# check if config file exits
	if (not os.path.exists(path)):
		return -1
		
	treeOptions = ET.parse(path)
	gamelist = treeOptions.getroot()
	
	piboyEntry = ET.Element("game")
	
	pathEntry = ET.Element("path")
	pathEntry.text = PIBOY_SCRIPTNAME_MENU
	piboyEntry.insert(0, pathEntry)
	
	name = ET.Element("name")
	name.text = PIBOY_NAME_MENU
	piboyEntry.insert(1, name)
	
	desc = ET.Element("desc")
	desc.text = PIBOY_DESC_MENU
	piboyEntry.insert(2, desc)
	
	image = ET.Element("image")
	image.text = PIBOY_DESC_IMAGE
	piboyEntry.insert(3, image)
	
	gamelist.insert(0, piboyEntry)
	
	indent(gamelist)
	treeOptions.write(path, encoding="utf-8", xml_declaration=True)

def copyFileWithAnotherName(path, newPath):
	# check if file exits
	if (not os.path.exists(path)):
		return -1
	
	file = open(path, 'r')
	lines = file.readlines()
	file.close()
	
	newFile = open(newPath, 'w')
	newFile.writelines(lines)

def createRetroarchCfg():
	print("\nNow manage retroarch configurations files in " + CONFIGS_ROOT_FOLDER)
	systems = next(os.walk(CONFIGS_ROOT_FOLDER))
	
	for system in systems[1]:
		if system <> 'all' and not system.startswith("auto-") and system <> 'retropie': 
			contents = next(os.walk(CONFIGS_ROOT_FOLDER + system + '/'))[2]
			# check if retroarch.cfg exists
			retroarchcfgExists = False
			retroarchcfgLcdExists = False
			retroarchcfgTvExists = False
			for file in contents:
				if file == "retroarch.cfg":
					retroarchcfgExists = True
				if file == "retroarch.cfg.lcd":
					retroarchcfgLcdExists = True
				if file == "retroarch.cfg.tv":
					retroarchcfgTvExists = True
			
			if retroarchcfgExists == True:
				if retroarchcfgLcdExists == False:
					# create retroarch.cfg.lcd
					copyFileWithAnotherName(CONFIGS_ROOT_FOLDER + system + '/' + 'retroarch.cfg', CONFIGS_ROOT_FOLDER + system + '/' + 'retroarch.cfg.lcd')
					print("File " + CONFIGS_ROOT_FOLDER + system + '/' + 'retroarch.cfg.lcd' + "was created")
				else:
					print("File " + CONFIGS_ROOT_FOLDER + system + '/' + 'retroarch.cfg.lcd' + "already exixts")
					
				if retroarchcfgTvExists == False:
					# create retroarch.cfg.tv
					copyFileWithAnotherName(CONFIGS_ROOT_FOLDER + system + '/' + 'retroarch.cfg', CONFIGS_ROOT_FOLDER + system + '/' + 'retroarch.cfg.tv')
					print("File " + CONFIGS_ROOT_FOLDER + system + '/' + 'retroarch.cfg.tv' + "was created")
				else:
					print("File " + CONFIGS_ROOT_FOLDER + system + '/' + 'retroarch.cfg.tv' + "already exixts")
				
			else:
				print("There is no retroarch.cfg in system " + system)

def createOverlaysFolders():
	print("\nNow manage overlays folders in " + OVERLAYS_FOLDER)

	# define the access rights
	access_rights = 0o755
	
	if (not os.path.exists(OVERLAYS_LCD_FOLDER)):
		try:
			os.mkdir(OVERLAYS_LCD_FOLDER, access_rights)
		except OSError:
			print ("Creation of the directory %s failed" % OVERLAYS_LCD_FOLDER)
		else:
			print ("Successfully created the directory %s" % OVERLAYS_LCD_FOLDER)
	else:
		print(OVERLAYS_LCD_FOLDER + " already exists")
	
	if (not os.path.exists(OVERLAYS_TV_FOLDER)):
		try:
			os.mkdir(OVERLAYS_TV_FOLDER, access_rights)
		except OSError:
			print ("Creation of the directory %s failed" % OVERLAYS_TV_FOLDER)
		else:
			print ("Successfully created the directory %s" % OVERLAYS_TV_FOLDER)
	else:
		print(OVERLAYS_TV_FOLDER + " already exists")
	
	if (not os.path.exists(OVERLAYS_TV_CLEAN_FOLDER)):
		try:
			os.mkdir(OVERLAYS_TV_CLEAN_FOLDER, access_rights)
		except OSError:
			print ("Creation of the directory %s failed" % OVERLAYS_TV_CLEAN_FOLDER)
		else:
			print ("Successfully created the directory %s" % OVERLAYS_TV_CLEAN_FOLDER)
	else:
		print(OVERLAYS_TV_CLEAN_FOLDER + " already exists")
	
	if (not os.path.exists(OVERLAYS_TV_GRID_FOLDER)):
		try:
			os.mkdir(OVERLAYS_TV_GRID_FOLDER, access_rights)
		except OSError:
			print ("Creation of the directory %s failed" % OVERLAYS_TV_GRID_FOLDER)
		else:
			print ("Successfully created the directory %s" % OVERLAYS_TV_GRID_FOLDER)
	else:
		print(OVERLAYS_TV_GRID_FOLDER + " already exists")

def addAutoconfigToRcLocal():
	print("\nNow manage to add autoconfig.py execution in rc.local")

	rcLocalFile = open("/etc/rc.local", 'r')
	lines = rcLocalFile.readlines()
	rcLocalFile.close()
	
	already_in = False
	for line in lines:
		if line.strip() == "sudo python /home/pi/PiBoy-Configurator/autoconfig.py":
			already_in = True
			
	if already_in == False:
		newLines = []
		
		for line in lines:
			if line.strip() == "exit 0":
				# insert
				newLines.append('\n' + "sudo python /home/pi/PiBoy-Configurator/autoconfig.py" + '\n\n')
				
			newLines.append(line.strip()+"\n")
		
		try :
			rcLocalFile = open("/etc/rc.local", 'w')
			rcLocalFile.writelines(newLines)
			rcLocalFile.close()
			print("The line was successfully added in rc.local")
		except IOError:
			print("Please run this script as Root : sudo python install.py")
	else:
		print("The line is already in rc.local")
		
def addOverscan():
	bootConfigFile = open(BOOT_CONFIG_FILE, 'r')
	lines = bootConfigFile.readlines()
	bootConfigFile.close()

	newLines = []
	
	overscan_value = getOptionFromPiboyconfFile('overscan_value')
			
	for line in lines:
		if not line.startswith("overscan_"):
			newLines.append(line.strip()+"\n")

	newLines.append(("overscan_left=" + overscan_value).strip()+"\n")
	newLines.append(("overscan_right=" + overscan_value).strip()+"\n")
	newLines.append(("overscan_top=" + overscan_value).strip()+"\n")
	newLines.append(("overscan_bottom=" + overscan_value).strip()+"\n")
	
	bootConfigFile = open(BOOT_CONFIG_FILE, 'w')
	bootConfigFile.writelines(newLines)
	bootConfigFile.close()

def removeOverscan():
	bootConfigFile = open(BOOT_CONFIG_FILE, 'r')
	lines = bootConfigFile.readlines()
	bootConfigFile.close()

	newLines = []
	
	overscan_value = getOptionFromPiboyconfFile('overscan_value')
	
	for line in lines:
		if not line.startswith("overscan_"):
			newLines.append(line.strip()+"\n")
	
	bootConfigFile = open(BOOT_CONFIG_FILE, 'w')
	bootConfigFile.writelines(newLines)
	bootConfigFile.close()