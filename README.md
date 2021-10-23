# PIBOY-CONFIGURATOR version 1.3.5

# Special Thanks


- __Richard Capewell__ for the Retropie Menu icon
- __DrBuns3n__ for having the patience to point out problems at start-up and offer relevant suggestions
- __Alex Rodriguez__ to have created the different volume images set, and to have given his authorization to integrate them into the project
- __Grow YourOwn__ for his supports

# 1. Installation

## 1.1 SSH
  Connect on SSH to your Pi and type the following commands :
  
    cd /home/pi
    git clone https://github.com/Vilikt/PiBoy-Configurator2.git ./PiBoy-Configurator
    cd PiBoy-Configurator
    sudo python install.py

## 1.2 SFTP
  You may don't want to use SSH. So you can download the sources and upload the Piboy-Configurator folder on /home/pi with FileZilla, WinSCP or something else.
  Then turn on your Piboy and connect a keyboard. Once you are in EmulationStation, press F4 key to get in the command prompt. Then type the following commands :

    cd /home/pi/PiBoy-Configurator
    sudo python install.py

# 2. Updates


  Piboy-Configurator project maybe updated since your first install. Check your actual version on the top left corner in the menu.
  To make an update, go to the command prompt (see 1. Installation) and type the following commands :
  
      cd /home/pi/PiBoy-Configurator
      git pull

  You can also to it within the general menu (see 5.1).

# 3. Add your overlays


  Basically this project was designed to use with the overlay pack available on https://github.com/gallyg/zover4recalbox


  You can see that the pack contains two types of overlays: with CRT effect (grid) and without effect (clean).


  You will see later that you can select the type of overlay you want to use. Note that by default is "grid". Also if you don't want to use multiple types of overlay you can put everything in the default "grid" directory.


# 4. Edit your retroarch configurations files


  The installation script may created two file in each system configs foler : retroarch.cfg.lcd and retroarch.cfg.tv. Each one is a copy of the retroarch.cfg.
  All you need to do now is to edit retroarch.cfg.lcd with the configuration you want for the handheld mode and retroarch.cfg.tv for TV mode.
  
  There is an example with GB system.
  
  __/opt/retropie/configs/gb/retroarch.cfg.lcd__ :

    # Settings made here will only override settings in the global retroarch.cfg if placed above the #include line

    input_remapping_directory = "/opt/retropie/configs/gb/"

    custom_viewport_height = "480"
    custom_viewport_width = "534"
    video_shader = "~/.config/retroarch/shaders/hq2x&lcd3x.glslp"
    savefile_directory = "~/RetroPie/saves/gb/sram/"
    savestate_directory = "~/RetroPie/saves/gb/savestates/"

    input_overlay_enable = true
    input_overlay = "~/.config/retroarch/overlay/LCD/gb-dmg.cfg"
    input_overlay_opacity = 1.0
    input_overlay_scale = 1.0
    video_scale_integer = "true"


    gambatte_dark_filter_level = "0"
    gambatte_gb_bootloader = "enabled"
    gambatte_gb_colorization = "internal"
    gambatte_gb_hwmode = "GB"
    gambatte_gb_internal_palette = "TWB27 - Greenscale"
    gambatte_gbc_color_correction = "GBC only"
    gambatte_gbc_color_correction_mode = "accurate"
    gambatte_gbc_frontlight_position = "central"
    gambatte_mix_frames = "mix"
    gambatte_show_gb_link_settings = "disabled"
    gambatte_up_down_allowed = "disabled"
    #include "/opt/retropie/configs/all/retroarch.cfg"
  
  
   /opt/retropie/configs/gb/retroarch.cfg.tv :
   
    # Settings made here will only override settings in the global retroarch.cfg if placed above the #include line

    input_remapping_directory = "/opt/retropie/configs/gb/"

    savefile_directory = "~/RetroPie/saves/gb/sram/"
    savestate_directory = "~/RetroPie/saves/gb/savestates/"

    input_overlay_enable = true
    input_overlay_opacity = 0.7
    input_overlay_scale = 1.0
    input_overlay = "~/.config/retroarch/overlay/TV/[overlay_style]/handhelds/gb_overlay.cfg"
    input_overlay_hide_in_menu = "false"
    aspect_ratio_index = "23"
    video_scale_integer = "false"

    video_message_pos_x = "0.220000"
    video_message_pos_y = "0.120000"
    custom_viewport_x = "409"
    custom_viewport_y = "35"
    custom_viewport_width = "1102"
    custom_viewport_height = "1010"


    gambatte_dark_filter_level = "0"
    gambatte_gb_bootloader = "enabled"
    gambatte_gb_colorization = "internal"
    gambatte_gb_hwmode = "GB"
    gambatte_gb_internal_palette = "GB - DMG"
    gambatte_gbc_color_correction = "GBC only"
    gambatte_gbc_color_correction_mode = "accurate"
    gambatte_gbc_frontlight_position = "central"
    gambatte_mix_frames = "mix"
    gambatte_show_gb_link_settings = "disabled"
    gambatte_up_down_allowed = "disabled"
    #include "/opt/retropie/configs/all/retroarch.cfg"

On startup the autoconfig.py is executed and it replaces each retroarch.cfg file with the content of retroarch.cfg.lcd or retroarch.cfg.tv if you are plugged on HDMI or not.

***NOTE*** : "[overlay_style]" **must** be written this way. Indeed, the script will replace this with "grid" or "clean" depending on what you have configured (see 5.1).

# 5. PiBoy Configuration entry in Retropiemenu


  A new entry named "PiBoy Configuration" is created in RetropieMenu.
  If you select it you will go on the principal menu "General Settings" :
  
  ![Alt text](https://i.imgur.com/LvfFBo2.png "General Settings")
  
## 5.1 Update

Select this option to perform an update of PiBoy-Configurator (you must be connected to internet).  
  
## 5.2 Overlay Style in TV mode

Here you can choose the style of your overlay in ~~TV~~ HDMI mode.
Assuming that you have opted for the overlays of https://github.com/gallyg/zover4recalbox, you can choose between those located in the  **/opt/retropie/configs/all/retroarch/overlay/TV/grid** directory or those of the __/opt/retropie/configs/all/retroarch/overlay/TV/clean__ directory.
Anyway, put your overlays in one of the directories in question and choose it here.

## 5.3 OSD

Simply choose the icons you want to be displayed by the OSD. Select each one to change it.

![Alt text](https://puu.sh/GVqF8/d32e1eeeae.png "OSD")

## 5.4 Green & Red LED settings

Simply choose the amount in percent of the LED's power.

## 5.5 WiFi and Bluetooth toggle

Here you can determine whether WiFi or Bluetooth is enabled or not depending on the modes.

![Alt text](https://puu.sh/GVqHi/c61d895748.png "Toggle WiFi")

![Alt text](https://puu.sh/GVqRO/90684f6210.png "Toggle Bluetooth")

### 1

The first entry let you choose to toggle ON or OFF **ONLY** if the option for the mode you're in is "whatever".
For instance, if your are on HDMI mode and the second entry is set to _Always ENABLE in HDMI mode_, the WiFi or Bluetooth state will stay ON !

### 2
The second entries determine the thing in HDMI mode and can take three kind of value :

> Always ENABLE in HDMI mode

The WiFi or Bluetooth will always toggle to ON in HDMI mode

> Always DISABLE in HDMI mode

The WiFi or Bluetooth will always toggle to OFF in HDMI mode

> In HDMI mode : whatever

The WiFi or Bluetooth will always toggle depends on the last state

### 3
The third entries determine the thing in LCD mode and can take three kind of value :

> Always ENABLE in LCD mode

The WiFi or Bluetooth will always toggle to ON in LCD mode

> Always DISABLE in LCD mode

The WiFi or Bluetooth will always toggle to OFF in LCD mode

> In LCD mode : whatever

The WiFi or Bluetooth will always toggle depends on the last state

## 5.6 Select ES Theme on TV/LCD mode

![Alt text](https://puu.sh/GVqXF/e43a7228d3.png "Select ES Theme on LCD mode")

You have the list of the EmulationStation themes available in the **/etc/emulationstation/themes** directory. Just select wich one you want for each mode.

## 5.7 Onboard controller behavior

Select if the onboard controller of the piboy should be enable or not in HDMI mode.

## 5.8 Overscan on TV mode

![Alt text](https://puu.sh/GVr19/37ce137455.png "Overscan on TV mode")

Enable overscan or not and set the value. It will be the same for each side: top, bottom, left, right
