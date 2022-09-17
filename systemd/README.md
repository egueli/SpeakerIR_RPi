Copy these files to start SpeakerIR at boot:

    sudo cp -av *.service /lib/systemd/system

Then, enable both services:

    sudo systemctl enable {irsetup,speakerir}.service

Then, the app should start automatically when the system boots up.