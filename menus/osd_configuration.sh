#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

# Global vars
PIBOYCONF_ROOT_FOLDER="$HOME/PiBoy-Configurator"
source $PIBOYCONF_ROOT_FOLDER/common.sh >/dev/null 2>&1

THROTTLE="Undefined"
BLUETOOTH="Undefined"
WIFI="Undefined"
BATTERY="Undefined"
TEMPERATURE="Undefined"

function update_variables() {
	THROTTLE=`sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py throttle comment get`
	BLUETOOTH=`sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py bluetooth comment get`
	WIFI=`sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py wifi comment get`
	BATTERY=`sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py battery comment get`
	TEMPERATURE=`sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py temperature comment get`
	VOLUME=`sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py volumeicon comment get`
	LOAD=`sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py load comment get`
	VOLTAGE=`sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py voltage comment get`
	CURRENT=`sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py current comment get`
	CPU=`sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py cpu comment get`
	#getVolumeImagesRessourcesName
}

function getVolumeImagesRessourcesName() {
	for entry in "$OSD_RESSOURCES_FOLDER"/*
	do
		if [[ $entry == *"$RESSOURCE_VOLUME_IMAGE_CLR"* ]]; then
			if [[ $entry == *"__"* ]]; then
				VOLUME="no"
			else
				VOLUME="yes"
			fi
		fi
	done
}

function manage_choice() {
	#local choice=$1

	if [ "$choice" == "show_throttle" ]; then
		if [ "$THROTTLE" == "yes" ]; then
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py throttle comment set no
		else
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py throttle comment set yes
		fi
	elif [ "$choice" == "show_bt" ]; then
		if [ "$BLUETOOTH" == "yes" ]; then
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py bluetooth comment set no
		else
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py bluetooth comment set yes
		fi
	elif [ "$choice" == "show_wifi" ]; then
		if [ "$WIFI" == "yes" ]; then
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py wifi comment set no
		else
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py wifi comment set yes
		fi
	elif [ "$choice" == "show_battery" ]; then
		if [ "$BATTERY" == "yes" ]; then
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py battery comment set no
		else
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py battery comment set yes
		fi
	elif [ "$choice" == "show_temperature" ]; then
		if [ "$TEMPERATURE" == "yes" ]; then
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py temperature comment set no
		else
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py temperature comment set yes
		fi
	elif [ "$choice" == "show_volume" ]; then
		if [ "$VOLUME" == "yes" ]; then
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py volumeicon comment set no
		else
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py volumeicon comment set yes
		fi
	elif [ "$choice" == "show_load" ]; then
		if [ "$LOAD" == "yes" ]; then
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py load comment set no
		else
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py load comment set yes
		fi
	elif [ "$choice" == "show_voltage" ]; then
		if [ "$VOLTAGE" == "yes" ]; then
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py voltage comment set no
		else
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py voltage comment set yes
		fi
	elif [ "$choice" == "show_current" ]; then
		if [ "$CURRENT" == "yes" ]; then
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py current comment set no
		else
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py current comment set yes
		fi
	elif [ "$choice" == "show_cpu" ]; then
		if [ "$CPU" == "yes" ]; then
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py cpu comment set no
		else
			sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py cpu comment set yes
		fi
	fi
	
	update_variables
}


function main_menu() {
    local choice

    while true; do
        choice=$(dialog --backtitle "PiBoy Configurator v.$piboyconf_version" --title "OSD Configuration" \
            --ok-label "Select" --cancel-label "Back" --no-tags \
            --menu "Settings" 25 75 20 \
			"show_throttle" "1 Show throttle : $THROTTLE" \
			"show_bt" "2 Show Bluetooth : $BLUETOOTH" \
			"show_wifi" "3 Show Wifi : $WIFI" \
			"show_battery" "4 Show Battery : $BATTERY" \
			"show_temperature" "5 Show Temperature : $TEMPERATURE" \
			"show_volume" "6 Show Volume : $VOLUME" \
			"show_load" "7 Show Load : $LOAD" \
			"show_voltage" "8 Show Voltage : $VOLTAGE" \
			"show_current" "9 Show Current : $CURRENT" \
			"show_cpu" "10 Show CPU : $CPU" \
            2>&1 > /dev/tty)
		
		opt=$?
		[ $opt -eq 1 ] && exit
		
		manage_choice choice
    done
}

update_variables
main_menu

