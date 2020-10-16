cp battery_longevity.sh   /usr/libexec/
cp batterie_supervisor.py /usr/libexec/
cp de.irmo.battery_longevity.plist /Library/LaunchDaemons/

launchctl load /Library/LaunchDaemons/de.irmo.battery_longevity.plist