#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

# Global vars
PIBOYCONF_ROOT_FOLDER="$HOME/PiBoy-Configurator"

cd $PIBOYCONF_ROOT_FOLDER
git reset --hard
git pull

source $PIBOYCONF_ROOT_FOLDER/common.sh >/dev/null 2>&1

sudo python $PIBOYCONF_ROOT_FOLDER/install.py --force
