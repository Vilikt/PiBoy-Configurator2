#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

# Global vars
PIBOYCONF_ROOT_FOLDER="/home/pi/PiBoy-Configurator"

python $PIBOYCONF_ROOT_FOLDER/uninstall.py

sudo systemctl restart autologin@tty1.service
