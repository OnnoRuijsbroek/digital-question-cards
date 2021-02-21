# Digital question cards

Instead of having tens of boxes with questions cards, this can be replaced by a Raspberry Pi with a OLED hat. Started
with ePaper hat, but replaced by OLED since the hat has buttons.

## prerequisites

- placed in /lib folder (updated location and naming and removed unused import (e.g. numpy))
    - https://www.waveshare.com/wiki/1.3inch_OLED_HAT
- raspberry pi zero, with headless linux

## setup

- SPI must be enabled, in /boot/config.txt look for and uncomment "dtparam=spi=on"  or via sudo raspi-config
- sudo apt-get install python3-smbus python3-dev python3-rpi.gpio python3-pip libopenjp2-7 libtiff5
- sudo pip3 install spidev Image

## source files

- the 3 buttons map to 3 categories
- the source files are numbered and suffixed by `.txt`
- the layout of categories and contents (amount of lines) can be configured at `#sourceFiles`

## booting python script

- source https://www.raspberrypi-spy.co.uk/2015/02/how-to-autorun-a-python-script-on-raspberry-pi-boot/
    - sudo raspi-config -> autologin
    - sudo nano /etc/profile
    - sudo python3 /home/pi/main.py & (at the end)
- copy files `scp *.txt pi@192.168.1.1:`
