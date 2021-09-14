#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

# Global vars
PIBOYCONF_ROOT_FOLDER="$HOME/PiBoy-Configurator"
source $PIBOYCONF_ROOT_FOLDER/common.sh >/dev/null 2>&1

function update_variables() {
	ONBOARD_CONTROLLER_STATE=`sudo python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py onboard_controller_hdmi get`
}

function manage_choice() {
	if [ "$choice" == "enable" ]; then
		python /home/pi/PiBoy-Configurator/readers/piboy_config_file.py onboard_controller_hdmi set yes
	elif [ "$choice" == "disable" ]; then
		python /home/pi/PiBoy-Configurator/readers/piboy_config_file.py onboard_controller_hdmi set no
	fi
	
	update_variables
}

function main_menu() {
    local choice

    while true; do
		#ONBOARD_CONTROLLER_STATE=($(grep -oP '(?<=onboard_controller_hdmi>)[^<]+' "$PIBOYCONF_ROOT_FOLDER/piboy.cfg"))
		#ONBOARD_CONTROLLER_STATE=0

		if [ "$ONBOARD_CONTROLLER_STATE" == "yes" ]; then
			ONBOARD_CONTROLLER="Enable"
		else
			ONBOARD_CONTROLLER="Disable"
		fi
		
        choice=$(dialog --backtitle "PiBoy Configurator v.$piboyconf_version" --title "Onboard controller behavior" \
            --ok-label "Select" --cancel-label "Back" --no-tags \
            --menu "Onboard controller is $ONBOARD_CONTROLLER on HDMI" 25 75 20 \
			"enable" "1 Enable on HDMI" \
			"disable" "2 Disable on HDMI" \
            2>&1 > /dev/tty)
		
		opt=$?
		[ $opt -eq 1 ] && exit
		
        manage_choice choice
    done
}

update_variables
main_menu