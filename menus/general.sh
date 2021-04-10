#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

# Global vars
PIBOYCONF_ROOT_FOLDER="$HOME/PiBoy-Configurator"

FILE=$PIBOYCONF_ROOT_FOLDER/piboy.cfg

function main_menu() {
    local choice

    while true; do
		source $PIBOYCONF_ROOT_FOLDER/common.sh >/dev/null 2>&1
	
        choice=$(dialog --backtitle "PiBoy Configurator v.$piboyconf_version" --title "General Settings" \
            --ok-label "Select" --cancel-label "Back" --no-tags \
            --menu "Settings" 25 75 20 \
			"update" "1 Update PiBoy-Configurator" \
			"overlay_style" "2 Overlay Style in TV mode" \
			"osd_configuration" "3 OSD" \
			"green_led_setting" "4 Green LED setting" \
			"red_led_setting" "5 Red LED setting" \
			"toggle_wifi" "6 Wifi Toggle" \
			"toggle_bluetooth" "7 Bluetooth Toggle" \
			"theme_lcd" "8 Set ES Theme on LCD mode" \
			"theme_tv" "9 Set ES Theme on TV mode" \
			"onboard_controller" "10 Set onboard controller behavior" \
			"overscan" "11 Set screen overscan on TV mode" \
            2>&1 > /dev/tty)
		
		opt=$?
		[ $opt -eq 1 ] && exit
		
        bash $PIBOYCONF_MENU_FOLDER/$choice.sh
		
    done
}

if [[ -f "$FILE" ]]; then
    main_menu
else
    sudo python "$PIBOYCONF_ROOT_FOLDER"/install.py --only_create_conf_file
	main_menu
fi
