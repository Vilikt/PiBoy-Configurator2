#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

# Global vars
PIBOYCONF_ROOT_FOLDER="$HOME/PiBoy-Configurator"
source $PIBOYCONF_ROOT_FOLDER/common.sh >/dev/null 2>&1

function update_variables() {
	OVERSCAN_ENABLE=`python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py overscan_enable get`
	OVERSCAN_VALUE=`python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py overscan_value get`
}

function manage_choice() {
	if [ "$choice" == "OVERSCAN" ]; then
		if [ "$OVERSCAN_ENABLE" == "no" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py overscan_enable set yes
		elif [ "$OVERSCAN_ENABLE" == "yes" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py overscan_enable set no
		fi
	elif [ "$choice" == "VALUE_INCREASE" ]; then
		python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py overscan_value set $((OVERSCAN_VALUE + 1))
	elif [ "$choice" == "VALUE_DECREASE" ]; then
		python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py overscan_value set $((OVERSCAN_VALUE - 1))
	elif [ "$choice" == "VALUE_INCREASE_10" ]; then
		python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py overscan_value set $((OVERSCAN_VALUE + 10))
	elif [ "$choice" == "VALUE_DECREASE_10" ]; then
		python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py overscan_value set $((OVERSCAN_VALUE - 10))
	fi

	update_variables
}

function main_menu() {
    local choice
	
    while true; do
		OVERSCAN_STATE=0

		if [ "$OVERSCAN_ENABLE" == "yes" ]; then
			OVERSCAN_STATE="Enable"
		elif [ "$OVERSCAN_ENABLE" == "no" ]; then
			OVERSCAN_STATE="Disable"
		else
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py overscan_enable set no
			OVERSCAN_STATE="Disable"
		fi
	
        choice=$(dialog --backtitle "PiBoy Configurator v.$piboyconf_version" --title "Overscan on TV mode" \
            --ok-label "Select" --cancel-label "Back" --no-tags \
            --menu "Overscan value is : $OVERSCAN_VALUE" 25 75 20 \
			"OVERSCAN" "1 Overscan is : $OVERSCAN_STATE" \
			"VALUE_INCREASE" "2 Increase overscan value by 1" \
			"VALUE_DECREASE" "3 Decrease overscan value by 1" \
			"VALUE_INCREASE_10" "2 Increase overscan value by 10" \
			"VALUE_DECREASE_10" "3 Decrease overscan value by 10" \
            2>&1 > /dev/tty)
		
		opt=$?
		[ $opt -eq 1 ] && exit
		
        manage_choice choice
    done
}

update_variables
main_menu