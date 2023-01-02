# Configuring IR reception on Raspberry Pi

Uncomment/add the following line in `/boot/config.txt`:

    dtoverlay=gpio-ir,gpio_pin=4

(feel free to replace 4 with your desired GPIO pin number)

After a reboot, the system should have a file/symlink at `/dev/input/by-path/platform-ir-receiver@4-event`.

# Creating IR scancodes file

    sudo ir-keytable -p all -t

Press the five buttons on your IR remote, then write the respective IR codes and protocols into a `.toml` file. See [acer.toml] and [lg.toml] for examples.

# Random notes

The `tm1637.py` file is copied from https://github.com/SimonStJG/raspberrypi-tm1637/tree/master.

Why use that version instead of [the original tm1637 library](https://pypi.org/project/raspberrypi-tm1637/)? Because for some reason, the underlying wiringpi library conflicts with GPIOs when used as input devices (evdev), while the gpiozero library used by that version doesn't cause any conflict.

