#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

# Global vars
PIBOYCONF_ROOT_FOLDER="$HOME/PiBoy-Configurator"
source $PIBOYCONF_ROOT_FOLDER/common.sh >/dev/null 2>&1

function update_variables() {
	RED_LED=`sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py redled value_below get`
}

function manage_choice() {
	sudo python $PIBOYCONF_ROOT_FOLDER/readers/osd_config_file.py redled value_below set "$choice"
	
	update_variables
}

function main_menu() {
    local choice

    while true; do
        choice=$(dialog --backtitle "PiBoy Configurator v.$piboyconf_version" --title "Red LED setting" \
            --ok-label "Select" --cancel-label "Back" --no-tags \
            --menu "Red LED is at $RED_LED%" 25 75 20 \
			"10" "1 10%" \
			"20" "2 20%" \
			"30" "3 30%" \
			"40" "4 40%" \
			"50" "5 50%" \
			"60" "6 60%" \
			"70" "7 70%" \
			"80" "8 80%" \
			"90" "9 90%" \
			"100" "10 100%" \
            2>&1 > /dev/tty)
		
		opt=$?
		[ $opt -eq 1 ] && exit
		
        manage_choice choice
    done
}

update_variables
main_menu