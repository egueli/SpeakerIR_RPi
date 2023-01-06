1. Copy these files to start SpeakerIR at boot:

    sudo cp -av *.service /lib/systemd/system

2. Edit `/lib/systemd/system/irsetup.service` and `/lib/systemd/system/speakerir.service` to use the actual scripts location instead of `/home/enrico/app`.

Then, enable both services:

    sudo systemctl enable {irsetup,speakerir}.service

Then, the app should start automatically when the system boots up.