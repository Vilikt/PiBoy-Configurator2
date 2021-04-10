#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

PIBOYCONF_ROOT_FOLDER="$HOME/PiBoy-Configurator"
PIBOYCONF_MENU_FOLDER="$PIBOYCONF_ROOT_FOLDER/menus"
PIBOYCONF_ACTIONS_FOLDER="$PIBOYCONF_ROOT_FOLDER/actions"
OSD_ROOT_FOLDER="$HOME/osd"
OSD_RESSOURCES_FOLDER="$OSD_ROOT_FOLDER/resources"
OSD_CONFIG_FILE="/boot/osd.cfg"
VERSION="$PIBOYCONF_ROOT_FOLDER/version.sh"
RESSOURCE_VOLUME_IMAGE_CLR="VolumeClr.png"
RESSOURCE_VOLUME_IMAGE_ICON="VolumeIcon.png"
RESSOURCE_VOLUME_IMAGE_SET="VolumeSet.png"
source $VERSION >/dev/null 2>&1