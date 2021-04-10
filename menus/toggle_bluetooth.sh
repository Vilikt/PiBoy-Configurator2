#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

# Global vars
PIBOYCONF_ROOT_FOLDER="$HOME/PiBoy-Configurator"
source $PIBOYCONF_ROOT_FOLDER/common.sh >/dev/null 2>&1

function update_variables() {
	BT_ENABLE=`python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_enable get`
	BT_ALWAYS_ENABLE_HDMI=`python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_always_enable_hdmi get`
	BT_ALWAYS_ENABLE_LCD=`python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_always_enable_lcd get`
}

function manage_choice() {
	if [ "$choice" == "BT" ]; then
		if [ "$BT_ENABLE" == "no" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_enable set yes
		elif [ "$BT_ENABLE" == "yes" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_enable set no
		fi
	elif [ "$choice" == "ALWAYS_HDMI" ]; then
		if [ "$BT_ALWAYS_ENABLE_HDMI" == "undefined" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_always_enable_hdmi set yes
		elif [ "$BT_ALWAYS_ENABLE_HDMI" == "yes" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_always_enable_hdmi set no
		elif [ "$BT_ALWAYS_ENABLE_HDMI" == "no" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_always_enable_hdmi set undefined
		fi
	elif [ "$choice" == "ALWAYS_LCD" ]; then
		if [ "$BT_ALWAYS_ENABLE_LCD" == "undefined" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_always_enable_lcd set yes
		elif [ "$BT_ALWAYS_ENABLE_LCD" == "yes" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_always_enable_lcd set no
		elif [ "$BT_ALWAYS_ENABLE_LCD" == "no" ]; then
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_always_enable_lcd set undefined
		fi
	fi

	update_variables
}

function main_menu() {
    local choice
	
	while true; do
		BT_STATE=0

		if [ "$BT_ENABLE" == "yes" ]; then
			BT_STATE="Enable"
		elif [ "$BT_ENABLE" == "no" ]; then
			BT_STATE="Disable"
		fi
		
		if [ "$BT_ALWAYS_ENABLE_HDMI" == "yes" ]; then
			ALWAYS_HDMI_TEXT="Always ENABLE in HDMI mode"
		elif [ "$BT_ALWAYS_ENABLE_HDMI" == "no" ]; then
			ALWAYS_HDMI_TEXT="Always DISABLE in HDMI mode"
		elif [ "$BT_ALWAYS_ENABLE_HDMI" == "undefined" ]; then
			ALWAYS_HDMI_TEXT="In HDMI mode : whatever"
		else
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_always_enable_hdmi set undefined
			ALWAYS_HDMI_TEXT="In HDMI mode : whatever"
		fi
		
		if [ "$BT_ALWAYS_ENABLE_LCD" == "yes" ]; then
			ALWAYS_LCD_TEXT="Always ENABLE in LCD mode"
		elif [ "$BT_ALWAYS_ENABLE_LCD" == "no" ]; then
			ALWAYS_LCD_TEXT="Always DISABLE in LCD mode"
		elif [ "$BT_ALWAYS_ENABLE_LCD" == "undefined" ]; then
			ALWAYS_LCD_TEXT="In LCD mode : whatever"
		else
			python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py bt_always_enable_lcd set undefined
			ALWAYS_LCD_TEXT="In LCD mode : whatever"
		fi
		
        choice=$(dialog --backtitle "PiBoy Configurator v.$piboyconf_version" --title "Toggle Bluetooth" \
            --ok-label "Select" --cancel-label "Back" --no-tags \
            --menu "Configure Bluetooth behavior" 25 75 20 \
			"BT" "1 Now Bluetooth is : $BT_STATE" \
			"ALWAYS_HDMI" "2 $ALWAYS_HDMI_TEXT" \
			"ALWAYS_LCD" "3 $ALWAYS_LCD_TEXT" \
            2>&1 > /dev/tty)
		
		opt=$?
		[ $opt -eq 1 ] && exit
		
        manage_choice choice
    done
}

update_variables
main_menu