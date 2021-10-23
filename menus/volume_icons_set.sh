#!/bin/bash
#####################################################################
#Project					:		Retropie_PiBoy_Configurator
#####################################################################

# Global vars
PIBOYCONF_ROOT_FOLDER="$HOME/PiBoy-Configurator"
source $PIBOYCONF_ROOT_FOLDER/common.sh >/dev/null 2>&1

declare -rA valIconsSet=( 
	['alternate_volume_bar']="Alternate volume bar" 
	['mario_coin']="Mario Coins" 
	['original']="Original" 
	['pacman']="Pacman" 
	['retro']="Retro" 
	['zelda_hearts']="Zelda Hearts"
)


function update_variables() {
	VOL_ICON_SET=`python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py vol_icon_set get`
}

function manage_choice() {
	export choice
	
	python $PIBOYCONF_ROOT_FOLDER/readers/piboy_config_file.py vol_icon_set set
	update_variables
	
	cp $HOME/osd/resources/vol_icons_sets/original/* $HOME/osd/resources/
	cp $HOME/osd/resources/vol_icons_sets/$choice/* $HOME/osd/resources/
}

function main_menu() {
    local choice

    while true; do
        choice=$(dialog --backtitle "PiBoy Configurator v.$piboyconf_version" --title "Volume Icons Set setting" \
            --ok-label "Select" --cancel-label "Back" --no-tags \
            --menu "Volume icons set is : ${valIconsSet[$VOL_ICON_SET]}" 25 75 20 \
			"original" "1 ${valIconsSet[original]}" \
			"alternate_volume_bar" "2 ${valIconsSet[alternate_volume_bar]}" \
			"mario_coin" "3 ${valIconsSet[mario_coin]}" \
			"pacman" "4 ${valIconsSet[pacman]}" \
			"retro" "5 ${valIconsSet[retro]}" \
			"zelda_hearts" "6 ${valIconsSet[zelda_hearts]}" \
            2>&1 > /dev/tty)
		
		opt=$?
		[ $opt -eq 1 ] && exit
		
        manage_choice choice
    done
}

update_variables
main_menu