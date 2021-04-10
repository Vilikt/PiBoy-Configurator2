#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

# Global vars
PIBOYCONF_ROOT_FOLDER="$HOME/PiBoy-Configurator"
source $PIBOYCONF_ROOT_FOLDER/common.sh >/dev/null 2>&1

function update_variables() {
	WIFI_ENABLE=`python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_enable get`
	WIFI_ALWAYS_ENABLE_HDMI=`python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_always_enable_hdmi get`
	WIFI_ALWAYS_ENABLE_LCD=`python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_always_enable_lcd get`
}

function manage_choice() {
	if [ "$choice" == "WIFI" ]; then
		if [ "$WIFI_ENABLE" == "no" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_enable set yes
		elif [ "$WIFI_ENABLE" == "yes" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_enable set no
		fi
	elif [ "$choice" == "ALWAYS_HDMI" ]; then
		if [ "$WIFI_ALWAYS_ENABLE_HDMI" == "undefined" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_always_enable_hdmi set yes
		elif [ "$WIFI_ALWAYS_ENABLE_HDMI" == "yes" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_always_enable_hdmi set no
		elif [ "$WIFI_ALWAYS_ENABLE_HDMI" == "no" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_always_enable_hdmi set undefined
		fi
	elif [ "$choice" == "ALWAYS_LCD" ]; then
		if [ "$WIFI_ALWAYS_ENABLE_LCD" == "undefined" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_always_enable_lcd set yes
		elif [ "$WIFI_ALWAYS_ENABLE_LCD" == "yes" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_always_enable_lcd set no
		elif [ "$WIFI_ALWAYS_ENABLE_LCD" == "no" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_always_enable_lcd set undefined
		fi
	fi

	update_variables
}

function main_menu() {
    local choice

    while true; do
		WIFI_STATE=0

		if [ "$WIFI_ENABLE" == "yes" ]; then
			WIFI_STATE="Enable"
		elif [ "$WIFI_ENABLE" == "no" ]; then
			WIFI_STATE="Disable"
		fi
		
		if [ "$WIFI_ALWAYS_ENABLE_HDMI" == "yes" ]; then
			ALWAYS_HDMI_TEXT="Always ENABLE in HDMI mode"
		elif [ "$WIFI_ALWAYS_ENABLE_HDMI" == "no" ]; then
			ALWAYS_HDMI_TEXT="Always DISABLE in HDMI mode"
		elif [ "$WIFI_ALWAYS_ENABLE_HDMI" == "undefined" ]; then
			ALWAYS_HDMI_TEXT="In HDMI mode : whatever"
		else
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_always_enable_hdmi set undefined
			ALWAYS_HDMI_TEXT="In HDMI mode : whatever"
		fi
		
		if [ "$WIFI_ALWAYS_ENABLE_LCD" == "yes" ]; then
			ALWAYS_LCD_TEXT="Always ENABLE in LCD mode"
		elif [ "$WIFI_ALWAYS_ENABLE_LCD" == "no" ]; then
			ALWAYS_LCD_TEXT="Always DISABLE in LCD mode"
		elif [ "$WIFI_ALWAYS_ENABLE_LCD" == "undefined" ]; then
			ALWAYS_LCD_TEXT="In LCD mode : whatever"
		else
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py wifi_always_enable_lcd set undefined
			ALWAYS_LCD_TEXT="In LCD mode : whatever"
		fi
		
        choice=$(dialog --backtitle "PiBoy Configurator v.$piboyconf_version" --title "Toggle WiFi" \
            --ok-label "Select" --cancel-label "Back" --no-tags \
            --menu "Configure WiFi behavior" 25 75 20 \
			"WIFI" "1 Now WiFi is : $WIFI_STATE" \
			"ALWAYS_HDMI" "3 $ALWAYS_HDMI_TEXT" \
			"ALWAYS_LCD" "4 $ALWAYS_LCD_TEXT" \
            2>&1 > /dev/tty)
		
		opt=$?
		[ $opt -eq 1 ] && exit
		
        manage_choice choice
    done
}

update_variables
main_menu