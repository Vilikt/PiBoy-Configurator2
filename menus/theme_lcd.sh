#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

# Global vars
PIBOYCONF_ROOT_FOLDER="$HOME/PiBoy-Configurator"
source $PIBOYCONF_ROOT_FOLDER/common.sh >/dev/null 2>&1

ES_THEMES_FOLDER="/etc/emulationstation/themes"

function getESThemesNames() {
	cd $ES_THEMES_FOLDER
	temp=$(ls -d */)
	es_themes=(`echo ${temp///}`)
	
	cd $PIBOYCONF_ROOT_FOLDER/menus
}

function update_variables() {
	LCD_THEME=`python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py theme_lcd get`
}

function manage_choice() {
	export choice
	python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py theme_lcd set
	update_variables
}

function main_menu() {
    local choice
	local menu_line
	
	let i=0
	MENU_LINES=()
	for theme_name in "${es_themes[@]}"; do
		i=$((i+1))
		MENU_LINES+=("$theme_name" "$i $theme_name")
	done

    while true; do
        choice=$(dialog --backtitle "PiBoy Configurator v.$piboyconf_version" --title "Select ES Theme on LCD mode" \
            --ok-label "Select" --cancel-label "Back" --no-tags \
            --menu "Actual is '$LCD_THEME'" 25 75 20 "${MENU_LINES[@]}" 2>&1 > /dev/tty)
		
		opt=$?
		[ $opt -eq 1 ] && exit
		
        manage_choice choice
		
    done
}

getESThemesNames
update_variables
main_menu