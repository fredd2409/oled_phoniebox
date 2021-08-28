#!/usr/bin/python3
from gpiozero import Button
from signal import pause
from subprocess import check_call
from time import sleep

# This script will block any I2S DAC e.g. from Hifiberry, Justboom, ES9023, PCM5102A
# due to the assignment of GPIO 19 and 21 to a buttons

# 2018-10-31
# Added the function on holding volume + - buttons to change the volume in 0.3s interval
#
# 2018-10-15
# this script has the `pull_up=True` for all pins. See the following link for additional info:
# https://github.com/MiczFlor/RPi-Jukebox-RFID/issues/259#issuecomment-430007446
#
# 2017-12-12
# This script was copied from the following RPi forum post:
# https://forum-raspberrypi.de/forum/thread/13144-projekt-jukebox4kids-jukebox-fuer-kinder/?postID=312257#post312257
# I have not yet had the time to test is, so I placed it in the misc folder.
# If anybody has ideas or tests or experience regarding this solution, please create pull requests or contact me.

jukebox4kidsPath = "/home/pi/RPi-Jukebox-RFID"

def def_shutdown():
    check_call(jukebox4kidsPath+"/scripts/playout_controls.sh -c=shutdown", shell=True)

def def_volU():
    check_call(jukebox4kidsPath+"/scripts/playout_controls.sh -c=volumeup", shell=True)

def def_volD():
    check_call(jukebox4kidsPath+"/scripts/playout_controls.sh -c=volumedown", shell=True)

def def_vol0():
    check_call(jukebox4kidsPath+"/scripts/playout_controls.sh -c=mute", shell=True)

def def_next():
    for x in range(0, 19):
        if btn_next.is_pressed == True :
            sleep(0.1)
        else:
            check_call(jukebox4kidsPath+"/scripts/playout_controls.sh -c=playernext", shell=True)
            break

def def_contrastup():
    if btn_prev.is_pressed == True :
        check_call("/usr/bin/touch /tmp/o4p_overview.temp", shell=True)
    else:
        check_call("/usr/bin/python3 /home/pi/oled_phoniebox/scripts/contrast/contrast_up.py", shell=True)

def def_contrastdown():
    if btn_next.is_pressed == True :
        check_call("/usr/bin/touch /tmp/o4p_overview.temp", shell=True)
    else:
        check_call("/usr/bin/python3 /home/pi/oled_phoniebox/scripts/contrast/contrast_down.py", shell=True)

def def_prev():
    for x in range(0, 19):
        if btn_prev.is_pressed == True :
            sleep(0.1)
        else:
            check_call(jukebox4kidsPath+"/scripts/playout_controls.sh -c=playerprev", shell=True)
            break

def def_halt():
#    for x in range(0, 19):
#        if btn_halt.is_pressed == True :
#            sleep(0.1)
#        else:
    check_call(jukebox4kidsPath+"/scripts/playout_controls.sh -c=playerpause", shell=True)
#            break
	
def toggle_display():
    check_call("/home/pi/oled_phoniebox/scripts/toggle_display/toggle_display.sh", shell=True)

#btn_shut = Button(3, hold_time=2)
#btn_vol0 = Button(21,pull_up=True)
btn_volup = Button(7,pull_up=True,hold_time=0.3,hold_repeat=True)
btn_voldown = Button(13,pull_up=True,hold_time=0.3,hold_repeat=True)
btn_next = Button(8,pull_up=True,hold_time=2.0,hold_repeat=False)
btn_prev = Button(27,pull_up=True,hold_time=2.0,hold_repeat=False)
btn_halt = Button(12,pull_up=True,hold_time=0.0,hold_repeat=False)

#btn_shut.when_held = def_shutdown
#btn_vol0.when_pressed = def_vol0
btn_volup.when_pressed = def_volU
#When the Volume Up button was held for more than 0.3 seconds every 0.3 seconds he will call a ra$
btn_volup.when_held = def_volU
btn_voldown.when_pressed = def_volD
#When the Volume Down button was held for more than 0.3 seconds every 0.3 seconds he will lower t$
btn_voldown.when_held = def_volD
btn_next.when_pressed = def_next
btn_next.when_held = def_contrastup
btn_prev.when_pressed = def_prev
btn_prev.when_held = def_contrastdown
btn_halt.when_pressed = def_halt
btn_halt.when_held = toggle_display

pause()
