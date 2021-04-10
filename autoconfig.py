#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import xml.etree.ElementTree as ET
import os
import sys
import tools

MODE = 0
OVERLAY_STYLE = ""
SNES_MINI_THEME = 0
MODE_HDMI = "HDMI"
MODE_LCD = "LCD"

def getWidth():
	return int(subprocess.check_output(["fbset"]).splitlines()[2].strip().split(' ')[1])
	
def getHeight():
	return int(subprocess.check_output(["fbset"]).splitlines()[2].strip().split(' ')[2])
	
def compatibleResolution(width, height):
	resolution = ""

	if (width == 640 and height == 480) or (width == 800 and height == 600) or (width == 1024 and height == 768) or (width == 1280 and height == 720) or (width == 1280 and height == 960) or (width == 1366 and height == 768) or (width == 1440 and height == 1080) or (width == 1920 and height == 1080):
		resolution = str(width) + "x" + str(height)
	else:
		resolution = "640x480"
		
	return str(resolution)

def makeEmulationStationCfg(mode):
	# set Theme
	if (mode == MODE_LCD):
		lcd_theme = tools.getOptionFromPiboyconfFile('theme_lcd')
		
		if len(lcd_theme) > 0:
			p2 = subprocess.Popen(" python " + tools.READERS_FOLDER + "es_config_file.py ThemeSet set " + lcd_theme, stdout=subprocess.PIPE, shell=True)
			out, err = p2.communicate() 
			result = out.split('\n')
	elif (mode == MODE_HDMI):
		tv_theme = tools.getOptionFromPiboyconfFile('theme_tv')
		
		if len(tv_theme) > 0:
			p2 = subprocess.Popen(" python " + tools.READERS_FOLDER + "es_config_file.py ThemeSet set " + tv_theme, stdout=subprocess.PIPE, shell=True)
			out, err = p2.communicate() 
			result = out.split('\n')
		
def makeRetroarchCfg(system, mode, overlayStyle):
	uid = 1000
	gid = 1000
	
	if (mode == MODE_HDMI):
		suffix = "tv"
	elif (mode == MODE_LCD):
		suffix = "lcd"
	
	path = tools.CONFIGS_ROOT_FOLDER + system + "/" + "retroarch.cfg." + suffix
	
	# check if config file mode exits
	if (not os.path.exists(path)):
		return
	
	# removes existing retroarch.cfg in configs folder
	if (os.path.exists(tools.CONFIGS_ROOT_FOLDER + system + "/" + "retroarch.cfg")):
		os.remove(tools.CONFIGS_ROOT_FOLDER + system + "/" + "retroarch.cfg")

	# copy the appropriate file according to the actual mode
	fin = open(path, "rt")
	fout = open(tools.CONFIGS_ROOT_FOLDER + system + "/" + "retroarch.cfg", "wt")
	for line in fin:
		# replace necessary entries
		line = line.replace('[overlay_style]', overlayStyle.lower())
		fout.write(line)
	fin.close()
	fout.close()
	
	# set the owner to "pi"
	os.chown(tools.CONFIGS_ROOT_FOLDER + system + "/" + "retroarch.cfg", uid, gid)
	
	return
	
def changeEmulatorsCfgSGB(mode):
	path = tools.CONFIGS_ROOT_FOLDER + "sgb/emulators.cfg"
	
	# check if file exits
	if (not os.path.exists(path)):
		return
	
	file = open(path, "rt")
	data = file.read()
	
	# change default emulator according to MODE
	if (mode == MODE_LCD):
		data = data.replace('default = "lr-mgba-sgb"', 'default = "lr-gambatte"')
	else:
		data = data.replace('default = "lr-gambatte"', 'default = "lr-mgba-sgb"')
		
	file.close()
	
	file = open(path, "wt")
	file.write(data)
	file.close()

	return

def enableOnboardPiboyController():
	enableOnboardPiboyControllerInESInput()
	setOnboardPiboyControllerRetroarchJoypads(True)

def setOnboardPiboyControllerRetroarchJoypads(enable):
	uid = 1000
	gid = 1000
	
	if (enable==True):
		path = tools.RETROARCHJOYPADS_CONFIG_FOLDER + 'PiBoy DMG Controller.cfg.disabled'
	else:
		path = tools.RETROARCHJOYPADS_CONFIG_FOLDER + 'PiBoy DMG Controller.cfg'
	
	# check if config file exits
	if (not os.path.exists(path)):
		return -1
	
	if (enable==True):
		os.rename(path, tools.RETROARCHJOYPADS_CONFIG_FOLDER + 'PiBoy DMG Controller.cfg')
	else:
		os.rename(path, tools.RETROARCHJOYPADS_CONFIG_FOLDER + 'PiBoy DMG Controller.cfg.disabled')
		
def enableOnboardPiboyControllerInESInput():
	uid = 1000
	gid = 1000
	
	# in ES input
	pathEsInput = tools.EMULATIONSTATION_CONFIG_FOLDER + 'es_input.cfg'
	
	# check if config file exits
	if (not os.path.exists(pathEsInput)):
		return -1
	
	pathPiboyEsInput = tools.EMULATIONSTATION_CONFIG_FOLDER + 'piboy_es_input.cfg'
	
	# check if config file exits
	if (not os.path.exists(pathPiboyEsInput)):
		#print(pathPiboyEsInput + " is not exists")
		return -1
	
	treeOptions = ET.parse(pathPiboyEsInput)
	inputConfigPiboy = treeOptions.getroot()
	
	esInput = ET.parse(pathEsInput)
	inputList = esInput.getroot()
	
	already_here = False
	for inputConfig in inputList.iter('inputConfig'):
		if inputConfig.get("deviceName") == tools.PIBOY_CONTROLLER_NAME:
			already_here = True
	
	if not already_here:
		inputList.insert(1, inputConfigPiboy)
		tools.indent(inputList)
		esInput.write(pathEsInput, encoding="utf-8", xml_declaration=True)
	
def disableOnboardPiboyControllerInESInput():
	uid = 1000
	gid = 1000

	path = tools.EMULATIONSTATION_CONFIG_FOLDER + 'es_input.cfg'

	# check if config file exits
	if (not os.path.exists(path)):
		return -1
		
	treeOptions = ET.parse(path)
	inputList = treeOptions.getroot()
	
	for inputConfig in inputList.iter('inputConfig'):
		if inputConfig.get("deviceName") == tools.PIBOY_CONTROLLER_NAME:
			# save the xml
			newPath = tools.EMULATIONSTATION_CONFIG_FOLDER + 'piboy_es_input.cfg'
	
			tree = ET.ElementTree(inputConfig)
			tree.write(newPath, encoding="utf-8", xml_declaration=True)
			
			# set the owner to "pi"
			os.chown(newPath, uid, gid)
			
			# delete in es_input
			inputList.remove(inputConfig)
			
			treeOptions.write(path, encoding="utf-8", xml_declaration=True)

def disableOnboardPiboyController():
	disableOnboardPiboyControllerInESInput()
	setOnboardPiboyControllerRetroarchJoypads(False)

def manageSystems(systems, actual_path):
	for system in systems[1]:
		newPath = r"" + actual_path + system + '/'
		
		if os.path.isdir(newPath):
			subfolders = next(os.walk(newPath))
		
			if len(subfolders[1]) > 0 :
				manageSystems(subfolders, newPath)
			
		makeRetroarchCfg(system, MODE, OVERLAY_STYLE)

#####################
# BEGIN

width = getWidth()
height = getHeight()
resolution = compatibleResolution(width, height)

# Determine MODE
if (resolution == "640x480"):
	MODE = MODE_LCD
else:
	MODE = MODE_HDMI
	
# Read options
res = tools.getOptionFromPiboyconfFile('overlay_style')
if (res <> -1):
	OVERLAY_STYLE = res.upper()
else:
	exit(-1)

# Disable PiBoy onboard controller if needed
res = tools.getOptionFromPiboyconfFile('onboard_controller_hdmi')
if (res <> -1):
	ONBOARD_CONTROLLER_HDMI = res
else:
	exit(-1)

if (MODE == MODE_HDMI):
	if (ONBOARD_CONTROLLER_HDMI == 'no'):
		disableOnboardPiboyController()
	else:
		enableOnboardPiboyController()
else:
	#print('Try to enable onBoardController if necessary')
	enableOnboardPiboyController()
	
# WiFi
if (MODE == MODE_HDMI):
	res = tools.getOptionFromPiboyconfFile('wifi_always_enable_hdmi')
	if (res <> -1):
		WIFI_ALWAYS_ENABLE_HDMI = res
	else:
		exit(-1)
		
	if (WIFI_ALWAYS_ENABLE_HDMI != 'undefined'):
		if (WIFI_ALWAYS_ENABLE_HDMI == 'yes'):
			tools.setWiFi(True)
		elif (WIFI_ALWAYS_ENABLE_HDMI == 'no'):
			tools.setWiFi(False)
	else:
		res = tools.getOptionFromPiboyconfFile('wifi_enable')
		if (res <> -1):
			if (res == 'yes'):
				tools.setWiFi(True)
			elif (res == 'no'):
				tools.setWiFi(False)
		else:
			tools.setWiFi(True)
			
elif (MODE == MODE_LCD):
	res = tools.getOptionFromPiboyconfFile('wifi_always_enable_lcd')
	if (res <> -1):
		WIFI_ALWAYS_ENABLE_LCD = res
	else:
		exit(-1)
		
	if (WIFI_ALWAYS_ENABLE_LCD != 'undefined'):
		if (WIFI_ALWAYS_ENABLE_LCD == 'yes'):
			tools.setWiFi(True)
		elif (WIFI_ALWAYS_ENABLE_LCD == 'no'):
			tools.setWiFi(False)
	else:
		res = tools.getOptionFromPiboyconfFile('wifi_enable')
		if (res <> -1):
			if (res == 'yes'):
				tools.setWiFi(True)
			elif (res == 'no'):
				tools.setWiFi(False)
		else:
			tools.setWiFi(True)
			
# Bkuetooth
if (MODE == MODE_HDMI):
	res = tools.getOptionFromPiboyconfFile('bt_always_enable_hdmi')
	if (res <> -1):
		BT_ALWAYS_ENABLE_HDMI = res
	else:
		exit(-1)
		
	if (BT_ALWAYS_ENABLE_HDMI != 'undefined'):
		if (BT_ALWAYS_ENABLE_HDMI == 'yes'):
			tools.setBluetooth(True)
		elif (BT_ALWAYS_ENABLE_HDMI == 'no'):
			tools.setBluetooth(False)
	else:
		res = tools.getOptionFromPiboyconfFile('bt_enable')
		if (res <> -1):
			if (res == 'yes'):
				tools.setBluetooth(True)
			elif (res == 'no'):
				tools.setBluetooth(False)
		else:
			tools.setBluetooth(True)
			
elif (MODE == MODE_LCD):
	res = tools.getOptionFromPiboyconfFile('bt_always_enable_lcd')
	if (res <> -1):
		BT_ALWAYS_ENABLE_LCD = res
	else:
		exit(-1)
		
	if (BT_ALWAYS_ENABLE_LCD != 'undefined'):
		if (BT_ALWAYS_ENABLE_LCD == 'yes'):
			tools.setBluetooth(True)
		elif (BT_ALWAYS_ENABLE_LCD == 'no'):
			tools.setBluetooth(False)
	else:
		res = tools.getOptionFromPiboyconfFile('bt_enable')
		if (res <> -1):
			if (res == 'yes'):
				tools.setBluetooth(True)
			elif (res == 'no'):
				tools.setBluetooth(False)
		else:
			tools.setBluetooth(True)

# Overscan
res = tools.getOptionFromPiboyconfFile('overscan_enable')
if (res <> -1):
	OVERSCAN_ENABLE = res
else:
	exit(-1)
	
if (OVERSCAN_ENABLE == 'yes'):
	tools.addOverscan()
else:
	tools.removeOverscan()

# Super Game Boy case
changeEmulatorsCfgSGB(MODE)

# EmulationStation configuration
makeEmulationStationCfg(MODE)

# Retroarch configurations
# Get all systems folders
systems = next(os.walk(tools.CONFIGS_ROOT_FOLDER))
manageSystems(systems, tools.CONFIGS_ROOT_FOLDER)

exit()
