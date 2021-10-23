#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import xml.etree.ElementTree as ET
import os
import sys
import shutil
import tools

# remove PiBoy configurator entry in Retropie menu if needed
res = tools.checkPiboyConfiguratorEntryExists()

if (res == False):
	print("Retropie Menu entry does not exists")
elif (res == True):
	tools.removeRetropieMenuEntry()
elif (res == -1):
	print("ERROR : File gamelist does not exists...")
	
# remove PiBoy-Configurator.sh
if os.path.exists("/home/pi/RetroPie/retropiemenu/PiBoy-Configurator.sh"):
	os.remove("/home/pi/RetroPie/retropiemenu/PiBoy-Configurator.sh")
else:
	print("File /home/pi/RetroPie/retropiemenu/PiBoy-Configurator.sh does not exists")
	
# remove autoconfig.py execution in rc.local if needed
tools.removeAutoconfigToRcLocal()

# remove piboy.cfg
if os.path.exists("/home/pi/PiBoy-Configurator/piboy.cfg"):
	os.remove("/home/pi/PiBoy-Configurator/piboy.cfg")
else:
	print("File /home/pi/PiBoy-Configurator/piboy.cfg does not exists")

