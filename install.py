#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import xml.etree.ElementTree as ET
import os
import sys
import shutil
import tools

def checkInstall():
	path = tools.PIBOY_CONFIGURATOR_ROOT_FOLDER + 'piboy.cfg'
	
	if (os.path.exists(path)):
		return True
	else:
		return False

# first check if need to install
if (checkInstall() == True and not ("--force" in sys.argv)):
	print("Already installed")
	exit(0)
	
# create piboy.cfg
print("Create piboy.cfg")
tools.createPiboyCfg()

if (not ("--only_create_conf_file" in sys.argv)):
	# move the files
	subprocess.call(['sh', './install.sh'])

	# add PiBoy configurator entry in Retropie menu if needed
	res = tools.checkPiboyConfiguratorEntryExists()
	
	if (res == False):
		print("Add Retropie Menu entry")
		tools.addRetropieMenuEntry()
	elif (res == True):
		print("Retropie Menu entry already exits")
	elif (res == -1):
		print("ERROR : File gamelist does not exists...")
		
	# create retroarch.cfg.tv and retroarch.cfg.lcd in all systems config folder if needed
	tools.createRetroarchCfg()

	# create LCD and TV folder in overlays if needed
	tools.createOverlaysFolders()

	# add autoconfig.py execution in rc.local if needed
	tools.addAutoconfigToRcLocal()

print("\nInstallation finished successfully")