#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

# Global vars
PIBOYCONF_ROOT_FOLDER="$HOME/PiBoy-Configurator"
source $PIBOYCONF_ROOT_FOLDER/common.sh >/dev/null 2>&1

function manage_choice() {
	if [ "$choice" == "overlay_set_grid" ]; then
		python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py overlay_style set grid
	elif [ "$choice" == "overlay_set_clean" ]; then
		python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py overlay_style set clean
	fi
}

function main_menu() {
    local choice

    while true; do
		actual_style=`python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py overlay_style get`
		
        choice=$(dialog --backtitle "PiBoy Configurator v.$piboyconf_version" --title "Overlays Style" \
            --ok-label "Select" --cancel-label "Back" --no-tags \
            --menu "Actual : $actual_style" 25 75 20 \
			"overlay_set_grid" "1 Grid" \
			"overlay_set_clean" "2 Clean" \
            2>&1 > /dev/tty)
		
		opt=$?
		[ $opt -eq 1 ] && exit
		
        manage_choice choice
    done
}

main_menu