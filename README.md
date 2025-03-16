# Setup

## Configure IR reception on Raspberry Pi

Uncomment/add the following line in `/boot/config.txt`:

    dtoverlay=gpio-ir,gpio_pin=4

(feel free to replace 4 with your desired GPIO pin number)

After a reboot, the system should have a file/symlink at `/dev/input/by-path/platform-ir-receiver@4-event`.

## Setup venv required Python packages

    python3 -m venv .venv
    . .venv/bin/activate
    pip3 install gpiozero RPi.GPIO evdev

## Create IR scancodes file

    sudo ir-keytable -p all -t

Press the five buttons on your IR remote, then write the respective IR codes and protocols into a `.toml` file. See [acer.toml] and [lg.toml] for examples.

## OSMC

Some notes regarding OSMC:

* In OSMC, `evdev` cannot be installed via pip: it needs compilation on device, which may not be easy to do. Install evdev from the OS package manager e.g. `sudo apt install python3-evdev`.

* OSMC starts LIRC automatically, and it takes the same device used by SpeakerIR. As I control my OSMC via HDMI CEC, I don't need any IR support. So I ran this to completely disable LIRC:

    sudo chmod -x /lib/udev/lircd_helper

* You may need to install packages and run the application as root.

# Run

From inside venv:

    ./main.py

Or outside:

    .venv/bin/python3 main.py

# Run at system startup (Raspbian)

    sudo ./systemd_install.sh $USER

# Random notes

The `tm1637.py` file is copied from https://github.com/SimonStJG/raspberrypi-tm1637/tree/master.

Why use that version instead of [the original tm1637 library](https://pypi.org/project/raspberrypi-tm1637/)? Because for some reason, the underlying wiringpi library conflicts with GPIOs when used as input devices (evdev), while the gpiozero library used by that version doesn't cause any conflict.

